HOW TO INSTALL AND RUN THE DIGITAL FORENSIC TOOLKIT
===================================================

1. SYSTEM REQUIREMENTS:
   - Kali Linux or Ubuntu Linux
   - Python 3.6 or higher
   - Internet connection (for installing dependencies)

2. INSTALLATION:
   - Copy the "Digital_Forensic_Toolkit" folder to your home directory
   - Open a terminal
   - Run these commands:
     
     sudo apt update
     sudo apt install -y python3 python3-tk
     sudo apt install -y testdisk john guymager sleuthkit autopsy wireshark
     sudo pip3 install rekall
     
     git clone https://github.com/b3dk7/StegExpose.git ~/StegExpose
     chmod +x ~/StegExpose/StegExpose.jar

3. RUNNING THE TOOLKIT:
   - Open a terminal
   - Navigate to the toolkit directory:
     cd ~/Digital_Forensic_Toolkit
   - Run the toolkit:
     python3 forensic_toolkit.py

4. TROUBLESHOOTING:
   - If you get errors about missing packages, run the installation commands again
   - If the GUI doesn't appear, make sure python3-tk is installed
   - For other issues, contact: [Your Email]

