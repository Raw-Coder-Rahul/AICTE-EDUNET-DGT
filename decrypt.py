import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SteganographyDecryptor:
    def __init__(self, master):
        self.master = master
        master.title("Image Decryption Tool")
        master.geometry("700x600")

        self.canvas = tk.Canvas(master, width=700, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Load and resize the background image to fit the canvas
        original_image = Image.open("images/blue black.jpg")
        resized_image = original_image.resize((700, 600), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.label = tk.Label(master, text="Steganography Image Decryption", bg="lightblue", font=("Times New Roman", 16, "bold"))
        self.canvas.create_window(350, 60, window=self.label)

        self.select_button = tk.Button(master, text="Select Encrypted Image", command=self.select_image, bg="blue", fg="white", font=("Times New Roman", 12, "bold"))
        self.canvas.create_window(350, 150, window=self.select_button)

        self.passkey_label = tk.Label(master, text="Enter Passkey (Optional):", bg="lightblue", font=("Times New Roman", 12))
        self.canvas.create_window(350, 200, window=self.passkey_label)

        self.passkey_entry = tk.Entry(master, width=50, font=("Times New Roman", 12))
        self.canvas.create_window(350, 250, window=self.passkey_entry)

        self.decrypt_button = tk.Button(master, text="Decrypt Message", command=self.decrypt, bg="green", fg="white", font=("Times New Roman", 12, "bold"))
        self.canvas.create_window(350, 300, window=self.decrypt_button)

        self.image_path = ""

    def select_image(self):
        self.image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if not self.image_path:
            messagebox.showwarning("Warning", "No image selected!")

    def decrypt(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first!")
            return

        passkey = self.passkey_entry.get()
        secret_message = self.decrypt_image(self.image_path, passkey)
        if secret_message is not None:
            if passkey and not secret_message.startswith(passkey):
                messagebox.showwarning("Warning", "Passkey does not match!")
            else:
                if passkey:
                    secret_message = secret_message[len(passkey):]  # Remove passkey from the message
                messagebox.showinfo("Decrypted Message", f"The hidden message is: {secret_message}")
        else:
            messagebox.showerror("Error", "Failed to decrypt the message.")

    def decrypt_image(self, image_path, passkey):
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Failed to read the image.")
            return None

        message = ""
        for row in img:
            for pixel in row:
                char = chr(pixel[0])  # Retrieve character's ASCII value from the red channel
                if char == chr(0):  # Null character indicates the end of the message
                    return message
                message += char

        return message

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyDecryptor(root)
    root.mainloop()
