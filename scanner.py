import cv2
from pyzbar.pyzbar import decode
import pyperclip
import threading
import tkinter as tk
from tkinter import messagebox

class BarcodeScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcode Scanner")
        self.root.geometry("400x200")
        
        self.result_label = tk.Label(root, text="Scanned Result:")
        self.result_label.pack(pady=10)

        self.result_text = tk.Text(root, height=2, width=40)
        self.result_text.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Scanning", command=self.start_scanning)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_scanning, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.scanning = False

    def start_scanning(self):
        self.scanning = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.scan_barcode).start()

    def stop_scanning(self):
        self.scanning = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def scan_barcode(self):
        cap = cv2.VideoCapture(0)
        while self.scanning:
            ret, frame = cap.read()
            if not ret:
                continue

            barcodes = decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                pyperclip.copy(barcode_data)
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, barcode_data)
                self.scanning = False
                break

            cv2.imshow("Barcode Scanner - Press Q to Close", frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or not self.scanning:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = BarcodeScannerApp(root)
    root.mainloop()
