#!/bin/bash

# Digital Forensic Toolkit Installer
# ----------------------------------

echo "====================================================="
echo "      Digital Forensic Toolkit - Installer           "
echo "====================================================="

# Create installation directory
INSTALL_DIR="$HOME/DigitalForensicToolkit"
echo "[+] Creating installation directory..."
mkdir -p "$INSTALL_DIR"

# Copy main script
echo "[+] Copying toolkit files..."
cp forensic_toolkit.py "$INSTALL_DIR/"

# Install dependencies
echo "[+] Installing required packages..."
sudo apt update
sudo apt install -y python3 python3-tk python3-pip
sudo apt install -y testdisk john guymager sleuthkit autopsy wireshark

# Install Rekall
echo "[+] Installing Rekall..."
sudo pip3 install rekall

# Install StegExpose
echo "[+] Installing StegExpose..."
if [ ! -d "$HOME/StegExpose" ]; then
  git clone https://github.com/b3dk7/StegExpose.git "$HOME/StegExpose"
  chmod +x "$HOME/StegExpose/StegExpose.jar"
fi

# Create desktop shortcut
echo "[+] Creating desktop shortcut..."
cat > "$HOME/Desktop/forensic-toolkit.desktop" << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Digital Forensic Toolkit
Comment=Launch the Digital Forensic Toolkit
Exec=python3 $INSTALL_DIR/forensic_toolkit.py
Icon=utilities-terminal
Terminal=false
Categories=Utility;
EOL
chmod +x "$HOME/Desktop/forensic-toolkit.desktop"

# Create uninstaller
echo "[+] Creating uninstaller..."
cat > "$INSTALL_DIR/uninstall.sh" << EOL
#!/bin/bash
echo "Uninstalling Digital Forensic Toolkit..."
rm -rf "$INSTALL_DIR"
rm -f "$HOME/Desktop/forensic-toolkit.desktop"
echo "Uninstallation complete!"
EOL
chmod +x "$INSTALL_DIR/uninstall.sh"

echo "====================================================="
echo "Installation complete!"
echo "The toolkit has been installed to: $INSTALL_DIR"
echo "A desktop shortcut has been created."
echo ""
echo "To run the toolkit:"
echo "1. Double-click the desktop shortcut, or"
echo "2. Run: python3 $INSTALL_DIR/forensic_toolkit.py"
echo ""
echo "To uninstall, run: $INSTALL_DIR/uninstall.sh"
echo "====================================================="
