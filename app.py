import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import zipfile
import threading
import shutil

class ZipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Zipper & Unzipper")
        self.root.geometry("600x450")
        self.root.minsize(550, 400)

        # Apply a modern theme
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Create the main notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # Create the frames for each tab
        self.zip_frame = ttk.Frame(self.notebook, padding="10")
        self.unzip_frame = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.zip_frame, text="Compress (Zip)")
        self.notebook.add(self.unzip_frame, text="Extract (Unzip)")

        # Build the content of each tab
        self.create_zip_widgets()
        self.create_unzip_widgets()

    # --- ZIP TAB WIDGETS (No changes here) ---
    def create_zip_widgets(self):
        # Frame for the list of files
        list_frame = ttk.LabelFrame(self.zip_frame, text="Files and Folders to Zip")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Listbox to show files to be zipped
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill="both", expand=True, pady=5, padx=5)

        # Scrollbar for the listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame for action buttons
        button_frame = ttk.Frame(self.zip_frame)
        button_frame.pack(fill="x", pady=5)

        # Buttons
        ttk.Button(button_frame, text="Add File(s)", command=self.add_files).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_list).pack(side=tk.LEFT, expand=True, padx=5)

        # Main "ZIP FILES" button
        ttk.Button(self.zip_frame, text="ZIP FILES", command=self.zip_action, style='Accent.TButton').pack(fill="x", pady=10, padx=5)

        # Status bar
        self.zip_status = tk.StringVar()
        ttk.Label(self.zip_frame, textvariable=self.zip_status).pack(fill="x", side="bottom", padx=5)
        
        # Style for the accent button
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))

    # --- UNZIP TAB WIDGETS (No changes here) ---
    def create_unzip_widgets(self):
        # Frame for selecting the zip file
        source_frame = ttk.LabelFrame(self.unzip_frame, text="Select Zip File")
        source_frame.pack(fill="x", padx=5, pady=5)

        self.zip_file_path = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.zip_file_path, state="readonly").pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
        ttk.Button(source_frame, text="Browse...", command=self.browse_zip_file).pack(side=tk.RIGHT, padx=5)

        # Frame for selecting the destination
        dest_frame = ttk.LabelFrame(self.unzip_frame, text="Select Destination Folder")
        dest_frame.pack(fill="x", padx=5, pady=10)

        self.dest_path = tk.StringVar()
        ttk.Entry(dest_frame, textvariable=self.dest_path, state="readonly").pack(side=tk.LEFT, fill="x", expand=True, padx=5, pady=5)
        ttk.Button(dest_frame, text="Browse...", command=self.browse_destination).pack(side=tk.RIGHT, padx=5)
        
        # Main "UNZIP FILE" button
        ttk.Button(self.unzip_frame, text="UNZIP FILE", command=self.unzip_action, style='Accent.TButton').pack(fill="x", pady=20, padx=5)

        # Status bar
        self.unzip_status = tk.StringVar()
        ttk.Label(self.unzip_frame, textvariable=self.unzip_status).pack(fill="x", side="bottom", padx=5)


    # --- ZIP TAB FUNCTIONS (No changes here) ---
    def add_files(self):
        files = filedialog.askopenfilenames(title="Select files")
        if files:
            for file in files:
                self.file_listbox.insert(tk.END, file)
            self.zip_status.set(f"Added {len(files)} file(s).")

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select a folder")
        if folder:
            self.file_listbox.insert(tk.END, folder)
            self.zip_status.set(f"Added folder: {os.path.basename(folder)}")

    def remove_selected(self):
        selected_indices = self.file_listbox.curselection()
        for i in reversed(selected_indices):
            self.file_listbox.delete(i)
        self.zip_status.set("Removed selected item(s).")

    def clear_list(self):
        self.file_listbox.delete(0, tk.END)
        self.zip_status.set("List cleared.")

    def zip_action(self):
        items_to_zip = self.file_listbox.get(0, tk.END)
        if not items_to_zip:
            messagebox.showwarning("Warning", "No files or folders selected to zip.")
            return

        zip_save_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("Zip files", "*.zip")],
            title="Save Zip File As"
        )
        if not zip_save_path:
            self.zip_status.set("Zip operation cancelled.")
            return

        thread = threading.Thread(target=self._perform_zip, args=(items_to_zip, zip_save_path))
        thread.start()

    def _perform_zip(self, items, save_path):
        self.zip_status.set("Zipping... Please wait.")
        try:
            with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for item in items:
                    if os.path.isfile(item):
                        zipf.write(item, os.path.basename(item))
                    elif os.path.isdir(item):
                        base_dir = os.path.basename(item)
                        for root, dirs, files in os.walk(item):
                            for file in files:
                                file_path = os.path.join(root, file)
                                archive_name = os.path.join(base_dir, os.path.relpath(file_path, item))
                                zipf.write(file_path, archive_name)
            
            self.zip_status.set(f"Successfully created: {os.path.basename(save_path)}")
            messagebox.showinfo("Success", "Files have been zipped successfully!")
        except Exception as e:
            self.zip_status.set(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")


    # --- UNZIP TAB FUNCTIONS (Changes are in _perform_unzip) ---
    def browse_zip_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a Zip File",
            filetypes=[("Zip files", "*.zip")]
        )
        if filepath:
            self.zip_file_path.set(filepath)
            self.unzip_status.set(f"Selected: {os.path.basename(filepath)}")

    def browse_destination(self):
        dirpath = filedialog.askdirectory(title="Select Destination Folder")
        if dirpath:
            self.dest_path.set(dirpath)
            self.unzip_status.set(f"Destination: {dirpath}")
            
    def unzip_action(self):
        zip_path = self.zip_file_path.get()
        dest_path = self.dest_path.get()

        if not zip_path:
            messagebox.showwarning("Warning", "Please select a zip file to extract.")
            return
        if not dest_path:
            messagebox.showwarning("Warning", "Please select a destination folder.")
            return
        
        thread = threading.Thread(target=self._perform_unzip, args=(zip_path, dest_path))
        thread.start()

    # ===================================================================
    # === MODIFIED SECTION: This function handles the safe extraction ===
    # ===================================================================
    def _perform_unzip(self, zip_path, dest_path):
        self.unzip_status.set("Extracting... Please wait.")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                # Get a list of all items in the zip file
                members = zipf.infolist()
                
                for member in members:
                    # Construct the full target path
                    target_path = os.path.join(dest_path, member.filename)
                    
                    # If the member is a directory, create it and continue
                    if member.is_dir():
                        os.makedirs(target_path, exist_ok=True)
                        continue

                    # If the file already exists, find a new name
                    if os.path.exists(target_path):
                        # Split the path into base and extension
                        base, ext = os.path.splitext(target_path)
                        counter = 1
                        # Loop until we find a name that doesn't exist
                        while True:
                            new_path = f"{base} ({counter}){ext}"
                            if not os.path.exists(new_path):
                                target_path = new_path
                                break
                            counter += 1
                    
                    # Ensure the directory for the file exists before writing
                    target_dir = os.path.dirname(target_path)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir, exist_ok=True)

                    # Extract the file by reading from zip and writing to disk
                    # This is more robust than extract() as it allows renaming.
                    with zipf.open(member, 'r') as source_file:
                        with open(target_path, "wb") as target_file:
                            shutil.copyfileobj(source_file, target_file)

            self.unzip_status.set(f"Successfully extracted to: {dest_path}")
            messagebox.showinfo("Success", "File has been unzipped successfully!")

        except zipfile.BadZipFile:
            self.unzip_status.set("Error: The file is not a valid zip file.")
            messagebox.showerror("Error", "The selected file is not a valid zip archive.")
        except Exception as e:
            self.unzip_status.set(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

# --- Main application entry point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ZipperApp(root)
    root.mainloop()