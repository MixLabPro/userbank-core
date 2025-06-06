# Personal Profile MCP Build Instructions

This document explains how to package `main.py` and `main_sse.py` into standalone executable files.

## File Overview

### Configuration Files
- `build_main.spec` - PyInstaller configuration file for packaging `main.py`
- `build_main_sse.spec` - PyInstaller configuration file for packaging `main_sse.py`

### Build Scripts
- `build.bat` - Windows batch script for automated build process
- `build.ps1` - PowerShell script for automated build process (recommended)

## Usage

### Method 1: Using Batch Script (Recommended)
1. Double-click to run `build.bat`
2. The script will automatically:
   - Check and install PyInstaller (if not installed)
   - Clean previous build files
   - Package both programs sequentially
   - Display build results

### Method 2: Using PowerShell Script
1. Right-click `build.ps1` and select "Run with PowerShell"
2. Or execute in PowerShell: `.\build.ps1`

### Method 3: Manual Build
If the automated scripts encounter issues, you can manually execute the following commands:

```bash
# Install PyInstaller (if not installed)
pip install pyinstaller

# Clean previous build files
rmdir /s /q dist
rmdir /s /q build

# Package main.py
pyinstaller build_main.spec --clean --noconfirm

# Package main_sse.py
pyinstaller build_main_sse.spec --clean --noconfirm
```

## Output Files

After successful packaging, two executable files will be generated in the `dist` directory:

- `UserBank_Stdio_Core.exe` - Standard MCP server based on `main.py`
- `UserBank_SSE_Core.exe` - SSE mode server based on `main_sse.py`

## Running Instructions

### UserBank_Stdio_Core.exe
- This is the standard MCP server
- Double-click to run and start the server
- Suitable for MCP client connections

### UserBank_SSE_Core.exe
- This is the SSE mode HTTP server
- Double-click to start the web server
- Default listening port is determined by configuration file
- Supports CORS and can be accessed through browsers

## Important Notes

1. **Dependency Inclusion**: The packaging process automatically includes all necessary dependency files:
   - `tools` directory and all its modules
   - `config_manager.py` configuration manager
   - `Database` directory (if exists)

2. **Hidden Imports**: Configuration files include all necessary hidden imports to ensure no module missing issues at runtime

3. **File Size**: Generated exe files may be large (typically 50-100MB), which is normal as they contain the complete Python runtime and all dependencies

4. **Runtime Environment**: Generated exe files can run on any Windows machine without requiring Python installation

5. **Configuration Files**: Ensure configuration files and database files are in the same directory as the exe files or in correct relative paths

## Troubleshooting

### If Build Fails
1. Ensure all dependencies are properly installed: `pip install -r requirements.txt`
2. Check for syntax errors or import errors
3. Review PyInstaller's detailed error messages

### If Runtime Errors Occur
1. Check if configuration file paths are correct
2. Ensure database files exist and are accessible
3. Review error messages in console output

### Common Issues
- **Module Not Found**: Check if `hiddenimports` list includes all necessary modules
- **File Path Errors**: Ensure file paths in `datas` list are correct
- **Permission Issues**: Ensure sufficient permissions to create and run exe files

## Custom Configuration

If you need to modify the packaging configuration, you can edit the `.spec` files:

- Modify the `name` field to change output filename
- Add `icon` field to set program icon
- Modify `console` field to control console window visibility
- Add additional data files in `datas`
- Add additional hidden import modules in `hiddenimports` 