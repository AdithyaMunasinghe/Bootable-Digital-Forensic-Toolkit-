# Digital Forensic Toolkit

<p align="center">
  A centralized Linux desktop interface for common digital-forensics workflows.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Kali%20Linux%20%7C%20Ubuntu-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/GUI-Tkinter-2C5282?style=flat-square" alt="Tkinter">
  <img src="https://img.shields.io/badge/Status-Prototype-orange?style=flat-square" alt="Project status">
</p>

## Overview

Digital Forensic Toolkit is a Python and Tkinter application that provides a single interface for launching and managing common digital-forensics tools.

Instead of opening and managing each forensic utility independently, investigators can use the toolkit to detect storage devices, launch investigation workflows, track recent activity, manage reports, and export collected results.

> **Project status:** The current version runs as a desktop application on Kali Linux or Ubuntu. A bootable live image is not currently included in this repository.

## Key Features

- Detect connected disks and storage partitions
- Monitor devices and refresh the device list
- Check whether required forensic tools are installed
- Install missing dependencies
- Launch common forensic workflows from one interface
- Record recent investigation activity
- View, export and remove generated reports
- Export collected results as a timestamped ZIP archive
- Create a Linux desktop shortcut during installation

## Integrated Forensic Tools

| Investigation area | Tool | Current workflow |
|---|---|---|
| File recovery | PhotoRec | Launches PhotoRec against a selected device |
| Password auditing | John the Ripper | Processes a user-selected hash file |
| Disk acquisition | Guymager | Opens the Guymager imaging interface |
| Memory analysis | Rekall | Runs process-list analysis against a memory image |
| File-system analysis | Autopsy / Sleuth Kit | Opens Autopsy for file-system investigation |
| Network forensics | Wireshark | Opens Wireshark for traffic analysis |
| Steganography detection | StegExpose | Scans a selected directory and produces CSV output |

## Application Sections

### Home

Provides an introduction to the toolkit and quick access to its main features.

### Dashboard

Displays connected block devices, toolkit status and recent investigation activity.

### Forensic Functions

Provides launch controls for file recovery, password auditing, disk imaging, memory analysis, file-system analysis, network forensics and steganography detection.

### Installation

Checks the availability of required forensic tools and assists with installing missing dependencies.

### Reports

Lists supported report files from the results directory and allows them to be opened, exported or removed.

## Technology Stack

- Python 3
- Tkinter and `ttk`
- Bash
- Linux command-line utilities
- JSON activity storage
- Python logging
- ZIP-based result export

## System Requirements

- Kali Linux or Ubuntu
- Python 3.6 or newer
- A graphical desktop environment
- `sudo` access for installing and launching certain tools
- An internet connection during dependency installation
- Java Runtime Environment for StegExpose
- `x-terminal-emulator`
- Git

Some forensic tools may not be available in every Ubuntu release or may require additional repositories.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AdithyaMunasinghe/Bootable-Digital-Forensic-Toolkit-.git
cd Bootable-Digital-Forensic-Toolkit-/forensic_toolkit_shared
```

### 2. Review and run the installer

The installer uses `sudo`, installs system packages, clones StegExpose and creates a desktop shortcut. Review the script before running it.

```bash
chmod +x install_toolkit.sh
./install_toolkit.sh
```

The application will be installed in:

```text
~/DigitalForensicToolkit
```

### 3. Launch the toolkit

Use the generated desktop shortcut or run:

```bash
python3 ~/DigitalForensicToolkit/forensic_toolkit.py
```

## Manual Installation

Install the required system packages:

```bash
sudo apt update
sudo apt install -y \
  python3 \
  python3-tk \
  python3-pip \
  git \
  default-jre \
  testdisk \
  john \
  guymager \
  sleuthkit \
  autopsy \
  wireshark
```

Install Rekall:

```bash
sudo pip3 install rekall
```

Install StegExpose:

```bash
git clone https://github.com/b3dk7/StegExpose.git ~/StegExpose
chmod +x ~/StegExpose/StegExpose.jar
```

Launch the application from the cloned repository:

```bash
cd Bootable-Digital-Forensic-Toolkit-/forensic_toolkit_shared
python3 forensic_toolkit.py
```

> Rekall is an older project and may have compatibility issues with recent Python distributions. Installation success depends on the operating system and Python version.

## Usage

1. Launch the application.
2. Open the dashboard and refresh the connected-device list.
3. Carefully verify the target device before beginning an investigation.
4. Open the forensic-functions section.
5. Choose the required investigation workflow.
6. Follow the instructions provided by the launched forensic tool.
7. Review generated output from the reports section.
8. Export the investigation results when required.

## Results and Activity Data

Generated files and activity history are stored in:

```text
~/forensic_results
```

Depending on the selected workflow, this directory may contain:

```text
activities.json
john_results.txt
rekall_results.txt
stegexpose_results.csv
photorec_results/
```

The application can export the contents of this directory as:

```text
forensic_results_YYYYMMDD_HHMMSS.zip
```

A runtime log is written to:

```text
forensic_toolkit.log
```

## Important Operational Notes

### Device selection

The application uses `lsblk` to discover block devices and partitions. Always verify the selected device path before starting an operation.

### Write protection

The current application does not enforce hardware or software write blocking. For evidential investigations, use an appropriate forensic write blocker and follow your organization’s acquisition procedures.

### Evidence integrity

The current version does not automatically calculate or verify evidence hashes. Investigators should independently calculate cryptographic hashes before and after acquisition.

### John the Ripper wordlist

The password-auditing workflow expects the following wordlist:

```text
/usr/share/wordlists/rockyou.txt
```

On Kali Linux, it may initially be compressed. If authorized to use it, extract it with:

```bash
sudo gzip -dk /usr/share/wordlists/rockyou.txt.gz
```

## Project Structure

```text
Bootable-Digital-Forensic-Toolkit-/
├── .gitattributes
└── forensic_toolkit_shared/
    ├── forensic_toolkit.py    # Main Tkinter application
    ├── install_toolkit.sh     # Bash installer
    ├── toolkit_setup.py       # Graphical setup utility
    ├── test.py                # Test script
    ├── README.txt             # Original installation notes
    └── forensic_toolkit.log   # Application log
```

## Security and Ethical Use

This toolkit includes functionality related to password auditing, storage-device analysis, network inspection and data recovery.

Use it only:

- On systems and data you own
- With clear authorization from the system or data owner
- In accordance with applicable laws and organizational policies
- Under an approved digital-forensics or incident-response process

The author is not responsible for unauthorized, illegal or unethical use of this software.

## Current Limitations

- No bootable ISO or live-environment build configuration is included
- No automatic write-blocking protection
- No automatic evidence hashing or verification
- Some workflows launch external tools rather than processing evidence internally
- Rekall may not work with modern Python environments
- Tool availability differs between Linux distributions
- Automated tests and continuous integration are not yet included

## Roadmap

Potential future improvements include:

- [ ] Build a bootable Kali or Ubuntu live image
- [ ] Add SHA-256 evidence hashing and verification
- [ ] Add case and evidence metadata management
- [ ] Add chain-of-custody reporting
- [ ] Add read-only device-mounting controls
- [ ] Add Volatility 3 memory-analysis support
- [ ] Improve dependency and compatibility checks
- [ ] Add structured HTML and PDF reports
- [ ] Add automated tests and continuous integration
- [ ] Package the application for easier installation

## Contributing

Contributions, issue reports and improvement suggestions are welcome.

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```

4. Push the branch:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a pull request.

## Author

Developed by [Adithya Munasinghe](https://github.com/AdithyaMunasinghe).

---

If this project is useful, consider giving the repository a ⭐.
