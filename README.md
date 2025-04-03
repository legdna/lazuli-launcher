# **Oraclès Launcher**

Oraclès Launcher is the official launcher for the Oraclès Discord server. It enables players to seamlessly connect and play on the Oraclès Minecraft server and the Terraclès Terraria server.

---

## **Table of Contents**
1. [Development Environment Setup](#development-environment-setup)
    - [Dependencies for Windows 10/11 MSYS2 (UCRT64)](#dependencies-for-windows-1011-msys2-ucrt64)
2. [Building the Application for Windows](#building-the-application-for-windows)
3. [License](#license)

---

## **Development Environment Setup**

To contribute to or develop this program, you need to set up your development environment with the following dependencies.

### **Dependencies for Windows 10/11 MSYS2 (UCRT64)**

The following dependencies must be installed in the **MSYS2 UCRT64 environment**. If MSYS2 is not installed, download it from [MSYS2.org](https://www.msys2.org/) and follow their setup instructions.

#### **System Dependencies**
Run these commands in the MSYS2 UCRT64 terminal:
```bash
pacman -Sy mingw-w64-ucrt-x86_64-gtk4
pacman -Sy mingw-w64-ucrt-x86_64-libadwaita
pacman -Sy mingw-w64-ucrt-x86_64-python
pacman -Sy mingw-w64-ucrt-x86_64-python-gobject
pacman -Sy mingw-w64-ucrt-x86_64-python-psutil
pacman -Sy mingw-w64-ucrt-x86_64-python-nuitka
pacman -Sy mingw-w64-ucrt-x86_64-toolchain base-devel
pacman -Sy mingw-w64-ucrt-x86_64-python-pip
```

#### **Python Dependencies**
Once Python is installed via MSYS2, install the required Python packages using `pip`:
```bash
pip install darkdetect
pip install discord-rich-presence
pip install requests
pip install minecraft_launcher_lib
pip install pillow
pip install pywinstyles
pip install pygobject-stubs
```

---

## **Building the Application for Windows**

Follow these steps to build the application into a standalone executable for Windows using Nuitka:

### **1. Prepare the Environment**
Ensure all dependencies are installed as described above.

### **2. Compile GResource Files**

Since this application uses GResource for resource management, you need to compile the .gresource.xml file into a .gresource binary. Use the following command:

```bash
glib-compile-resources --target=data/oracles.gresource --sourcedir=data data/oracles.gresource.xml
```

### **3. Build the application**
To compile the application into a standalone executable for Windows, use the provided script build_for_windows.cmd:
```powershell
.\build_for_windows.cmd
```

### **4. Output**
The compiled executable will be located in the `oracles.dist/` directory.

---

## **License**

This project is licensed under the terms of the **GNU General Public License v3.0 (GPLv3)**.  
You can find a copy of the license in the `LICENSE` file or at [https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).

### Key Points of GPLv3:
- You are free to use, modify, and distribute this software.
- Any modifications or derivative works must also be licensed under GPLv3.
- The source code must be made available when distributing binaries.
