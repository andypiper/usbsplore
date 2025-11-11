# USBSplore

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GNOME](https://img.shields.io/badge/GNOME-47%2F48%2F49-4A86CF?logo=gnome)](https://www.gnome.org/)

> A modern GNOME application for viewing USB devices connected to your system

USBSplore is a GTK4/libadwaita application that displays USB devices in an intuitive tree view with detailed information about each device. Inspired by [usbview](https://github.com/gregkh/usbview/) by Greg Kroah-Hartman, it brings a modern interface following the GNOME Human Interface Guidelines.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

USBSplore was created to provide a modern, native GNOME application for viewing USB device information. It reads device data from the Linux sysfs filesystem and presents it in an accessible way following GNOME's design principles.

The application is built for GNOME 47/48/49 using GTK 4, libadwaita, Python 3, and Meson. It provides an intuitive tree view of the USB device hierarchy with detailed information panels, refresh capabilities, and a responsive adaptive layout following the GNOME Human Interface Guidelines.

## Install

**Dependencies**: Python 3.10+, GTK 4.12+, libadwaita 1.4+, PyGObject 3.46+, Meson 0.59.0+

Install dependencies on your distribution:

```bash
# Fedora/RHEL
sudo dnf install gtk4 libadwaita python3-gobject meson

# Ubuntu/Debian
sudo apt install libgtk-4-dev libadwaita-1-dev python3-gi meson

# Arch Linux
sudo pacman -S gtk4 libadwaita python-gobject meson
```

Build and install from source:

```bash
git clone https://github.com/andypiper/usbsplore.git
cd usbsplore
meson setup builddir
meson compile -C builddir
sudo meson install -C builddir
```

## Usage

```bash
usbsplore
```

The application displays USB devices in a tree view on the left. Click any device to see detailed information in the right panel. Use the refresh button to update the device list.

**Keyboard Shortcuts:**
- `Ctrl+Q` - Quit
- `Ctrl+?` - Show shortcuts

**Development/Testing without installation:**

```bash
# Setup development environment (compiles GSettings schema)
./setup-dev.sh

# Run directly from source tree
./run-dev.py
```

## Maintainers

[@andypiper](https://github.com/andypiper)

## Contributing

PRs accepted! For major changes, please open an issue first to discuss what you would like to change.

**Questions?** Open an issue or contact the maintainer.

**Development requirements:**
- Follow [PEP 8](https://pep8.org/) for Python code
- Follow [GNOME HIG](https://developer.gnome.org/hig/) for UI design
- Run tests with `meson test -C builddir`

## License

[GPL-3.0-or-later](LICENSE) © 2025 Andy Piper
