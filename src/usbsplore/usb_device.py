"""USB Device information collector.

This module reads USB device information from sysfs and provides
a structured representation of the USB device hierarchy.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import re


class USBDevice:
    """Represents a USB device with its properties."""

    def __init__(self, sysfs_path: str):
        """Initialize USB device from sysfs path.

        Args:
            sysfs_path: Path to device in /sys/bus/usb/devices/
        """
        self.sysfs_path = Path(sysfs_path)
        self.name = self.sysfs_path.name
        self.children: List[USBDevice] = []
        self._properties: Dict[str, str] = {}
        self._load_properties()

    def _read_sysfs_attr(self, attr: str) -> Optional[str]:
        """Read a sysfs attribute file.

        Args:
            attr: Attribute name to read

        Returns:
            Attribute value or None if not readable
        """
        try:
            attr_path = self.sysfs_path / attr
            if attr_path.exists():
                with open(attr_path, 'r') as f:
                    return f.read().strip()
        except (IOError, PermissionError):
            pass
        return None

    def _load_properties(self):
        """Load device properties from sysfs."""
        # Basic device properties
        attrs = [
            'idVendor', 'idProduct', 'manufacturer', 'product',
            'serial', 'bDeviceClass', 'bDeviceSubClass', 'bDeviceProtocol',
            'bNumInterfaces', 'bConfigurationValue', 'bMaxPower',
            'speed', 'version', 'devpath', 'busnum', 'devnum',
            'maxchild', 'quirks', 'avoid_reset_quirk', 'authorized',
            'bmAttributes', 'bMaxPacketSize0', 'bNumConfigurations',
            'urbnum'
        ]

        for attr in attrs:
            value = self._read_sysfs_attr(attr)
            if value:
                self._properties[attr] = value

        # Load driver/module information
        self._load_driver_info()

    def _load_driver_info(self):
        """Load kernel driver and module information."""
        # Check for driver symlink
        driver_path = self.sysfs_path / 'driver'
        if driver_path.exists() and driver_path.is_symlink():
            # Get driver name from symlink target
            driver_name = driver_path.resolve().name
            self._properties['driver'] = driver_name

            # Try to get module name
            module_path = driver_path / 'module'
            if module_path.exists() and module_path.is_symlink():
                module_name = module_path.resolve().name
                self._properties['module'] = module_name

    def add_child(self, device: 'USBDevice'):
        """Add a child device to this device."""
        self.children.append(device)

    @property
    def vendor_id(self) -> Optional[str]:
        """Get vendor ID."""
        return self._properties.get('idVendor')

    @property
    def product_id(self) -> Optional[str]:
        """Get product ID."""
        return self._properties.get('idProduct')

    @property
    def manufacturer(self) -> Optional[str]:
        """Get manufacturer name."""
        return self._properties.get('manufacturer')

    @property
    def product(self) -> Optional[str]:
        """Get product name."""
        return self._properties.get('product')

    @property
    def serial(self) -> Optional[str]:
        """Get serial number."""
        return self._properties.get('serial')

    @property
    def speed(self) -> Optional[str]:
        """Get device speed."""
        return self._properties.get('speed')

    @property
    def device_class(self) -> Optional[str]:
        """Get device class."""
        return self._properties.get('bDeviceClass')

    @property
    def bus_number(self) -> Optional[str]:
        """Get bus number."""
        return self._properties.get('busnum')

    @property
    def device_number(self) -> Optional[str]:
        """Get device number."""
        return self._properties.get('devnum')

    @property
    def max_power(self) -> Optional[str]:
        """Get maximum power consumption."""
        return self._properties.get('bMaxPower')

    @property
    def version(self) -> Optional[str]:
        """Get USB version."""
        return self._properties.get('version')

    @property
    def driver(self) -> Optional[str]:
        """Get kernel driver name."""
        return self._properties.get('driver')

    @property
    def module(self) -> Optional[str]:
        """Get kernel module name."""
        return self._properties.get('module')

    def get_display_name(self) -> str:
        """Get a human-readable display name for the device."""
        # Try product name first
        if self.product:
            return self.product

        # Try manufacturer + product
        if self.manufacturer:
            return self.manufacturer

        # Fall back to vendor:product IDs
        if self.vendor_id and self.product_id:
            return f"USB Device {self.vendor_id}:{self.product_id}"

        # Last resort: use the sysfs name
        if 'usb' in self.name:
            return f"USB Root Hub ({self.name})"
        return f"USB Device ({self.name})"

    def get_all_properties(self) -> Dict[str, str]:
        """Get all device properties."""
        return self._properties.copy()

    def is_root_hub(self) -> bool:
        """Check if this device is a root hub."""
        return bool(re.match(r'^usb\d+$', self.name))


class USBDeviceTree:
    """Builds and manages the USB device tree."""

    def __init__(self):
        """Initialize USB device tree."""
        self.root_devices: List[USBDevice] = []
        self._device_map: Dict[str, USBDevice] = {}

    def scan(self) -> List[USBDevice]:
        """Scan for USB devices and build the tree.

        Returns:
            List of root USB devices (root hubs)
        """
        usb_devices_path = Path('/sys/bus/usb/devices')

        if not usb_devices_path.exists():
            return []

        # First pass: create all device objects
        for device_path in sorted(usb_devices_path.iterdir()):
            if device_path.is_symlink():
                real_path = device_path.resolve()
                device_name = device_path.name

                # Skip interface entries (contain colons)
                if ':' in device_name:
                    continue

                device = USBDevice(str(real_path))
                self._device_map[device_name] = device

        # Second pass: build hierarchy
        for device_name, device in self._device_map.items():
            if device.is_root_hub():
                # This is a root hub
                self.root_devices.append(device)
            else:
                # Find parent by parsing device name
                # Device names are like: 1-1, 1-1.2, 1-1.2.3
                parent_name = self._get_parent_name(device_name)
                if parent_name and parent_name in self._device_map:
                    parent = self._device_map[parent_name]
                    parent.add_child(device)

        return self.root_devices

    def _get_parent_name(self, device_name: str) -> Optional[str]:
        """Get parent device name from child device name.

        Args:
            device_name: Child device name (e.g., '1-1.2.3')

        Returns:
            Parent device name (e.g., '1-1.2') or None
        """
        # Root hubs (usb1, usb2, etc.) have no parent
        if device_name.startswith('usb'):
            return None

        # First level devices (1-1, 2-1, etc.)
        if re.match(r'^\d+-\d+$', device_name):
            # Parent is the root hub
            bus_num = device_name.split('-')[0]
            return f'usb{bus_num}'

        # Deeper level devices (1-1.2, 1-1.2.3, etc.)
        if '.' in device_name:
            # Remove the last port number
            return device_name.rsplit('.', 1)[0]

        return None

    def refresh(self) -> List[USBDevice]:
        """Refresh the device tree.

        Returns:
            Updated list of root USB devices
        """
        self.root_devices.clear()
        self._device_map.clear()
        return self.scan()
