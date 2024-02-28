import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import tkinter.ttk as ttk

class ImageProcessingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Customized Image Processing App")
        self.master.geometry("1250x600")
        self.master.configure(bg="#F0F0F0")

        self.header_frame = tk.Frame(master, bg="#1976D2")  # Changed header color to blue
        self.header_frame.pack(fill=tk.X)

        self.header_label = tk.Label(self.header_frame, text="My Custom Image Processor", font=("Arial", 24), bg="#1976D2", fg="white", padx=20)  # Changed header text
        self.header_label.pack(anchor=tk.CENTER)

        self.navbar_frame = tk.Frame(master, bg="#00ACC1")  # Changed navbar color to teal
        self.navbar_frame.pack(fill=tk.X)

        self.process_options = ["Select Operation", "Convert to RGB", "Convert to Grayscale", "Convert to Binary", "Convert to BGR", "Convert to GRB", "Edge Detection", "Blur"]
        self.selected_process = tk.StringVar(self.master)
        self.selected_process.set(self.process_options[0])  # Default option

        self.process_dropdown = tk.OptionMenu(self.navbar_frame, self.selected_process, *self.process_options)
        self.process_dropdown.config(font=("Arial", 14), bg="#00ACC1", fg="white")
        self.process_dropdown["menu"].config(font=("Arial", 14), bg="#00ACC1", fg="white")
        self.process_dropdown.pack(side=tk.LEFT, padx=20, pady=10)

        self.btn_brightness_contrast = tk.Button(self.navbar_frame, text="Adjust Brightness/Contrast", command=self.adjust_brightness_contrast, font=("Arial", 14), bg="#FF6F00", fg="white", relief=tk.FLAT)  # Changed button color to orange
        self.btn_brightness_contrast.pack(side=tk.LEFT, padx=20, pady=10)

        self.btn_add_annotation = tk.Button(self.navbar_frame, text="Add Annotation", command=self.add_annotation, font=("Arial", 14), bg="#E91E63", fg="white", relief=tk.FLAT)  # Changed button color to pink
        self.btn_add_annotation.pack(side=tk.LEFT, padx=20, pady=10)

        self.btn_reset = tk.Button(self.navbar_frame, text="Reset", command=self.reset_image, font=("Arial", 14), bg="#4CAF50", fg="white", relief=tk.FLAT)  # Changed button color to green
        self.btn_reset.pack(side=tk.LEFT, padx=20, pady=10)

        self.btn_upload = tk.Button(self.navbar_frame, text="Upload Image", command=self.upload_image, font=("Arial", 14), bg="#FFC107", fg="white", relief=tk.FLAT)  # Changed button color to yellow
        self.btn_upload.pack(side=tk.LEFT, padx=20, pady=10)

        self.btn_save = tk.Button(self.navbar_frame, text="Save Image", command=self.save_image, font=("Arial", 14), bg="#795548", fg="white", relief=tk.FLAT)
        self.btn_save.pack(side=tk.LEFT, padx=20, pady=10)

        self.theme_options = ["Light", "Dark"]
        self.selected_theme = tk.StringVar(self.master)
        self.selected_theme.set(self.theme_options[0])  # Default option

        self.theme_dropdown = tk.OptionMenu(self.navbar_frame, self.selected_theme, *self.theme_options, command=self.change_theme)
        self.theme_dropdown.config(font=("Arial", 14), bg="#00ACC1", fg="white")
        self.theme_dropdown["menu"].config(font=("Arial", 14), bg="#00ACC1", fg="white")
        self.theme_dropdown.pack(side=tk.LEFT, padx=20, pady=10)

        self.canvas = tk.Canvas(master, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.image = None
        self.cv_image = None
        self.tk_image = None

    def change_theme(self, event=None):
        selected_theme = self.selected_theme.get()
        if selected_theme == "Dark":
            self.master.configure(bg="#212121")  # Changed background color to dark grey
            self.header_frame.configure(bg="#424242")  # Changed header frame color to grey
            self.header_label.configure(bg="#424242", fg="white")  # Changed header text color
            self.navbar_frame.configure(bg="#303F9F")  # Changed navbar color to dark blue
            self.process_dropdown.config(bg="#303F9F", fg="white")  # Changed dropdown color to dark blue
            self.btn_brightness_contrast.config(bg="#FF5722", fg="white")  # Changed button color to deep orange
            self.btn_add_annotation.config(bg="#FF5252", fg="white")  # Changed button color to red
            self.btn_reset.config(bg="#4CAF50", fg="white")  # Changed button color to green
            self.btn_upload.config(bg="#FFD600", fg="white")  # Changed button color to yellow
            self.btn_save.config(bg="#795548", fg="white")  # Changed button color to brown
            self.theme_dropdown.config(bg="#303F9F", fg="white")  # Changed dropdown color to dark blue
        else:
            self.master.configure(bg="#F0F0F0")
            self.header_frame.configure(bg="#1976D2")
            self.header_label.configure(bg="#1976D2", fg="white")
            self.navbar_frame.configure(bg="#00ACC1")
            self.process_dropdown.config(bg="#00ACC1", fg="white")
            self.btn_brightness_contrast.config(bg="#FF6F00", fg="white")
            self.btn_add_annotation.config(bg="#E91E63", fg="white")
            self.btn_reset.config(bg="#4CAF50", fg="white")
            self.btn_upload.config(bg="#FFC107", fg="white")
            self.btn_save.config(bg="#795548", fg="white")
            self.theme_dropdown.config(bg="#00ACC1", fg="white")

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = cv2.imread(file_path)
                if self.image is None:
                    messagebox.showerror("Error", "Failed to load image. Please select a valid image file.")
                    return
                self.cv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                self.show_image()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_image(self):
        if self.tk_image:
            self.canvas.delete("all")
        if len(self.cv_image.shape) == 3:  # Color image
            height, width, _ = self.cv_image.shape
        else:  # Grayscale image
            height, width = self.cv_image.shape
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        scale = min(canvas_width / width, canvas_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = cv2.resize(self.cv_image, (new_width, new_height))
        self.tk_image = ImageTk.PhotoImage(image=Image.fromarray(resized_image))
        x_offset = (canvas_width - new_width) // 2
        y_offset = (canvas_height - new_height) // 2
        self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=self.tk_image)

    def process_image(self):
        if self.image is not None:
            option = self.selected_process.get()
            if option == "Select Operation":
                messagebox.showinfo("Info", "Please select an operation.")
            elif option == "Convert to RGB":
                self.convert_to_rgb()
            elif option == "Convert to Grayscale":
                self.convert_to_grayscale()
            elif option == "Convert to Binary":
                self.convert_to_binary()
            elif option == "Adjust Brightness/Contrast":
                self.adjust_brightness_contrast()
            elif option == "Convert to BGR":
                self.convert_to_bgr()
            elif option == "Convert to GRB":
                self.convert_to_grb()
            elif option == "Edge Detection":
                self.detect_edges()
            elif option == "Blur":
                self.apply_blur()

    def convert_to_rgb(self):
        if self.image is not None:
            self.cv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.show_image()

    def convert_to_grayscale(self):
        if self.image is not None:
            self.cv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.show_image()

    def convert_to_binary(self):
        if self.image is not None:
            threshold = simpledialog.askinteger("Threshold", "Enter threshold value (0-255):", parent=self.master, minvalue=0, maxvalue=255)
            if threshold is not None:
                gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                _, self.cv_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
                self.show_image()

    def adjust_brightness_contrast(self):
        if self.image is not None:
            alpha = 1.0  # Contrast control (1.0-3.0)
            beta = 0    # Brightness control (0-100)
            self.cv_image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.show_image()

    def add_annotation(self):
        if self.image is not None:
            cv2.putText(self.cv_image, "Sample Text", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(self.cv_image, (100, 100), (300, 300), (0, 255, 0), 2)
            cv2.circle(self.cv_image, (200, 200), 50, (0, 0, 255), 2)
            cv2.line(self.cv_image, (0, 0), (300, 300), (255, 255, 0), 2)
            self.show_image()

    def reset_image(self):
        if self.image is not None:
            self.cv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.show_image()

    def save_image(self):
        if self.image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(self.cv_image, cv2.COLOR_RGB2BGR))

    def convert_to_bgr(self):
        if self.image is not None:
            self.cv_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
            self.show_image()

    def convert_to_grb(self):
        if self.image is not None:  
            self.cv_image = self.image[:, :, [1, 0, 2]]  # Swap channels to convert to GRB
            self.show_image()
    
    def detect_edges(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            self.cv_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            self.show_image()

    def apply_blur(self):
        if self.image is not None:
            blur_amount = simpledialog.askinteger("Gaussian Blur", "Enter blur amount (odd number):", parent=self.master, minvalue=1)
            if blur_amount is not None:
                self.cv_image = cv2.GaussianBlur(self.cv_image, (blur_amount, blur_amount), 0)
                self.show_image()
def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    process_button = tk.Button(root, text="Process", command=app.process_image, font=("Arial", 14), bg="#FF5722", fg="white", relief=tk.FLAT)
    process_button.pack(side=tk.BOTTOM, padx=20, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()
