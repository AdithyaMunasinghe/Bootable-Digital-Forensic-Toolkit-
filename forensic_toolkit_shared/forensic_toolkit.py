#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import time
import logging
import datetime
import json
import platform
import shutil
import queue

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='forensic_toolkit.log'
)
logger = logging.getLogger('ForensicToolkit')

class ForensicToolkit(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.title("Digital Forensic Toolkit")
        self.geometry("950x700")
        self.minsize(900, 650)
        
        # Set color scheme
        self.colors = {
            "primary_dark": "#1e3a5f",    # Dark blue
            "primary": "#2c5282",         # Medium blue
            "primary_light": "#3182ce",   # Light blue
            "secondary": "#38b2ac",       # Teal
            "accent": "#ed8936",          # Orange
            "success": "#48bb78",         # Green
            "warning": "#ecc94b",         # Yellow
            "danger": "#e53e3e",          # Red
            "background_dark": "#2d3748", # Dark gray
            "background": "#f7fafc",      # Light gray
            "text_light": "#ffffff",      # White
            "text_dark": "#1a202c"        # Dark gray
        }
        
        # Icons (Unicode)
        self.icons = {
            "home": "🏠",
            "dashboard": "📊",
            "functions": "🧰",
            "installation": "🔧",
            "reports": "📝",
            "about": "ℹ️",
            "photo_recovery": "🔍",
            "password_cracking": "🔑",
            "disk_imaging": "💾",
            "memory_analysis": "🧠",
            "file_system": "📁",
            "network": "🌐",
            "steganography": "🕵️",
            "refresh": "🔄",
            "settings": "⚙️",
            "check": "✅",
            "warning": "⚠️",
            "error": "❌",
            "info": "ℹ️",
            "device": "💻",
            "search": "🔎",
            "save": "💾",
            "delete": "🗑️",
            "export": "📤",
            "import": "📥"
        }
        
        # Configure the style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabel", background=self.colors["background"], foreground=self.colors["text_dark"])
        self.style.configure("TButton", background=self.colors["primary"], foreground=self.colors["text_light"])
        
        # Configure notebook style
        self.style.configure("TNotebook", background=self.colors["background"])
        self.style.configure("TNotebook.Tab", background=self.colors["primary_dark"], 
                            foreground=self.colors["text_light"], padding=[15, 5])
        self.style.map("TNotebook.Tab", 
                      background=[("selected", self.colors["primary"])],
                      foreground=[("selected", self.colors["text_light"])])
        
        # Configure header style
        self.style.configure("Header.TLabel", 
                            font=("Arial", 24, "bold"), 
                            foreground=self.colors["primary"],
                            background=self.colors["background"])
        
        # Configure function button style
        self.style.configure("Function.TButton", 
                            font=("Arial", 12), 
                            background=self.colors["primary"],
                            foreground=self.colors["text_light"])
        
        # Configure success button style
        self.style.configure("Success.TButton", 
                            background=self.colors["success"],
                            foreground=self.colors["text_light"])
        
        # Configure warning button style
        self.style.configure("Warning.TButton", 
                            background=self.colors["warning"],
                            foreground=self.colors["text_dark"])
        
        # Configure accent button style
        self.style.configure("Accent.TButton", 
                            background=self.colors["accent"],
                            foreground=self.colors["text_light"])
        
        # Set background color
        self.configure(background=self.colors["background"])
        
        # Variables
        self.selected_device = tk.StringVar()
        self.devices = self.get_connected_devices()
        self.recent_activities = self.load_recent_activities()
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.home_frame = ttk.Frame(self.notebook)
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.functions_frame = ttk.Frame(self.notebook)
        self.installation_frame = ttk.Frame(self.notebook)
        self.reports_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.home_frame, text=f"{self.icons['home']} Home")
        self.notebook.add(self.dashboard_frame, text=f"{self.icons['dashboard']} Dashboard")
        self.notebook.add(self.functions_frame, text=f"{self.icons['functions']} Functions")
        self.notebook.add(self.installation_frame, text=f"{self.icons['installation']} Installation")
        self.notebook.add(self.reports_frame, text=f"{self.icons['reports']} Reports")
        self.notebook.add(self.about_frame, text=f"{self.icons['about']} About")
        
        # Create status bar first (before initializing tabs)
        self.status_bar = tk.Frame(self, bg=self.colors["primary_dark"], height=25)
        self.status_bar.pack(side="bottom", fill="x")
        
        self.status_text = tk.Label(
            self.status_bar, 
            text="Ready", 
            fg=self.colors["text_light"],
            bg=self.colors["primary_dark"],
            anchor="w",
            padx=10
        )
        self.status_text.pack(side="left")
        
        self.version_label = tk.Label(
            self.status_bar, 
            text="v1.1.0", 
            fg=self.colors["text_light"],
            bg=self.colors["primary_dark"],
            anchor="e",
            padx=10
        )
        self.version_label.pack(side="right")
        
        # Initialize tabs
        self.init_home_tab()
        self.init_dashboard_tab()
        self.init_functions_tab()
        self.init_installation_tab()
        self.init_reports_tab()
        self.init_about_tab()
        
        # Update device list AFTER creating status bar
        self.update_device_list()
        
        # Start device monitoring thread
        self.stop_monitoring = False
        self.monitor_thread = threading.Thread(target=self.monitor_devices)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def init_home_tab(self):
        # Create a banner frame
        banner_frame = tk.Frame(self.home_frame, bg=self.colors["primary_dark"], height=120)
        banner_frame.pack(fill="x", pady=0)
        
        # Add logo text to the banner
        logo_label = tk.Label(
            banner_frame, 
            text="🔍 Digital Forensic Toolkit", 
            font=("Arial", 28, "bold"),
            fg=self.colors["text_light"],
            bg=self.colors["primary_dark"],
            pady=30
        )
        logo_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.home_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_frame = tk.Frame(content_frame, bg=self.colors["primary_light"], padx=20, pady=20)
        welcome_frame.pack(fill="x", pady=10)
        
        welcome_label = tk.Label(
            welcome_frame,
            text="Welcome to the Digital Forensic Toolkit!",
            font=("Arial", 16, "bold"),
            fg=self.colors["text_light"],
            bg=self.colors["primary_light"]
        )
        welcome_label.pack(anchor="w")
        
        description = """
This toolkit provides automated access to various forensic tools
to help you analyze digital evidence efficiently.

To get started:
1. Connect a USB drive or external hard disk
2. Select the device from the dropdown below
3. Choose the forensic function you want to perform

All results will be saved in the 'forensic_results' directory.
        """
        
        desc_label = tk.Label(
            welcome_frame, 
            text=description, 
            font=("Arial", 12),
            justify="left",
            bg=self.colors["primary_light"],
            fg=self.colors["text_light"],
            padx=10,
            pady=10
        )
        desc_label.pack(anchor="w")
        
        # Device selection frame
        device_frame = tk.LabelFrame(
            content_frame, 
            text=" Connected Devices ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        device_frame.pack(fill="x", pady=15)
        
        device_icon_label = tk.Label(
            device_frame,
            text=self.icons["device"],
            font=("Arial", 16),
            bg=self.colors["background"],
            fg=self.colors["primary"]
        )
        device_icon_label.pack(side="left", padx=5)
        
        tk.Label(
            device_frame, 
            text="Select Device:", 
            bg=self.colors["background"],
            fg=self.colors["text_dark"],
            font=("Arial", 11)
        ).pack(side="left", padx=5, pady=10)
        
        self.device_dropdown = ttk.Combobox(
            device_frame, 
            textvariable=self.selected_device,
            state="readonly",
            width=40,
            font=("Arial", 11)
        )
        self.device_dropdown.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        refresh_button = tk.Button(
            device_frame, 
            text=f"{self.icons['refresh']} Refresh", 
            command=self.update_device_list,
            bg=self.colors["secondary"],
            fg=self.colors["text_light"],
            font=("Arial", 11),
            padx=10
        )
        refresh_button.pack(side="left", padx=10, pady=10)
        
        # Quick access buttons
        button_frame = tk.LabelFrame(
            content_frame, 
            text=" Quick Access ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        button_frame.pack(fill="x", pady=15)
        
        # Create a grid for quick access buttons
        functions_grid = tk.Frame(button_frame, bg=self.colors["background"])
        functions_grid.pack(fill="x", pady=10)
        
        quick_functions = [
            (f"{self.icons['photo_recovery']} Photo Recovery", self.run_photorec, self.colors["primary"]),
            (f"{self.icons['password_cracking']} Password Cracking", self.run_john, self.colors["accent"]),
            (f"{self.icons['disk_imaging']} Disk Imaging", self.run_guymager, self.colors["secondary"])
        ]
        
        for i, (text, command, color) in enumerate(quick_functions):
            btn = tk.Button(
                functions_grid, 
                text=text, 
                command=command, 
                bg=color,
                fg=self.colors["text_light"],
                font=("Arial", 12),
                width=20,
                height=2,
                relief="raised",
                bd=1
            )
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            functions_grid.columnconfigure(i, weight=1)
        
        # Help section
        help_frame = tk.Frame(content_frame, bg=self.colors["background"])
        help_frame.pack(fill="x", pady=10)
        
        help_label = tk.Label(
            help_frame,
            text=f"{self.icons['info']} Need help? Go to the About tab for more information.",
            font=("Arial", 11),
            bg=self.colors["background"],
            fg=self.colors["text_dark"]
        )
        help_label.pack(anchor="w", pady=5)
        
        about_button = tk.Button(
            help_frame, 
            text="About & Help", 
            command=lambda: self.notebook.select(5),
            bg=self.colors["primary_dark"],
            fg=self.colors["text_light"],
            font=("Arial", 11)
        )
        about_button.pack(side="left", pady=5)
    
    def init_dashboard_tab(self):
        # Create a banner frame
        banner_frame = tk.Frame(self.dashboard_frame, bg=self.colors["primary"], height=80)
        banner_frame.pack(fill="x", pady=0)
        
        # Add text to the banner
        banner_label = tk.Label(
            banner_frame, 
            text=f"{self.icons['dashboard']} Dashboard", 
            font=("Arial", 24, "bold"),
            fg=self.colors["text_light"],
            bg=self.colors["primary"],
            pady=20
        )
        banner_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.dashboard_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a grid layout for dashboard widgets
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        
        # System status widget
        system_frame = tk.LabelFrame(
            content_frame, 
            text=" System Status ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        system_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Get system info
        system_info = self.get_system_info()
        
        # Display system info
        for i, (key, value) in enumerate(system_info.items()):
            info_frame = tk.Frame(system_frame, bg=self.colors["background"])
            info_frame.pack(fill="x", pady=5)
            
            key_label = tk.Label(
                info_frame,
                text=f"{key}:",
                font=("Arial", 11, "bold"),
                bg=self.colors["background"],
                fg=self.colors["primary"],
                width=15,
                anchor="w"
            )
            key_label.pack(side="left", padx=5)
            
            value_label = tk.Label(
                info_frame,
                text=value,
                font=("Arial", 11),
                bg=self.colors["background"],
                fg=self.colors["text_dark"]
            )
            value_label.pack(side="left", padx=5)
        
        # Device status widget
        device_frame = tk.LabelFrame(
            content_frame, 
            text=" Device Status ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        device_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        device_label = tk.Label(
            device_frame,
            text="Selected Device:",
            font=("Arial", 11, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"]
        )
        device_label.pack(anchor="w", padx=5, pady=5)
        
        selected_device_label = tk.Label(
            device_frame,
            textvariable=self.selected_device,
            font=("Arial", 11),
            bg=self.colors["background"],
            fg=self.colors["text_dark"]
        )
        selected_device_label.pack(anchor="w", padx=5, pady=5)
        
        device_count_label = tk.Label(
            device_frame,
            text=f"Connected Devices: {len(self.devices)}",
            font=("Arial", 11),
            bg=self.colors["background"],
            fg=self.colors["text_dark"]
        )
        device_count_label.pack(anchor="w", padx=5, pady=5)
        
        refresh_button = tk.Button(
            device_frame, 
            text=f"{self.icons['refresh']} Refresh Devices", 
            command=self.update_device_list,
            bg=self.colors["secondary"],
            fg=self.colors["text_light"],
            font=("Arial", 11)
        )
        refresh_button.pack(anchor="w", padx=5, pady=10)
        
        # Recent activities widget
        activities_frame = tk.LabelFrame(
            content_frame, 
            text=" Recent Activities ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        activities_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Create a canvas with scrollbar for activities
        activities_canvas = tk.Canvas(activities_frame, bg=self.colors["background"], highlightthickness=0)
        activities_scrollbar = ttk.Scrollbar(activities_frame, orient="vertical", command=activities_canvas.yview)
        activities_scrollable_frame = ttk.Frame(activities_canvas)
        
        activities_scrollable_frame.bind(
            "<Configure>",
            lambda e: activities_canvas.configure(scrollregion=activities_canvas.bbox("all"))
        )
        
        activities_canvas.create_window((0, 0), window=activities_scrollable_frame, anchor="nw")
        activities_canvas.configure(yscrollcommand=activities_scrollbar.set)
        
        activities_canvas.pack(side="left", fill="both", expand=True)
        activities_scrollbar.pack(side="right", fill="y")
        
        # Display recent activities
        if self.recent_activities:
            for activity in self.recent_activities:
                activity_frame = tk.Frame(activities_scrollable_frame, bg=self.colors["background"], pady=5)
                activity_frame.pack(fill="x")
                
                icon_label = tk.Label(
                    activity_frame,
                    text=self.get_activity_icon(activity["type"]),
                    font=("Arial", 16),
                    bg=self.colors["background"],
                    fg=self.get_activity_color(activity["type"])
                )
                icon_label.pack(side="left", padx=5)
                
                activity_label = tk.Label(
                    activity_frame,
                    text=f"{activity['description']} - {activity['timestamp']}",
                    font=("Arial", 11),
                    bg=self.colors["background"],
                    fg=self.colors["text_dark"],
                    anchor="w"
                )
                activity_label.pack(side="left", padx=5, fill="x", expand=True)
        else:
            no_activities_label = tk.Label(
                activities_scrollable_frame,
                text="No recent activities",
                font=("Arial", 11, "italic"),
                bg=self.colors["background"],
                fg=self.colors["text_dark"]
            )
            no_activities_label.pack(pady=20)
        
        # Quick actions widget
        actions_frame = tk.LabelFrame(
            content_frame, 
            text=" Quick Actions ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        actions_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Create a grid for quick actions
        actions_grid = tk.Frame(actions_frame, bg=self.colors["background"])
        actions_grid.pack(fill="x", pady=10)
        
        quick_actions = [
            (f"{self.icons['functions']} Functions", lambda: self.notebook.select(2), self.colors["primary"]),
            (f"{self.icons['installation']} Check Tools", self.check_tools_installation, self.colors["secondary"]),
            (f"{self.icons['reports']} View Reports", lambda: self.notebook.select(4), self.colors["accent"]),
            (f"{self.icons['export']} Export Results", self.export_results, self.colors["primary_dark"])
        ]
        
        for i, (text, command, color) in enumerate(quick_actions):
            btn = tk.Button(
                actions_grid, 
                text=text, 
                command=command, 
                bg=color,
                fg=self.colors["text_light"],
                font=("Arial", 11),
                padx=10,
                pady=5
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            actions_grid.columnconfigure(i, weight=1)
        
        # Set row weights for content frame
        content_frame.rowconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=2)
        content_frame.rowconfigure(2, weight=1)
    
    def init_functions_tab(self):
        # Create a banner frame
        banner_frame = tk.Frame(self.functions_frame, bg=self.colors["secondary"], height=80)
        banner_frame.pack(fill="x", pady=0)
        
        # Add text to the banner
        banner_label = tk.Label(
            banner_frame, 
            text=f"{self.icons['functions']} Forensic Functions", 
            font=("Arial", 24, "bold"),
            fg=self.colors["text_light"],
            bg=self.colors["secondary"],
            pady=20
        )
        banner_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.functions_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Device selection frame
        device_frame = tk.Frame(content_frame, bg=self.colors["background"], padx=10, pady=10)
        device_frame.pack(fill="x", pady=10)
        
        device_icon_label = tk.Label(
            device_frame,
            text=self.icons["device"],
            font=("Arial", 16),
            bg=self.colors["background"],
            fg=self.colors["primary"]
        )
        device_icon_label.pack(side="left", padx=5)
        
        tk.Label(
            device_frame, 
            text="Selected Device:", 
            bg=self.colors["background"],
            fg=self.colors["text_dark"],
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=5)
        
        device_label = tk.Label(
            device_frame, 
            textvariable=self.selected_device,
            bg=self.colors["background"],
            fg=self.colors["primary"],
            font=("Arial", 11)
        )
        device_label.pack(side="left", padx=5)
        
        refresh_button = tk.Button(
            device_frame, 
            text=f"{self.icons['refresh']} Refresh", 
            command=self.update_device_list,
            bg=self.colors["secondary"],
            fg=self.colors["text_light"],
            font=("Arial", 11)
        )
        refresh_button.pack(side="right", padx=5)
        
        # Create a scrollable frame for functions
        functions_canvas = tk.Canvas(content_frame, bg=self.colors["background"], highlightthickness=0)
        functions_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=functions_canvas.yview)
        functions_scrollable_frame = ttk.Frame(functions_canvas)
        
        functions_scrollable_frame.bind(
            "<Configure>",
            lambda e: functions_canvas.configure(scrollregion=functions_canvas.bbox("all"))
        )
        
        functions_canvas.create_window((0, 0), window=functions_scrollable_frame, anchor="nw")
        functions_canvas.configure(yscrollcommand=functions_scrollbar.set)
        
        functions_canvas.pack(side="left", fill="both", expand=True, pady=10)
        functions_scrollbar.pack(side="right", fill="y", pady=10)
        
        # Define the functions with icons and descriptions
        functions = [
            (self.icons["photo_recovery"], "Photo Recovery", "Recover deleted photos using PhotoRec", 
             "Scans storage devices for lost files based on their signatures", self.run_photorec, self.colors["primary"]),
            
            (self.icons["password_cracking"], "Password Cracking", "Crack passwords using John the Ripper", 
             "Recovers passwords from various hash formats", self.run_john, self.colors["accent"]),
            
            (self.icons["disk_imaging"], "Disk Imaging", "Create disk images using Guymager", 
             "Creates forensic images of storage devices", self.run_guymager, self.colors["primary"]),
            
            (self.icons["memory_analysis"], "Memory Analysis", "Analyze memory dumps using Rekall", 
             "Extracts artifacts from memory dumps", self.run_rekall, self.colors["accent"]),
            
            (self.icons["file_system"], "File System Analysis", "Analyze file systems using Sleuthkit/Autopsy", 
             "Examines file systems for evidence", self.run_autopsy, self.colors["primary"]),
            
            (self.icons["network"], "Network Forensics", "Analyze network traffic using Wireshark", 
             "Inspects network packets for suspicious activity", self.run_wireshark, self.colors["accent"]),
            
            (self.icons["steganography"], "Steganography", "Detect hidden data using StegExpose", 
             "Identifies hidden data in images", self.run_stegexpose, self.colors["primary"])
        ]
        
        # Create function cards
        for i, (icon, name, desc, tooltip, command, color) in enumerate(functions):
            # Create a card frame for each function
            card_frame = tk.Frame(
                functions_scrollable_frame, 
                bg=self.colors["background"],
                bd=1,
                relief="raised",
                padx=10,
                pady=10
            )
            card_frame.pack(fill="x", padx=10, pady=10)
            
            # Create a header frame
            header_frame = tk.Frame(card_frame, bg=color)
            header_frame.pack(fill="x")
            
            # Add icon and title
            icon_label = tk.Label(
                header_frame,
                text=icon,
                font=("Arial", 20),
                bg=color,
                fg=self.colors["text_light"],
                padx=10,
                pady=5
            )
            icon_label.pack(side="left")
            
            title_label = tk.Label(
                header_frame,
                text=name,
                font=("Arial", 14, "bold"),
                bg=color,
                fg=self.colors["text_light"],
                padx=10,
                pady=10
            )
            title_label.pack(side="left")
            
            # Add description
            desc_frame = tk.Frame(card_frame, bg=self.colors["background"])
            desc_frame.pack(fill="x", pady=5)
            
            desc_label = tk.Label(
                desc_frame,
                text=desc,
                font=("Arial", 11),
                bg=self.colors["background"],
                fg=self.colors["text_dark"],
                anchor="w"
            )
            desc_label.pack(side="left", padx=10, pady=5)
            
            # Add tooltip
            tooltip_label = tk.Label(
                desc_frame,
                text=tooltip,
                font=("Arial", 10, "italic"),
                bg=self.colors["background"],
                fg=self.colors["primary"],
                anchor="w"
            )
            tooltip_label.pack(side="left", padx=10, pady=5)
            
            # Add button
            button_frame = tk.Frame(card_frame, bg=self.colors["background"])
            button_frame.pack(fill="x", pady=5)
            
            run_button = tk.Button(
                button_frame, 
                text="Run", 
                command=command, 
                bg=color,
                fg=self.colors["text_light"],
                font=("Arial", 12),
                width=10,
                padx=10,
                pady=5
            )
            run_button.pack(side="right", padx=10)
    
    def init_installation_tab(self):
        # Create a banner frame
        banner_frame = tk.Frame(self.installation_frame, bg=self.colors["warning"], height=80)
        banner_frame.pack(fill="x", pady=0)
        
        # Add text to the banner
        banner_label = tk.Label(
            banner_frame, 
            text=f"{self.icons['installation']} Tool Installation Status", 
            font=("Arial", 24, "bold"),
            fg=self.colors["text_dark"],
            bg=self.colors["warning"],
            pady=20
        )
        banner_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.installation_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a header
        header_frame = tk.Frame(content_frame, bg=self.colors["primary_dark"], padx=5, pady=5)
        header_frame.pack(fill="x", pady=10)
        
        # Create a header
        header_frame = tk.Frame(content_frame, bg=self.colors["primary_dark"], padx=5, pady=5)
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(
            header_frame, 
            text="Tool Name", 
            width=20, 
            anchor="w",
            bg=self.colors["primary_dark"],
            fg=self.colors["text_light"],
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        ).pack(side="left")
        
        tk.Label(
            header_frame, 
            text="Status", 
            width=10,
            bg=self.colors["primary_dark"],
            fg=self.colors["text_light"],
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        ).pack(side="left")
        
        tk.Label(
            header_frame, 
            text="Description", 
            width=40,
            anchor="w",
            bg=self.colors["primary_dark"],
            fg=self.colors["text_light"],
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        ).pack(side="left")
        
        # Create a frame for the tool status
        status_frame = tk.Frame(content_frame, bg=self.colors["background"])
        status_frame.pack(fill="both", expand=True, pady=10)
        
        # Define the tools to check
        tools = [
            ("PhotoRec", "testdisk", "File and photo recovery tool"),
            ("John the Ripper", "john", "Password cracking tool"),
            ("Guymager", "guymager", "Forensic disk imaging tool"),
            ("Rekall", "rekall", "Memory forensics framework"),
            ("Sleuthkit", "sleuthkit", "File system forensics toolkit"),
            ("Autopsy", "autopsy", "Digital forensics platform"),
            ("Wireshark", "wireshark", "Network protocol analyzer"),
            ("StegExpose", "StegExpose.jar", "Steganography detection tool")
        ]
        
        # Create status indicators for each tool
        self.status_labels = {}
        
        for i, (name, command, description) in enumerate(tools):
            # Create a frame for each tool
            tool_frame = tk.Frame(
                status_frame, 
                bg=self.colors["background"] if i % 2 == 0 else "#e2e8f0"
            )
            tool_frame.pack(fill="x")
            
            # Add tool name
            tool_label = tk.Label(
                tool_frame, 
                text=name, 
                width=20, 
                anchor="w",
                bg=tool_frame["bg"],
                fg=self.colors["text_dark"],
                font=("Arial", 11),
                padx=10,
                pady=8
            )
            tool_label.pack(side="left")
            
            # Add status label
            status_label = tk.Label(
                tool_frame, 
                text="Checking...", 
                width=10,
                bg=tool_frame["bg"],
                font=("Arial", 11),
                padx=10,
                pady=8
            )
            status_label.pack(side="left")
            
            # Add description
            desc_label = tk.Label(
                tool_frame, 
                text=description, 
                anchor="w",
                bg=tool_frame["bg"],
                fg=self.colors["text_dark"],
                font=("Arial", 11),
                padx=10,
                pady=8
            )
            desc_label.pack(side="left", fill="x", expand=True)
            
            self.status_labels[command] = status_label
        
        # Add buttons in a separate frame
        button_frame = tk.Frame(content_frame, bg=self.colors["background"])
        button_frame.pack(pady=20)
        
        # Add a button to check installation
        check_button = tk.Button(
            button_frame, 
            text=f"{self.icons['check']} Check Installation", 
            command=self.check_tools_installation,
            bg=self.colors["secondary"],
            fg=self.colors["text_light"],
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        check_button.pack(side="left", padx=10)
        
        # Add a button to install missing tools
        install_button = tk.Button(
            button_frame, 
            text=f"{self.icons['installation']} Install Missing Tools", 
            command=self.install_missing_tools,
            bg=self.colors["success"],
            fg=self.colors["text_light"],
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        install_button.pack(side="left", padx=10)
        
        # Check tools on initialization
        self.after(1000, self.check_tools_installation)
    
    def init_reports_tab(self):
        # Create a banner frame
        banner_frame = tk.Frame(self.reports_frame, bg=self.colors["accent"], height=80)
        banner_frame.pack(fill="x", pady=0)
        
        # Add text to the banner
        banner_label = tk.Label(
            banner_frame, 
            text=f"{self.icons['reports']} Forensic Reports", 
            font=("Arial", 24, "bold"),
            fg=self.colors["text_light"],
            bg=self.colors["accent"],
            pady=20
        )
        banner_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.reports_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create a frame for the reports list
        reports_frame = tk.LabelFrame(
            content_frame, 
            text=" Available Reports ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        reports_frame.pack(fill="both", expand=True, pady=10)
        
        # Get reports
        reports = self.get_available_reports()
        
        if reports:
            # Create a listbox for reports
            reports_listbox = tk.Listbox(
                reports_frame,
                bg=self.colors["background"],
                fg=self.colors["text_dark"],
                font=("Arial", 11),
                selectbackground=self.colors["primary"],
                selectforeground=self.colors["text_light"],
                height=15
            )
            reports_listbox.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Add reports to listbox
            for report in reports:
                reports_listbox.insert(tk.END, report)
            
            # Add buttons for report actions
            button_frame = tk.Frame(reports_frame, bg=self.colors["background"])
            button_frame.pack(fill="x", pady=10)
            
            view_button = tk.Button(
                button_frame, 
                text=f"{self.icons['search']} View Report", 
                command=lambda: self.view_report(reports_listbox.get(tk.ACTIVE)),
                bg=self.colors["primary"],
                fg=self.colors["text_light"],
                font=("Arial", 11),
                padx=10,
                pady=5
            )
            view_button.pack(side="left", padx=5)
            
            export_button = tk.Button(
                button_frame, 
                text=f"{self.icons['export']} Export Report", 
                command=lambda: self.export_report(reports_listbox.get(tk.ACTIVE)),
                bg=self.colors["secondary"],
                fg=self.colors["text_light"],
                font=("Arial", 11),
                padx=10,
                pady=5
            )
            export_button.pack(side="left", padx=5)
            
            delete_button = tk.Button(
                button_frame, 
                text=f"{self.icons['delete']} Delete Report", 
                command=lambda: self.delete_report(reports_listbox.get(tk.ACTIVE)),
                bg=self.colors["danger"],
                fg=self.colors["text_light"],
                font=("Arial", 11),
                padx=10,
                pady=5
            )
            delete_button.pack(side="left", padx=5)
        else:
            # No reports found
            no_reports_label = tk.Label(
                reports_frame,
                text="No reports found. Run forensic tools to generate reports.",
                font=("Arial", 11, "italic"),
                bg=self.colors["background"],
                fg=self.colors["text_dark"],
                pady=50
            )
            no_reports_label.pack()
    
    def init_about_tab(self):
        # Create a banner frame
        banner_frame = tk.Frame(self.about_frame, bg=self.colors["primary_dark"], height=80)
        banner_frame.pack(fill="x", pady=0)
        
        # Add text to the banner
        banner_label = tk.Label(
            banner_frame, 
            text=f"{self.icons['about']} About Digital Forensic Toolkit", 
            font=("Arial", 24, "bold"),
            fg=self.colors["text_light"],
            bg=self.colors["primary_dark"],
            pady=20
        )
        banner_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.about_frame, bg=self.colors["background"])
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Version info
        version_frame = tk.Frame(content_frame, bg=self.colors["primary"], padx=15, pady=15)
        version_frame.pack(fill="x", pady=10)
        
        tk.Label(
            version_frame,
            text="Digital Forensic Toolkit v1.1.0",
            font=("Arial", 16, "bold"),
            bg=self.colors["primary"],
            fg=self.colors["text_light"]
        ).pack()
        
        # About text
        about_text = """
This toolkit provides an easy-to-use interface for common digital forensic tasks.
It integrates several powerful open-source forensic tools to help investigators
analyze digital evidence efficiently and effectively.
        """
        
        about_label = tk.Label(
            content_frame,
            text=about_text,
            font=("Arial", 12),
            justify="left",
            bg=self.colors["background"],
            fg=self.colors["text_dark"],
            padx=10,
            pady=10
        )
        about_label.pack(fill="x", pady=10)
        
        # Tools list
        tools_frame = tk.LabelFrame(
            content_frame, 
            text=" Integrated Tools ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        tools_frame.pack(fill="x", pady=10)
        
        tools = [
            (self.icons["photo_recovery"], "PhotoRec", "For photo and file recovery", self.colors["primary"]),
            (self.icons["password_cracking"], "John the Ripper", "For password cracking", self.colors["accent"]),
            (self.icons["disk_imaging"], "Guymager", "For disk imaging", self.colors["primary"]),
            (self.icons["memory_analysis"], "Rekall", "For memory analysis", self.colors["accent"]),
            (self.icons["file_system"], "Sleuthkit/Autopsy", "For file system analysis", self.colors["primary"]),
            (self.icons["network"], "Wireshark", "For network forensics", self.colors["accent"]),
            (self.icons["steganography"], "StegExpose", "For steganography detection", self.colors["primary"])
        ]
        
        for icon, name, desc, color in tools:
            tool_frame = tk.Frame(tools_frame, bg=self.colors["background"])
            tool_frame.pack(fill="x", pady=2)
            
            icon_label = tk.Label(
                tool_frame,
                text=icon,
                font=("Arial", 16),
                bg=self.colors["background"],
                fg=color
            )
            icon_label.pack(side="left", padx=5)
            
            name_label = tk.Label(
                tool_frame,
                text=name,
                font=("Arial", 12, "bold"),
                bg=self.colors["background"],
                fg=self.colors["text_dark"]
            )
            name_label.pack(side="left", padx=5)
            
            desc_label = tk.Label(
                tool_frame,
                text=f"- {desc}",
                font=("Arial", 12),
                bg=self.colors["background"],
                fg=self.colors["text_dark"]
            )
            desc_label.pack(side="left", padx=5)
        
        # Help section
        help_frame = tk.LabelFrame(
            content_frame, 
            text=" Help & Support ", 
            font=("Arial", 12, "bold"),
            bg=self.colors["background"],
            fg=self.colors["primary"],
            padx=15,
            pady=15
        )
        help_frame.pack(fill="x", pady=10)
        
        help_text = """
For help with using this toolkit:

1. Check the documentation in the 'docs' folder
2. Visit the project website for tutorials and guides
3. Report issues on the project's issue tracker
        """
        
        help_label = tk.Label(
            help_frame,
            text=help_text,
            font=("Arial", 11),
            justify="left",
            bg=self.colors["background"],
            fg=self.colors["text_dark"]
        )
        help_label.pack(anchor="w", pady=5)
        
        # Disclaimer
        disclaimer_frame = tk.Frame(content_frame, bg="#f8d7da", padx=15, pady=15)
        disclaimer_frame.pack(fill="x", pady=10)
        
        disclaimer_icon = tk.Label(
            disclaimer_frame,
            text=self.icons["warning"],
            font=("Arial", 16),
            bg="#f8d7da",
            fg="#721c24"
        )
        disclaimer_icon.pack(side="left", padx=5)
        
        disclaimer_label = tk.Label(
            disclaimer_frame,
            text="Note: This toolkit should be used responsibly and legally.\nAlways ensure you have proper authorization before analyzing any digital device.",
            font=("Arial", 11, "italic"),
            bg="#f8d7da",
            fg="#721c24",
            justify="left"
        )
        disclaimer_label.pack(side="left", padx=5)
    
    def get_connected_devices(self):
        """Get a list of connected USB and external storage devices"""
        devices = []
        try:
            # Run lsblk to get block devices
            result = subprocess.run(
                ["lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT", "-n"],
                capture_output=True, 
                text=True, 
                check=True
            )
            
            # Parse the output
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[2] in ["disk", "part"]:
                    name = parts[0]
                    size = parts[1]
                    
                    # Skip system disk (usually sda)
                    if name.startswith(("loop", "sr")):
                        continue
                    
                    # Add device to list
                    device_path = f"/dev/{name}"
                    devices.append(f"{device_path} ({size})")
            
            logger.info(f"Found devices: {devices}")
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
        
        return devices
    
    def update_device_list(self):
        """Update the device dropdown with connected devices"""
        self.devices = self.get_connected_devices()
        self.device_dropdown['values'] = self.devices
        
        if self.devices and not self.selected_device.get():
            self.selected_device.set(self.devices[0])
        
        # Update status
        if hasattr(self, 'status_text'):
            self.status_text.config(text=f"Found {len(self.devices)} devices")
    
    def monitor_devices(self):
        """Monitor for new device connections"""
        previous_devices = set(self.devices)
        
        while not self.stop_monitoring:
            current_devices = set(self.get_connected_devices())
            
            # Check for new devices
            new_devices = current_devices - previous_devices
            if new_devices:
                logger.info(f"New devices detected: {new_devices}")
                self.update_device_list()
                
                # Show notification
                self.after(0, lambda: messagebox.showinfo(
                    "Device Detected", 
                    f"New storage device detected: {list(new_devices)[0]}"
                ))
            
            previous_devices = current_devices
            time.sleep(2)
    
    def check_tools_installation(self):
        """Check if all required tools are installed"""
        tools_status = {
            "testdisk": self.check_tool_installed("testdisk"),
            "john": self.check_tool_installed("john"),
            "guymager": self.check_tool_installed("guymager"),
            "rekall": self.check_tool_installed("rekall"),
            "sleuthkit": self.check_tool_installed("sleuthkit"),
            "autopsy": self.check_tool_installed("autopsy"),
            "wireshark": self.check_tool_installed("wireshark"),
            "StegExpose.jar": os.path.exists(os.path.expanduser("~/StegExpose/StegExpose.jar"))
        }
        
        # Update status labels
        for tool, status in tools_status.items():
            if tool in self.status_labels:
                if status:
                    self.status_labels[tool].config(
                        text=f"{self.icons['check']} Installed", 
                        foreground="green"
                    )
                else:
                    self.status_labels[tool].config(
                        text=f"{self.icons['check']} Installed", 
                        foreground="green"
                    )
        
        # Update status bar
        installed_count = sum(1 for status in tools_status.values() if status)
        total_count = len(tools_status)
        self.status_text.config(text=f"Tools installed: {installed_count}/{total_count}")
    
    def check_tool_installed(self, tool_name):
        """Check if a tool is installed by running 'which' command"""
        try:
            result = subprocess.run(
                ["which", tool_name],
                capture_output=True, 
                check=False
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def install_missing_tools(self):
        """Install missing tools"""
        missing_tools = []
        
        for tool, label in self.status_labels.items():
            if "Not Found" in label.cget("text"):
                missing_tools.append(tool)
        
        if not missing_tools:
            messagebox.showinfo("Installation", "All tools are already installed!")
            return
        
        # Ask for confirmation
        if not messagebox.askyesno(
            "Install Tools", 
            f"Do you want to install the following tools?\n\n{', '.join(missing_tools)}"
        ):
            return
        
        # Show progress dialog
        progress_window = tk.Toplevel(self)
        progress_window.title("Installing Tools")
        progress_window.geometry("400x150")
        progress_window.transient(self)
        progress_window.grab_set()
        
        progress_label = tk.Label(
            progress_window,
            text="Installing tools...",
            font=("Arial", 12),
            pady=10
        )
        progress_label.pack()
        
        progress_bar = ttk.Progressbar(
            progress_window,
            orient="horizontal",
            length=350,
            mode="indeterminate"
        )
        progress_bar.pack(pady=10)
        progress_bar.start(10)
        
        status_label = tk.Label(
            progress_window,
            text="Preparing installation...",
            font=("Arial", 10),
            pady=5
        )
        status_label.pack()
        
        # Run installation in a separate thread
        def update_status(text):
            status_label.config(text=text)
        
        install_thread = threading.Thread(
            target=self.do_install_tools, 
            args=(missing_tools, update_status, progress_window)
        )
        install_thread.daemon = True
        install_thread.start()
    
    def do_install_tools(self, tools, update_status, progress_window):
        """Perform the actual installation"""
        try:
            # Update package lists
            update_status("Updating package lists...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            
            # Install apt packages
            apt_tools = [t for t in tools if t != "StegExpose.jar" and t != "rekall"]
            if apt_tools:
                update_status(f"Installing: {', '.join(apt_tools)}")
                subprocess.run(["sudo", "apt", "install", "-y"] + apt_tools, check=True)
            
            # Install Rekall if needed
            if "rekall" in tools:
                update_status("Installing Rekall...")
                subprocess.run(["sudo", "pip3", "install", "rekall"], check=True)
            
            # Install StegExpose if needed
            if "StegExpose.jar" in tools:
                update_status("Installing StegExpose...")
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
            
            # Update status
            self.after(0, self.check_tools_installation)
            
            # Add to recent activities
            self.add_activity("installation", f"Installed tools: {', '.join(tools)}")
            
            # Close progress window and show success message
            self.after(0, progress_window.destroy)
            self.after(0, lambda: messagebox.showinfo(
                "Installation Complete", 
                "Tools installation completed successfully!"
            ))
        
        except Exception as e:
            logger.error(f"Installation error: {e}")
            self.after(0, progress_window.destroy)
            self.after(0, lambda: messagebox.showerror(
                "Installation Error", 
                f"Error installing tools: {str(e)}"
            ))
    
    def get_selected_device_path(self):
        """Get the path of the selected device"""
        device_str = self.selected_device.get()
        if not device_str:
            messagebox.showerror("Error", "No device selected!")
            return None
        
        # Extract device path from the string (format: "/dev/sdX (size)")
        device_path = device_str.split()[0]
        return device_path
    
    def create_results_dir(self):
        """Create a directory for storing results if it doesn't exist"""
        results_dir = os.path.expanduser("~/forensic_results")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        return results_dir
    
    def run_photorec(self):
        """Run PhotoRec for photo recovery"""
        device_path = self.get_selected_device_path()
        if not device_path:
            return
        
        # Create results directory
        results_dir = self.create_results_dir()
        output_dir = os.path.join(results_dir, "photorec_results")
        os.makedirs(output_dir, exist_ok=True)
        
        # Run PhotoRec in a new terminal
        try:
            subprocess.Popen([
                "x-terminal-emulator", 
                "-e", 
                f"sudo photorec {device_path}"
            ])
            
            messagebox.showinfo(
                "PhotoRec", 
                "PhotoRec has been launched in a new terminal window.\n"
                "Follow the on-screen instructions to recover files."
            )
            
            # Add to recent activities
            self.add_activity("photo_recovery", f"Photo recovery on {device_path}")
            
        except Exception as e:
            logger.error(f"Error running PhotoRec: {e}")
            messagebox.showerror("Error", f"Failed to run PhotoRec: {str(e)}")
    
    def run_john(self):
        """Run John the Ripper for password cracking"""
        # Ask for hash file
        hash_file = filedialog.askopenfilename(
            title="Select Hash File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not hash_file:
            return
        
        # Create results directory
        results_dir = self.create_results_dir()
        output_file = os.path.join(results_dir, "john_results.txt")
        
        # Run John in a new terminal
        try:
            subprocess.Popen([
                "x-terminal-emulator", 
                "-e", 
                f"sudo john --wordlist=/usr/share/wordlists/rockyou.txt {hash_file} --pot={output_file}"
            ])
            
            messagebox.showinfo(
                "John the Ripper", 
                "John the Ripper has been launched in a new terminal window.\n"
                f"Results will be saved to {output_file}"
            )
            
            # Add to recent activities
            self.add_activity("password_cracking", f"Password cracking on {os.path.basename(hash_file)}")
            
        except Exception as e:
            logger.error(f"Error running John: {e}")
            messagebox.showerror("Error", f"Failed to run John the Ripper: {str(e)}")
    
    def run_guymager(self):
        """Run Guymager for disk imaging"""
        try:
            subprocess.Popen(["sudo", "guymager"])
            
            messagebox.showinfo(
                "Guymager", 
                "Guymager has been launched.\n"
                "Use the interface to create disk images."
            )
            
            # Add to recent activities
            self.add_activity("disk_imaging", "Disk imaging with Guymager")
            
        except Exception as e:
            logger.error(f"Error running Guymager: {e}")
            messagebox.showerror("Error", f"Failed to run Guymager: {str(e)}")
    
    def run_rekall(self):
        """Run Rekall for memory analysis"""
        # Ask for memory dump file
        memory_file = filedialog.askopenfilename(
            title="Select Memory Dump File",
            filetypes=[("Memory dumps", "*.dmp *.raw *.mem"), ("All files", "*.*")]
        )
        
        if not memory_file:
            return
        
        # Create results directory
        results_dir = self.create_results_dir()
        output_file = os.path.join(results_dir, "rekall_results.txt")
        
        # Run Rekall in a new terminal
        try:
            subprocess.Popen([
                "x-terminal-emulator", 
                "-e", 
                f"rekall -f {memory_file} pslist > {output_file}"
            ])
            
            messagebox.showinfo(
                "Rekall", 
                "Rekall has been launched in a new terminal window.\n"
                f"Results will be saved to {output_file}"
            )
            
            # Add to recent activities
            self.add_activity("memory_analysis", f"Memory analysis on {os.path.basename(memory_file)}")
            
        except Exception as e:
            logger.error(f"Error running Rekall: {e}")
            messagebox.showerror("Error", f"Failed to run Rekall: {str(e)}")
    
    def run_autopsy(self):
        """Run Autopsy for file system analysis"""
        try:
            subprocess.Popen(["sudo", "autopsy"])
            
            messagebox.showinfo(
                "Autopsy", 
                "Autopsy has been launched.\n"
                "Use the web interface to analyze file systems."
            )
            
            # Add to recent activities
            self.add_activity("file_system", "File system analysis with Autopsy")
            
        except Exception as e:
            logger.error(f"Error running Autopsy: {e}")
            messagebox.showerror("Error", f"Failed to run Autopsy: {str(e)}")
    
    def run_wireshark(self):
        """Run Wireshark for network forensics"""
        try:
            subprocess.Popen(["sudo", "wireshark"])
            
            messagebox.showinfo(
                "Wireshark", 
                "Wireshark has been launched.\n"
                "Use the interface to analyze network traffic."
            )
            
            # Add to recent activities
            self.add_activity("network", "Network analysis with Wireshark")
            
        except Exception as e:
            logger.error(f"Error running Wireshark: {e}")
            messagebox.showerror("Error", f"Failed to run Wireshark: {str(e)}")
    
    def run_stegexpose(self):
        """Run StegExpose for steganography detection"""
        # Ask for directory containing suspicious files
        steg_dir = filedialog.askdirectory(
            title="Select Directory with Suspicious Files"
        )
        
        if not steg_dir:
            return
        
        # Create results directory
        results_dir = self.create_results_dir()
        output_file = os.path.join(results_dir, "stegexpose_results.csv")
        
        # Run StegExpose in a new terminal
        try:
            stegexpose_path = os.path.expanduser("~/StegExpose/StegExpose.jar")
            
            subprocess.Popen([
                "x-terminal-emulator", 
                "-e", 
                f"java -jar {stegexpose_path} -s {steg_dir} -o {output_file}"
            ])
            
            messagebox.showinfo(
                "StegExpose", 
                "StegExpose has been launched in a new terminal window.\n"
                f"Results will be saved to {output_file}"
            )
            
            # Add to recent activities
            self.add_activity("steganography", f"Steganography analysis on {os.path.basename(steg_dir)}")
            
        except Exception as e:
            logger.error(f"Error running StegExpose: {e}")
            messagebox.showerror("Error", f"Failed to run StegExpose: {str(e)}")
    
    def get_system_info(self):
        """Get system information"""
        system_info = {}
        
        # Get OS info
        system_info["Operating System"] = platform.system() + " " + platform.release()
        
        # Get hostname
        system_info["Hostname"] = platform.node()
        
        # Get disk space
        try:
            total, used, free = shutil.disk_usage("/")
            system_info["Disk Space"] = f"{free // (2**30)} GB free of {total // (2**30)} GB"
        except:
            system_info["Disk Space"] = "Unknown"
        
        # Get memory info
        try:
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    if "MemTotal" in line:
                        mem_total = int(line.split()[1]) // 1024  # Convert to MB
                        system_info["Memory"] = f"{mem_total} MB"
                        break
        except:
            system_info["Memory"] = "Unknown"
        
        # Get Python version
        system_info["Python Version"] = platform.python_version()
        
        return system_info
    
    def load_recent_activities(self):
        """Load recent activities from file"""
        activities_file = os.path.expanduser("~/forensic_results/activities.json")
        
        if os.path.exists(activities_file):
            try:
                with open(activities_file, "r") as f:
                    return json.load(f)
            except:
                return []
        else:
            return []
    
    def save_recent_activities(self):
        """Save recent activities to file"""
        activities_file = os.path.expanduser("~/forensic_results/activities.json")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(activities_file), exist_ok=True)
        
        try:
            with open(activities_file, "w") as f:
                json.dump(self.recent_activities, f)
        except Exception as e:
            logger.error(f"Error saving activities: {e}")
    
    def add_activity(self, activity_type, description):
        """Add a new activity to the recent activities list"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        activity = {
            "type": activity_type,
            "description": description,
            "timestamp": timestamp
        }
        
        self.recent_activities.insert(0, activity)
        
        # Limit to 20 most recent activities
        if len(self.recent_activities) > 20:
            self.recent_activities = self.recent_activities[:20]
        
        # Save activities
        self.save_recent_activities()
    
    def get_activity_icon(self, activity_type):
        """Get icon for activity type"""
        icons = {
            "photo_recovery": self.icons["photo_recovery"],
            "password_cracking": self.icons["password_cracking"],
            "disk_imaging": self.icons["disk_imaging"],
            "memory_analysis": self.icons["memory_analysis"],
            "file_system": self.icons["file_system"],
            "network": self.icons["network"],
            "steganography": self.icons["steganography"],
            "installation": self.icons["installation"]
        }
        
        return icons.get(activity_type, self.icons["info"])
    
    def get_activity_color(self, activity_type):
        """Get color for activity type"""
        colors = {
            "photo_recovery": self.colors["primary"],
            "password_cracking": self.colors["accent"],
            "disk_imaging": self.colors["secondary"],
            "memory_analysis": self.colors["primary"],
            "file_system": self.colors["accent"],
            "network": self.colors["secondary"],
            "steganography": self.colors["primary"],
            "installation": self.colors["success"]
        }
        
        return colors.get(activity_type, self.colors["primary"])
    
    def get_available_reports(self):
        """Get list of available reports"""
        results_dir = self.create_results_dir()
        reports = []
        
        # Check for report files
        if os.path.exists(results_dir):
            for file in os.listdir(results_dir):
                if file.endswith((".txt", ".csv", ".html")):
                    reports.append(file)
        
        return reports
    
    def view_report(self, report_name):
        """View a report"""
        if not report_name:
            return
        
        results_dir = self.create_results_dir()
        report_path = os.path.join(results_dir, report_name)
        
        if os.path.exists(report_path):
            try:
                # Open report with default application
                if platform.system() == "Linux":
                    subprocess.Popen(["xdg-open", report_path])
                elif platform.system() == "Windows":
                    os.startfile(report_path)
                else:
                    subprocess.Popen(["open", report_path])
            except Exception as e:
                logger.error(f"Error opening report: {e}")
                messagebox.showerror("Error", f"Failed to open report: {str(e)}")
        else:
            messagebox.showerror("Error", f"Report file not found: {report_path}")
    
    def export_report(self, report_name):
        """Export a report"""
        if not report_name:
            return
        
        results_dir = self.create_results_dir()
        report_path = os.path.join(results_dir, report_name)
        
        if os.path.exists(report_path):
            # Ask for destination
            dest_path = filedialog.asksaveasfilename(
                title="Export Report",
                initialfile=report_name,
                defaultextension=os.path.splitext(report_name)[1]
            )
            
            if dest_path:
                try:
                    shutil.copy2(report_path, dest_path)
                    messagebox.showinfo("Export", f"Report exported to {dest_path}")
                except Exception as e:
                    logger.error(f"Error exporting report: {e}")
                    messagebox.showerror("Error", f"Failed to export report: {str(e)}")
        else:
            messagebox.showerror("Error", f"Report file not found: {report_path}")
    
    def delete_report(self, report_name):
        """Delete a report"""
        if not report_name:
            return
        
        results_dir = self.create_results_dir()
        report_path = os.path.join(results_dir, report_name)
        
        if os.path.exists(report_path):
            # Ask for confirmation
            if messagebox.askyesno("Delete Report", f"Are you sure you want to delete {report_name}?"):
                try:
                    os.remove(report_path)
                    messagebox.showinfo("Delete", f"Report {report_name} deleted")
                    
                    # Refresh reports tab
                    self.init_reports_tab()
                except Exception as e:
                    logger.error(f"Error deleting report: {e}")
                    messagebox.showerror("Error", f"Failed to delete report: {str(e)}")
        else:
            messagebox.showerror("Error", f"Report file not found: {report_path}")
    
    def export_results(self):
        """Export all results"""
        results_dir = self.create_results_dir()
        
        if not os.path.exists(results_dir) or not os.listdir(results_dir):
            messagebox.showinfo("Export", "No results to export")
            return
        
        # Ask for destination directory
        dest_dir = filedialog.askdirectory(
            title="Select Export Directory"
        )
        
        if not dest_dir:
            return
        
        try:
            # Create a zip file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_file = os.path.join(dest_dir, f"forensic_results_{timestamp}.zip")
            
            shutil.make_archive(
                os.path.splitext(zip_file)[0],
                'zip',
                results_dir
            )
            
            messagebox.showinfo("Export", f"Results exported to {zip_file}")
        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")

if __name__ == "__main__":
    app = ForensicToolkit()
    app.mainloop()

