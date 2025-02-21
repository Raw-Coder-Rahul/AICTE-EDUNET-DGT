import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

class SteganographyEncryptor:
    def __init__(self, master):
        self.master = master
        master.title("Image Encryption Tool")
        master.geometry("700x600")

        self.canvas = tk.Canvas(master, width=700, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load and resize the background image to fit the canvas
        original_image = Image.open("images/red black.jpg")
        resized_image = original_image.resize((700, 600), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.label = tk.Label(master, text="Steganography Image Encryption", bg="lightblue", font=("Times New Roman", 16, "bold"))
        self.canvas.create_window(350, 60, window=self.label)

        self.select_button = tk.Button(master, text="Select Image", command=self.select_image, bg="blue", fg="white", font=("Times New Roman", 12, "bold"))
        self.canvas.create_window(350, 150, window=self.select_button)

        self.message_label = tk.Label(master, text="Enter Secret Message:", bg="lightblue", font=("Times New Roman", 12))
        self.canvas.create_window(350, 200, window=self.message_label)

        self.message_entry = tk.Entry(master, width=50, font=("Times New Roman", 12))
        self.canvas.create_window(350, 250, window=self.message_entry)

        self.passkey_label = tk.Label(master, text="Enter Passkey (Optional):", bg="lightblue", font=("Times New Roman", 12))
        self.canvas.create_window(350, 300, window=self.passkey_label)

        self.passkey_entry = tk.Entry(master, width=50, font=("Helvetica", 12))
        self.canvas.create_window(350, 350, window=self.passkey_entry)

        self.encrypt_button = tk.Button(master, text="Encrypt Message", command=self.encrypt, bg="green", fg="white", font=("Times New Roman", 12, "bold"))
        self.canvas.create_window(350, 400, window=self.encrypt_button)

        self.image_path = ""

    def select_image(self):
        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected!")

    def encrypt(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first!")
            return

        message = self.message_entry.get()
        if not message:
            messagebox.showwarning("Warning", "Please enter a secret message!")
            return

        passkey = self.passkey_entry.get()
        if passkey:
            message = passkey + message

        encrypted_image_path = self.encrypt_image(self.image_path, message)
        if encrypted_image_path:
            messagebox.showinfo("Success", f"Image encrypted and saved as {encrypted_image_path}")

    def encrypt_image(self, image_path, message):
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Failed to read the image.")
            return None

        message += chr(0)  # Null character to indicate the end of the message
        message_length = len(message)

        index = 0
        for row in img:
            for pixel in row:
                if index < message_length:
                    pixel[0] = ord(message[index])  # Store character's ASCII value in the red channel
                    index += 1
                if index >= message_length:
                    break
            if index >= message_length:
                break

        encrypted_image_path = "encryptedImage.png"
        cv2.imwrite(encrypted_image_path, img)
        return encrypted_image_path

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyEncryptor(root)
    root.mainloop()
