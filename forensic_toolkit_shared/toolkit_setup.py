import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

def install_dependencies():
    """Install required dependencies"""
    try:
        # Update package lists
        subprocess.run(["sudo", "apt", "update"], check=True)
        
        # Install Python packages
        subprocess.run(["sudo", "apt", "install", "-y", "python3-tk", "python3-pip"], check=True)
        
        # Install forensic tools
        subprocess.run(["sudo", "apt", "install", "-y", "testdisk", "john", "guymager", 
                        "sleuthkit", "autopsy", "wireshark"], check=True)
        
        # Install Rekall
        subprocess.run(["sudo", "pip3", "install", "rekall"], check=True)
        
        # Install StegExpose
        home_dir = os.path.expanduser("~")
        stegexpose_dir = os.path.join(home_dir, "StegExpose")
        
        if not os.path.exists(stegexpose_dir):
            subprocess.run(
                ["git", "clone", "https://github.com/b3dk7/StegExpose.git", stegexpose_dir],
                check=True
            )
            subprocess.run(
                ["chmod", "+x", os.path.join(stegexpose_dir, "StegExpose.jar")],
                check=True
            )
        
        return True
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_desktop_shortcut(install_dir):
    """Create desktop shortcut"""
    try:
        home_dir = os.path.expanduser("~")
        desktop_file = os.path.join(home_dir, "Desktop", "forensic-toolkit.desktop")
        
        with open(desktop_file, "w") as f:
            f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Digital Forensic Toolkit
Comment=Launch the Digital Forensic Toolkit
Exec=python3 {os.path.join(install_dir, "forensic_toolkit.py")}
Icon=utilities-terminal
Terminal=false
Categories=Utility;
""")
        
        os.chmod(desktop_file, 0o755)
        return True
    except Exception as e:
        print(f"Error creating desktop shortcut: {e}")
        return False

def copy_toolkit(install_dir):
    """Copy toolkit files to installation directory"""
    try:
        # Create installation directory
        os.makedirs(install_dir, exist_ok=True)
        
        # Copy toolkit file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        toolkit_path = os.path.join(script_dir, "forensic_toolkit.py")
        
        if os.path.exists(toolkit_path):
            import shutil
            shutil.copy2(toolkit_path, install_dir)
            return True
        else:
            print("Error: forensic_toolkit.py not found")
            return False
    except Exception as e:
        print(f"Error copying toolkit: {e}")
        return False

def main():
    # Create GUI
    root = tk.Tk()
    root.title("Digital Forensic Toolkit Setup")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")
    
    # Header
    header = tk.Label(
        root, 
        text="Digital Forensic Toolkit - Setup",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0",
        pady=20
    )
    header.pack()
    
    # Description
    description = tk.Label(
        root,
        text="This setup will install the Digital Forensic Toolkit\n"
             "and all required dependencies.",
        font=("Arial", 12),
        bg="#f0f0f0",
        pady=10
    )
    description.pack()
    
    # Installation directory
    dir_frame = tk.Frame(root, bg="#f0f0f0")
    dir_frame.pack(pady=10)
    
    dir_label = tk.Label(
        dir_frame,
        text="Installation Directory:",
        font=("Arial", 11),
        bg="#f0f0f0"
    )
    dir_label.pack(side="left", padx=5)
    
    home_dir = os.path.expanduser("~")
    default_install_dir = os.path.join(home_dir, "DigitalForensicToolkit")
    
    dir_var = tk.StringVar(value=default_install_dir)
    dir_entry = tk.Entry(
        dir_frame,
        textvariable=dir_var,
        width=30,
        font=("Arial", 11)
    )
    dir_entry.pack(side="left", padx=5)
    
    # Status text
    status_var = tk.StringVar(value="Ready to install")
    status_label = tk.Label(
        root,
        textvariable=status_var,
        font=("Arial", 11, "italic"),
        bg="#f0f0f0",
        fg="#555555",
        pady=10
    )
    status_label.pack()
    
    # Progress
    progress_frame = tk.Frame(root, bg="#f0f0f0")
    progress_frame.pack(pady=10, fill="x", padx=50)
    
    progress_var = tk.IntVar(value=0)
    progress_bar = tk.Canvas(
        progress_frame,
        width=400,
        height=20,
        bg="white",
        highlightthickness=1,
        highlightbackground="#cccccc"
    )
    progress_bar.pack()
    
    # Draw initial progress bar
    progress_bar.create_rectangle(0, 0, 0, 20, fill="#4CAF50", width=0, tags="progress")
    
    def update_progress(value):
        progress_var.set(value)
        progress_bar.delete("progress")
        width = 400 * (value / 100)
        progress_bar.create_rectangle(0, 0, width, 20, fill="#4CAF50", width=0, tags="progress")
        root.update()
    
    # Install button
    def install():
        install_dir = dir_var.get()
        
        # Update status
        status_var.set("Installing...")
        update_progress(10)
        
        # Copy toolkit files
        status_var.set("Copying toolkit files...")
        if not copy_toolkit(install_dir):
            messagebox.showerror("Error", "Failed to copy toolkit files")
            status_var.set("Installation failed")
            return
        update_progress(30)
        
        # Install dependencies
        status_var.set("Installing dependencies (this may take a while)...")
        if not install_dependencies():
            messagebox.showerror("Error", "Failed to install dependencies")
            status_var.set("Installation failed")
            return
        update_progress(80)
        
        # Create desktop shortcut
        status_var.set("Creating desktop shortcut...")
        if not create_desktop_shortcut(install_dir):
            messagebox.showerror("Warning", "Failed to create desktop shortcut")
        update_progress(90)
        
        # Finish
        update_progress(100)
        status_var.set("Installation complete!")
        
        messagebox.showinfo(
            "Installation Complete",
            f"The Digital Forensic Toolkit has been installed to:\n{install_dir}\n\n"
            f"A desktop shortcut has been created.\n\n"
            f"To run the toolkit:\n"
            f"1. Double-click the desktop shortcut, or\n"
            f"2. Run: python3 {os.path.join(install_dir, 'forensic_toolkit.py')}"
        )
        
        root.destroy()
    
    install_button = tk.Button(
        root,
        text="Install",
        command=install,
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=5
    )
    install_button.pack(pady=20)
    
    # Cancel button
    cancel_button = tk.Button(
        root,
        text="Cancel",
        command=root.destroy,
        font=("Arial", 11),
        bg="#f0f0f0",
        padx=10
    )
    cancel_button.pack()
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()

