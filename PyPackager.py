import customtkinter as ctk
from tkinter import filedialog, Listbox, END, ANCHOR
import subprocess
import threading
import os
import sys

# --- Constants ---
APP_NAME = "PyPackager"
APP_VERSION = "1.0"
WINDOW_SIZE = "800x750"

# --- Main Application Class ---
class PyPackagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title(f"{APP_NAME} - Your Python to EXE Converter")
        self.geometry(WINDOW_SIZE)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1) # Configure log output row to expand

        # --- Class Variables ---
        self.script_path = ctk.StringVar()
        self.icon_path = ctk.StringVar()
        self.output_dir = ctk.StringVar()
        self.one_file_var = ctk.BooleanVar(value=True)
        self.windowless_var = ctk.BooleanVar(value=True)
        self.final_dist_path = ""

        # --- Initialize UI ---
        self.create_widgets()

    def create_widgets(self):
        """Create and layout all the GUI widgets."""
        
        # --- File/Folder Selection Frame ---
        selection_frame = ctk.CTkFrame(self)
        selection_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        selection_frame.grid_columnconfigure(1, weight=1)

        # Python Script Selection
        ctk.CTkLabel(selection_frame, text="Python Script:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.script_entry = ctk.CTkEntry(selection_frame, textvariable=self.script_path, state="readonly")
        self.script_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(selection_frame, text="Browse...", command=self.select_script).grid(row=0, column=2, padx=10, pady=5)
        
        # Icon File Selection
        ctk.CTkLabel(selection_frame, text="Icon File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.icon_entry = ctk.CTkEntry(selection_frame, textvariable=self.icon_path, state="readonly")
        self.icon_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(selection_frame, text="Browse...", command=self.select_icon).grid(row=1, column=2, padx=10, pady=5)
        
        # Output Directory Selection
        ctk.CTkLabel(selection_frame, text="Output Folder:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.output_entry = ctk.CTkEntry(selection_frame, textvariable=self.output_dir, state="readonly")
        self.output_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(selection_frame, text="Browse...", command=self.select_output_dir).grid(row=2, column=2, padx=10, pady=5)

        # --- Build Options Frame ---
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        
        self.onefile_checkbox = ctk.CTkCheckBox(options_frame, text="Create one single file (--onefile)", variable=self.one_file_var)
        self.onefile_checkbox.pack(side="left", padx=10, pady=10)
        
        self.noconsole_checkbox = ctk.CTkCheckBox(options_frame, text="Windowless (for GUI Apps) (--noconsole)", variable=self.windowless_var)
        self.noconsole_checkbox.pack(side="left", padx=10, pady=10)

        # --- Data Files Frame ---
        data_frame = ctk.CTkFrame(self)
        data_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(data_frame, text="Add Extra Data Files/Folders:").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Using a standard tkinter Listbox as it's more suited for this than a CTk widget
        self.data_listbox = Listbox(data_frame, bg="#2e2e2e", fg="white", selectbackground="#1f6aa5", relief="sunken", borderwidth=1)
        self.data_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        data_buttons_frame = ctk.CTkFrame(data_frame)
        data_buttons_frame.grid(row=1, column=1, padx=10, pady=5, sticky="ns")
        ctk.CTkButton(data_buttons_frame, text="Add File", command=self.add_data_file).pack(pady=5, padx=5, fill="x")
        ctk.CTkButton(data_buttons_frame, text="Add Folder", command=self.add_data_folder).pack(pady=5, padx=5, fill="x")
        ctk.CTkButton(data_buttons_frame, text="Remove", command=self.remove_data_item).pack(pady=5, padx=5, fill="x")

        # --- Build Button ---
        self.build_button = ctk.CTkButton(self, text="BUILD EXE", font=("", 16, "bold"), command=self.start_build_thread)
        self.build_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, ipady=10, sticky="ew")

        # --- Output Log Frame ---
        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(log_frame, text="Output Log:").pack(side="left", padx=10)
        ctk.CTkButton(log_frame, text="Clear Log", command=self.clear_log).pack(side="right", padx=10)

        self.log_textbox = ctk.CTkTextbox(self, state="disabled", wrap="word")
        self.log_textbox.grid(row=6, column=0, columnspan=3, padx=10, pady=(0,10), sticky="nsew")

        # --- Status Bar ---
        self.status_frame = ctk.CTkFrame(self, height=30)
        self.status_frame.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.status_label = ctk.CTkLabel(self.status_frame, text="Status: Idle")
        self.status_label.pack(side="left", padx=10)
        self.open_folder_button = ctk.CTkButton(self.status_frame, text="Open Output Folder", command=self.open_output_folder, state="disabled")
        self.open_folder_button.pack(side="right", padx=10)
        
    # --- Callback Functions ---
    def select_script(self):
        path = filedialog.askopenfilename(title="Select Python Script", filetypes=[("Python files", "*.py *.pyw")])
        if path:
            self.script_path.set(path)

    def select_icon(self):
        path = filedialog.askopenfilename(title="Select Icon File", filetypes=[("Icon files", "*.ico")])
        if path:
            self.icon_path.set(path)

    def select_output_dir(self):
        path = filedialog.askdirectory(title="Select Output Folder")
        if path:
            self.output_dir.set(path)

    def add_data_file(self):
        path = filedialog.askopenfilename(title="Select Data File")
        if path:
            self.data_listbox.insert(END, path)

    def add_data_folder(self):
        path = filedialog.askdirectory(title="Select Data Folder")
        if path:
            self.data_listbox.insert(END, path)

    def remove_data_item(self):
        try:
            self.data_listbox.delete(ANCHOR)
        except:
            pass # Ignore if nothing is selected

    def clear_log(self):
        self.log_textbox.configure(state="normal")
        self.log_textbox.delete("1.0", END)
        self.log_textbox.configure(state="disabled")

    def open_output_folder(self):
        if os.path.exists(self.final_dist_path):
            if sys.platform == "win32":
                os.startfile(self.final_dist_path)
            elif sys.platform == "darwin": # macOS
                subprocess.run(["open", self.final_dist_path])
            else: # linux
                subprocess.run(["xdg-open", self.final_dist_path])

    def start_build_thread(self):
        """Starts the PyInstaller build process in a separate thread to keep the GUI responsive."""
        if not self.script_path.get():
            self.update_status("Error: No Python script selected!", "red")
            return
        
        self.toggle_ui_state("disabled")
        self.update_status("Building...", "orange")
        self.clear_log()
        
        # Run the build process in a separate thread
        build_thread = threading.Thread(target=self.run_pyinstaller)
        build_thread.daemon = True
        build_thread.start()

    def run_pyinstaller(self):
        """Constructs and runs the PyInstaller command."""
        script = self.script_path.get()
        command = [
            "pyinstaller",
            "--noconfirm", # Overwrite output directory without asking
            script
        ]

        # Add basic options
        if self.one_file_var.get():
            command.append("--onefile")
        if self.windowless_var.get():
            command.append("--windowed") # --noconsole is an alias

        # Add icon if specified
        if self.icon_path.get():
            command.extend(["--icon", self.icon_path.get()])

        # Add data files/folders
        # PyInstaller format: --add-data "source;destination" (Win) or "source:destination" (Mac/Linux)
        # We'll use '.' as the destination to place files in the root of the bundle.
        separator = os.pathsep 
        for item in self.data_listbox.get(0, END):
            # Get the base name of the file/folder to create its destination path
            dest_folder = os.path.basename(item)
            command.extend(["--add-data", f"{item}{separator}{dest_folder}"])
            
        # Handle output directory
        output_path = self.output_dir.get()
        if output_path:
            self.final_dist_path = os.path.join(output_path, "dist")
            build_path = os.path.join(output_path, "build")
            command.extend(["--distpath", self.final_dist_path])
            command.extend(["--workpath", build_path])
        else:
            # Default location is a 'dist' folder in the script's directory
            self.final_dist_path = os.path.join(os.path.dirname(script), "dist")

        # --- Execute the command ---
        self.log_message(f"Running command: {' '.join(command)}\n" + "-"*50)
        
        # Use Popen to capture real-time output
        try:
            # On Windows, prevent the console window from appearing
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                encoding='utf-8',
                startupinfo=startupinfo
            )
            
            # Read and display output line by line
            for line in iter(process.stdout.readline, ''):
                self.log_message(line)
            
            process.stdout.close()
            return_code = process.wait()

            if return_code == 0:
                self.after(0, self.build_finished, True)
            else:
                self.after(0, self.build_finished, False, f"PyInstaller exited with error code {return_code}.")
                
        except FileNotFoundError:
             self.after(0, self.build_finished, False, "Error: 'pyinstaller' command not found. Is it installed and in your system's PATH?")
        except Exception as e:
            self.after(0, self.build_finished, False, f"An unexpected error occurred: {e}")

    def build_finished(self, success, message=None):
        """Called on the main thread when the build is complete."""
        if success:
            self.update_status("Success!", "green")
            self.open_folder_button.configure(state="normal")
            self.log_message("\n" + "-"*50 + "\nBuild completed successfully.")
        else:
            self.update_status("Error!", "red")
            error_msg = message or "Build failed. Check the log for details."
            self.log_message("\n" + "-"*50 + f"\n{error_msg}")
        
        self.toggle_ui_state("normal")

    # --- Thread-safe GUI update methods ---
    def log_message(self, msg):
        """Safely append a message to the log textbox from any thread."""
        self.after(0, self._append_to_log, msg)

    def _append_to_log(self, msg):
        """The actual log update, run on the main GUI thread."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert(END, msg)
        self.log_textbox.see(END) # Auto-scroll
        self.log_textbox.configure(state="disabled")

    def update_status(self, text, color="white"):
        """Update the status label text and color."""
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def toggle_ui_state(self, state="normal"):
        """Enable or disable interactive widgets to prevent conflicts during a build."""
        self.build_button.configure(state=state)
        self.script_entry.configure(state="readonly" if state=="normal" else "disabled")
        self.icon_entry.configure(state="readonly" if state=="normal" else "disabled")
        self.output_entry.configure(state="readonly" if state=="normal" else "disabled")
        
        # Disable all browse/add/remove buttons
        for child in self.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                for btn in child.winfo_children():
                    if isinstance(btn, ctk.CTkButton) and btn != self.build_button:
                        btn.configure(state=state)
                # Handle nested frames (for data buttons)
                for sub_frame in child.winfo_children():
                    if isinstance(sub_frame, ctk.CTkFrame):
                        for btn in sub_frame.winfo_children():
                             if isinstance(btn, ctk.CTkButton):
                                 btn.configure(state=state)


        self.onefile_checkbox.configure(state=state)
        self.noconsole_checkbox.configure(state=state)
        self.data_listbox.configure(state=state)
        
        # Reset open folder button
        if state == "normal":
            self.open_folder_button.configure(state="disabled")

# --- Run the application ---
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark") # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"
    
    app = PyPackagerApp()
    app.mainloop()