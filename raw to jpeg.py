import os
import rawpy
import imageio
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class RAWtoJPEGConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("RAW to JPEG Converter")
        self.root.geometry("500x250")
        
        self.input_folder = tk.StringVar(value="No folder selected")
        self.output_folder = tk.StringVar(value="No folder selected")
        
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Input Folder", command=self.select_input_folder)
        file_menu.add_command(label="Select Output Folder", command=self.select_output_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Input Folder:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(main_frame, textvariable=self.input_folder, foreground="blue").grid(row=0, column=1, sticky=tk.W)
        ttk.Button(main_frame, text="Browse...", command=self.select_input_folder).grid(row=0, column=2, padx=5)
        
        ttk.Label(main_frame, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, pady=10)
        ttk.Label(main_frame, textvariable=self.output_folder, foreground="blue").grid(row=1, column=1, sticky=tk.W)
        ttk.Button(main_frame, text="Browse...", command=self.select_output_folder).grid(row=1, column=2, padx=5)
        
        ttk.Label(main_frame, text="Status:").grid(row=2, column=0, sticky=tk.W, pady=10)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="green")
        self.status_label.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        
        convert_button = ttk.Button(main_frame, text="Convert RAW to JPEG", command=self.convert)
        convert_button.grid(row=3, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
    
    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder (contains RAW files)")
        if folder:
            self.input_folder.set(folder)
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder (for JPEG files)")
        if folder:
            self.output_folder.set(folder)
    
    def convert(self):
        input_path = self.input_folder.get()
        output_path = self.output_folder.get()
        
        if input_path == "No folder selected" or output_path == "No folder selected":
            messagebox.showerror("Error", "Please select both input and output folders")
            return
        
        try:
            self.status_var.set("Converting...")
            self.root.update()
            
            convert_raw_to_jpeg(input_path, output_path)
            
            self.status_var.set("Conversion completed!")
            messagebox.showinfo("Success", "RAW to JPEG conversion completed successfully!")
        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def convert_raw_to_jpeg(raw_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    raw_files = [f for f in os.listdir(raw_folder) if any(f.lower().endswith(ext) for ext in ['.arw', '.cr2', '.dng', '.nef', '.raw', '.rw2', '.orf', '.raf'])]

    for raw_file in raw_files:
        raw_path = os.path.join(raw_folder, raw_file)

        output_path = os.path.join(output_folder, os.path.splitext(raw_file)[0] + '.jpg')

        convert_raw_to_jpeg_single(raw_path, output_path)

def convert_raw_to_jpeg_single(raw_path, output_path):
    try:
        with rawpy.imread(raw_path) as raw:
            rgb = raw.postprocess()

            imageio.imsave(output_path, rgb)

            print(f'Converted {raw_path} to {output_path}')

    except Exception as e:
        print(f'Error converting {raw_path}: {e}')


root = tk.Tk()
app = RAWtoJPEGConverter(root)
root.mainloop()
