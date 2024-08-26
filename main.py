import tkinter as tk
import cv2
import numpy as np
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance


class ImageEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PCD")
        self.root.geometry("1000x600")
        self.root.configure(bg="#2C3E50")  # Background warna gelap

        self.current_image_path = None
        self.original_image = None
        self.processed_image = None

        # Frame kiri untuk tombol dan slider
        control_frame = tk.Frame(root, bg="#34495E")
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Menambahkan gaya font
        font_style = ("Helvetica", 12, "bold")

        # Tombol untuk memuat gambar
        self.load_button = tk.Button(control_frame, text="Muat Gambar", command=self.load_image, bg="#1ABC9C",
                                     fg="white", font=font_style)
        self.load_button.pack(pady=10)

        # Slider untuk mengatur tingkat kontras
        self.contrast_slider = self.create_slider(control_frame, "Tingkat Kontras: 1.0", 0.5, 3.0, 1.0,
                                                  self.update_image)

        # Slider untuk mengatur tingkat ketajaman
        self.sharpen_slider = self.create_slider(control_frame, "Tingkat Ketajaman: 1.0", 0.0, 2.0, 1.0,
                                                 self.update_image)

        # Slider untuk mengatur pengurangan noise
        self.noise_slider = self.create_slider(control_frame, "Tingkat Noise: 0", 0, 50, 0, self.update_image)

        # Slider untuk mengatur tingkat kecerahan
        self.brightness_slider = self.create_slider(control_frame, "Tingkat Kecerahan: 1.0", 0.5, 3.0, 1.0,
                                                    self.update_image)

        # Slider untuk mengatur saturasi warna
        self.color_slider = self.create_slider(control_frame, "Tingkat Warna: 1.0", 0.0, 2.0, 1.0, self.update_image)

        # Tombol untuk menyimpan gambar
        self.save_button = tk.Button(control_frame, text="Simpan Gambar", command=self.save_image, bg="#E74C3C",
                                     fg="white", font=font_style)
        self.save_button.pack(pady=10)

        # Frame kanan untuk menampilkan gambar
        image_frame = tk.Frame(root, bg="#34495E")
        image_frame.grid(row=0, column=1, padx=10, pady=10)

        # Label untuk menampilkan gambar
        self.image_label = tk.Label(image_frame)
        self.image_label.pack()

    def create_slider(self, parent, label_text, from_, to_, default_value, command):
        """Fungsi untuk membuat slider dan label"""
        label = tk.Label(parent, text=label_text, bg="#34495E", fg="white", font=("Helvetica", 12))
        label.pack(pady=5)
        slider = ttk.Scale(parent, from_=from_, to=to_, orient="horizontal", value=default_value, command=command)
        slider.pack(pady=10)
        return slider

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.current_image_path = file_path
            self.original_image = Image.open(file_path)
            self.processed_image = self.original_image.copy()
            self.display_image(self.original_image)

    def display_image(self, img):
        img.thumbnail((700, 500))  # Menyesuaikan ukuran gambar dengan layar
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk  # Menyimpan referensi agar gambar ditampilkan

    def update_image(self, val):
        if self.original_image:
            contrast_factor = float(self.contrast_slider.get())
            sharpening_factor = float(self.sharpen_slider.get())
            noise_level = int(self.noise_slider.get())
            brightness_factor = float(self.brightness_slider.get())
            color_factor = float(self.color_slider.get())

            # Terapkan kecerahan
            enhancer = ImageEnhance.Brightness(self.original_image)
            temp_image = enhancer.enhance(brightness_factor)

            # Terapkan kontras
            enhancer = ImageEnhance.Contrast(temp_image)
            temp_image = enhancer.enhance(contrast_factor)

            # Terapkan ketajaman
            enhancer = ImageEnhance.Sharpness(temp_image)
            temp_image = enhancer.enhance(sharpening_factor)

            # Terapkan saturasi warna
            enhancer = ImageEnhance.Color(temp_image)
            temp_image = enhancer.enhance(color_factor)

            # Konversi gambar ke format OpenCV untuk pengurangan noise
            temp_image_cv = np.array(temp_image)
            temp_image_cv = cv2.cvtColor(temp_image_cv, cv2.COLOR_RGB2BGR)

            # Terapkan pengurangan noise
            if noise_level > 0:
                temp_image_cv = cv2.fastNlMeansDenoisingColored(temp_image_cv, None, noise_level, noise_level, 7, 21)

            # Konversi kembali ke format PIL
            temp_image_cv = cv2.cvtColor(temp_image_cv, cv2.COLOR_BGR2RGB)
            self.processed_image = Image.fromarray(temp_image_cv)

            self.display_image(self.processed_image)
        else:
            messagebox.showwarning("Peringatan", "Tidak ada gambar yang dimuat")

    def save_image(self):
        if self.processed_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if save_path:
                self.processed_image.save(save_path)
                messagebox.showinfo("Informasi", "Gambar berhasil disimpan")
        else:
            messagebox.showwarning("Peringatan", "Tidak ada gambar yang diproses untuk disimpan")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
