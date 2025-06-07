# Personal Profile MCP Build Instructions

This document explains how to package `main.py` and `main_sse.py` into standalone executable files.

## File Overview

### Configuration Files
- `build_main.spec` - PyInstaller configuration file for packaging `main.py`
- `build_main_sse.spec` - PyInstaller configuration file for packaging `main_sse.py`

### Build Scripts
- `build.bat` - Windows batch script for automated build process
- `build.ps1` - PowerShell script for automated build process (Windows recommended)
- `build.sh` - Shell script for automated build process (macOS recommended)

## Windows Usage

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

## macOS Usage

### Method 1: Using Shell Script (Recommended)
1. Open terminal and navigate to project directory
2. Execute the following commands:
```bash
chmod +x build.sh
./build.sh
```
3. The script will automatically:
   - Check and install PyInstaller (if not installed)
   - Clean previous build files
   - Package both programs sequentially
   - Display build results

### Method 2: Manual Build
If the automated script encounters issues, you can manually execute the following commands:

```bash
# Install PyInstaller (if not installed)
pip3 install pyinstaller

# Clean previous build files
rm -rf dist
rm -rf build

# Package main.py
pyinstaller build_main.spec --clean --noconfirm

# Package main_sse.py
pyinstaller build_main_sse.spec --clean --noconfirm
```

## Output Files

### Windows
After successful packaging, two executable files will be generated in the `dist` directory:

- `UserBank_Stdio_Core.exe` - Standard MCP server based on `main.py`
- `UserBank_SSE_Core.exe` - SSE mode server based on `main_sse.py`

### macOS
After successful packaging, two executable files will be generated in the `dist` directory:

- `UserBank_Stdio_Core` - Standard MCP server based on `main.py`
- `UserBank_SSE_Core` - SSE mode server based on `main_sse.py`

## Running Instructions

### Windows

#### UserBank_Stdio_Core.exe
- This is the standard MCP server
- Double-click to run and start the server
- Suitable for MCP client connections

#### UserBank_SSE_Core.exe
- This is the SSE mode HTTP server
- Double-click to start the web server
- Default listening port is determined by configuration file
- Supports CORS and can be accessed through browsers

### macOS

#### UserBank_Stdio_Core
- This is the standard MCP server
- Run in terminal: `./dist/UserBank_Stdio_Core`
- Suitable for MCP client connections

#### UserBank_SSE_Core
- This is the SSE mode HTTP server
- Run in terminal: `./dist/UserBank_SSE_Core`
- Default listening port is determined by configuration file
- Supports CORS and can be accessed through browsers

## Important Notes

1. **Dependency Inclusion**: The packaging process automatically includes all necessary dependency files:
   - `tools` directory and all its modules
   - `config_manager.py` configuration manager
   - `Database` directory (if exists)

2. **Hidden Imports**: Configuration files include all necessary hidden imports to ensure no module missing issues at runtime

3. **File Size**: Generated executable files may be large (typically 50-100MB), which is normal as they contain the complete Python runtime and all dependencies

4. **Runtime Environment**:
   - Windows: Generated exe files can run on any Windows machine without requiring Python installation
   - macOS: Generated executables can run on any macOS machine without requiring Python installation

5. **Configuration Files**: Ensure configuration files and database files are in the same directory as the executable files or in correct relative paths

## Troubleshooting

### If Build Fails
1. Ensure all dependencies are properly installed:
   - Windows: `pip install -r requirements.txt`
   - macOS: `pip3 install -r requirements.txt`
2. Check for syntax errors or import errors
3. Review PyInstaller's detailed error messages

### If Runtime Errors Occur
1. Check if configuration file paths are correct
2. Ensure database files exist and are accessible
3. Review error messages in console/terminal output

### Common Issues
- **Module Not Found**: Check if `hiddenimports` list includes all necessary modules
- **File Path Errors**: Ensure file paths in `datas` list are correct
- **Permission Issues**:
  - Windows: Ensure sufficient permissions to create and run exe files
  - macOS: Ensure sufficient permissions to create and run executables, may need to use `chmod +x` command

## Custom Configuration

If you need to modify the packaging configuration, you can edit the `.spec` files:

- Modify the `name` field to change output filename
- Add `icon` field to set program icon
- Modify `console` field to control console window visibility
- Add additional data files in `datas`
- Add additional hidden import modules in `hiddenimports`

## Security Considerations

1. **Code Signing**:
   - Windows: Digital certificate signing recommended
   - macOS: Code signing recommended to avoid security warnings
2. **Permission Settings**: Ensure application has appropriate file system access permissions
3. **Firewall Settings**: If using SSE mode, ensure firewall allows application network access

## Performance Optimization

1. **UPX Compression**: UPX compression enabled by default to reduce file size
2. **Resource Optimization**: Resource inclusion can be optimized by modifying `.spec` files
3. **Launch Optimization**: Launch time can be optimized by adjusting PyInstaller parameters 