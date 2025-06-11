# PyPackager

![dev-starter Chat Demo](https://raw.githubusercontent.com/LMLK-seal/PyPackager/refs/heads/main/img.jpg)

**A Modern GUI Frontend for PyInstaller**

PyPackager is a user-friendly graphical interface that simplifies the process of converting Python scripts into standalone executable files. Built with CustomTkinter, it provides an intuitive way to package your Python applications without dealing with complex command-line arguments.

## Features

### 🎯 **Simple Interface**
- Clean, modern dark-themed GUI
- Intuitive file selection with browse buttons
- Real-time build progress monitoring
- Comprehensive output logging

### 📦 **Flexible Packaging Options**
- **Single File Mode**: Create a single executable file (`--onefile`)
- **Windowless Mode**: Perfect for GUI applications (`--windowed`)
- **Custom Icons**: Add custom `.ico` files to your executables
- **Data Files**: Include additional files and folders in your package

### 🛠 **Advanced Features**
- Custom output directory selection
- Real-time PyInstaller output display
- Thread-safe GUI operations
- Cross-platform compatibility (Windows, macOS, Linux)
- One-click access to output folder

## Prerequisites

- Python 3.6 or higher
- PyInstaller (`pip install pyinstaller`)
- CustomTkinter (`pip install customtkinter`)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LMLK-Seal/PyPackager.git
   cd PyPackager
   ```

2. **Install dependencies:**
   ```bash
   pip install pyinstaller customtkinter
   ```

3. **Run PyPackager:**
   ```bash
   python PyPackager.py
   ```

## Usage

### Basic Workflow

1. **Select Python Script**: Browse and select your main `.py` file
2. **Choose Icon (Optional)**: Select a `.ico` file for your executable
3. **Set Output Directory (Optional)**: Choose where to save the built executable
4. **Configure Options**:
   - Enable "Create one single file" for a single executable
   - Enable "Windowless" for GUI applications
5. **Add Data Files (Optional)**: Include additional files/folders your app needs
6. **Click "BUILD EXE"**: Watch the real-time build progress
7. **Access Results**: Use the "Open Output Folder" button when complete

### Build Options

| Option | Description | PyInstaller Flag |
|--------|-------------|------------------|
| **One File** | Packages everything into a single executable | `--onefile` |
| **Windowless** | Hides console window (ideal for GUI apps) | `--windowed` |
| **Custom Icon** | Sets a custom icon for the executable | `--icon` |
| **Data Files** | Includes additional files in the package | `--add-data` |


## Technical Details

- **GUI Framework**: CustomTkinter for modern, cross-platform interface
- **Threading**: Non-blocking UI with threaded PyInstaller execution
- **Output Handling**: Real-time command output capture and display
- **Error Handling**: Comprehensive error reporting and user feedback

## File Structure

```
PyPackager/
├── PyPackager.py          # Main application file
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Requirements

Download the `requirements.txt` file:
```
customtkinter>=5.0.0
pyinstaller>=5.0.0
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Known Issues

- The application requires PyInstaller to be installed and accessible via command line
- Large applications may take considerable time to package
- Some antivirus software may flag PyInstaller-generated executables as false positives

## Roadmap

- [ ] Add support for additional PyInstaller options
- [ ] Implement project save/load functionality
- [ ] Add executable testing capabilities
- [ ] Include dependency analysis tools
- [ ] Add support for virtual environments

## License

This project is licensed under the MIT License.

## Acknowledgments

- [PyInstaller](https://pyinstaller.readthedocs.io/) - The powerful Python packaging tool
- [CustomTkinter](https://customtkinter.tomschimansky.com/) - Modern GUI framework for Python
- Python community for continuous support and inspiration


**Made with ❤️ for the Python community**
