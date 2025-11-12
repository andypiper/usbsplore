"""Main application window for USBSplore."""

from gi.repository import Gtk, Adw, GLib, Gio
from typing import Optional, Dict
from .usb_device import USBDevice, USBDeviceTree


@Gtk.Template(string='''
<interface>
  <template class="USBSploreWindow" parent="AdwApplicationWindow">
    <property name="default-width">900</property>
    <property name="default-height">600</property>
    <property name="title">USBSplore</property>
    <property name="content">
      <object class="AdwToolbarView">
        <child type="top">
          <object class="AdwHeaderBar">
            <property name="title-widget">
              <object class="AdwWindowTitle">
                <property name="title">USBSplore</property>
              </object>
            </property>
            <child type="end">
              <object class="GtkMenuButton" id="menu_button">
                <property name="icon-name">open-menu-symbolic</property>
                <property name="menu-model">primary_menu</property>
              </object>
            </child>
            <child type="end">
              <object class="GtkButton" id="refresh_button">
                <property name="icon-name">view-refresh-symbolic</property>
                <property name="tooltip-text">Refresh device list</property>
              </object>
            </child>
          </object>
        </child>
        <property name="content">
          <object class="AdwNavigationSplitView" id="split_view">
            <property name="sidebar-width-fraction">0.33</property>
            <property name="min-sidebar-width">280</property>
            <property name="max-sidebar-width">400</property>
            <property name="sidebar">
              <object class="AdwNavigationPage">
                <property name="title">USB Devices</property>
                <property name="child">
                  <object class="AdwToolbarView">
                    <child type="top">
                      <object class="AdwHeaderBar">
                        <property name="show-title">false</property>
                      </object>
                    </child>
                    <property name="content">
                      <object class="GtkScrolledWindow">
                        <property name="hscrollbar-policy">never</property>
                        <property name="vscrollbar-policy">automatic</property>
                        <property name="child">
                          <object class="GtkTreeView" id="device_tree">
                            <property name="headers-visible">false</property>
                          </object>
                        </property>
                      </object>
                    </property>
                  </object>
                </property>
              </object>
            </property>
            <property name="content">
              <object class="AdwNavigationPage">
                <property name="title">Device Details</property>
                <property name="child">
                  <object class="AdwToolbarView">
                    <child type="top">
                      <object class="AdwHeaderBar">
                        <property name="show-title">false</property>
                      </object>
                    </child>
                    <property name="content">
                      <object class="GtkScrolledWindow">
                        <property name="hscrollbar-policy">never</property>
                        <property name="vscrollbar-policy">automatic</property>
                        <property name="child">
                          <object class="AdwClamp">
                            <property name="maximum-size">700</property>
                            <property name="tightening-threshold">600</property>
                            <property name="child">
                              <object class="GtkBox" id="details_box">
                                <property name="orientation">vertical</property>
                                <property name="spacing">24</property>
                                <property name="margin-top">24</property>
                                <property name="margin-bottom">24</property>
                                <property name="margin-start">24</property>
                                <property name="margin-end">24</property>
                              </object>
                            </property>
                          </object>
                        </property>
                      </object>
                    </property>
                  </object>
                </property>
              </object>
            </property>
          </object>
        </property>
      </object>
    </property>
  </template>
  <menu id="primary_menu">
    <section>
      <item>
        <attribute name="label" translatable="yes">_Keyboard Shortcuts</attribute>
        <attribute name="action">win.show-help-overlay</attribute>
      </item>
      <item>
        <attribute name="label" translatable="yes">_About USBSplore</attribute>
        <attribute name="action">app.about</attribute>
      </item>
    </section>
  </menu>
  <object class="GtkShortcutsWindow" id="shortcuts_window">
    <property name="modal">true</property>
    <child>
      <object class="GtkShortcutsSection">
        <property name="section-name">shortcuts</property>
        <child>
          <object class="GtkShortcutsGroup">
            <property name="title" translatable="yes">General</property>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Show Keyboard Shortcuts</property>
                <property name="accelerator">&lt;Primary&gt;question</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Refresh Device List</property>
                <property name="accelerator">&lt;Primary&gt;r</property>
                <property name="action-name">win.refresh</property>
              </object>
            </child>
            <child>
              <object class="GtkShortcutsShortcut">
                <property name="title" translatable="yes">Quit</property>
                <property name="accelerator">&lt;Primary&gt;q</property>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </object>
</interface>
''')
class USBSploreWindow(Adw.ApplicationWindow):
    """Main application window."""

    __gtype_name__ = 'USBSploreWindow'

    device_tree = Gtk.Template.Child()
    details_box = Gtk.Template.Child()
    refresh_button = Gtk.Template.Child()
    split_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        """Initialize the main window."""
        super().__init__(**kwargs)

        self.usb_tree = USBDeviceTree()
        self.current_device: Optional[USBDevice] = None

        # Set up tree view
        self._setup_tree_view()

        # Set up actions
        self._setup_actions()

        # Connect signals
        self.refresh_button.connect('clicked', self._on_refresh_clicked)

        # Load devices
        self._load_devices()

    def _setup_actions(self):
        """Set up window actions and keyboard shortcuts."""
        # Refresh action
        refresh_action = Gio.SimpleAction.new('refresh', None)
        refresh_action.connect('activate', self._on_refresh_action)
        self.add_action(refresh_action)

        # Set up keyboard shortcuts
        app = self.get_application()
        if app:
            app.set_accels_for_action('win.refresh', ['<Primary>r'])

    def _setup_tree_view(self):
        """Set up the tree view for USB devices."""
        # Create tree store: device name, icon name, USBDevice object
        self.tree_store = Gtk.TreeStore(str, str, object)
        self.device_tree.set_model(self.tree_store)

        # Create column
        column = Gtk.TreeViewColumn()

        # Icon renderer
        icon_renderer = Gtk.CellRendererPixbuf()
        column.pack_start(icon_renderer, False)
        column.add_attribute(icon_renderer, 'icon-name', 1)

        # Text renderer
        text_renderer = Gtk.CellRendererText()
        column.pack_start(text_renderer, True)
        column.add_attribute(text_renderer, 'text', 0)

        self.device_tree.append_column(column)

        # Connect selection changed signal
        selection = self.device_tree.get_selection()
        selection.connect('changed', self._on_selection_changed)

    def _load_devices(self):
        """Load USB devices into the tree view."""
        self.tree_store.clear()
        root_devices = self.usb_tree.refresh()

        for device in root_devices:
            self._add_device_to_tree(device, None)

        # Expand all nodes
        self.device_tree.expand_all()

    def _add_device_to_tree(self, device: USBDevice, parent_iter: Optional[Gtk.TreeIter]):
        """Add a device and its children to the tree.

        Args:
            device: USB device to add
            parent_iter: Parent tree iterator or None for root
        """
        # Choose icon based on device type
        if device.is_root_hub():
            icon = 'network-wired-symbolic'
        else:
            # Use device class to choose icon
            device_class = device.device_class or '00'
            icon = self._get_icon_for_device_class(device_class)

        # Add to tree
        iter = self.tree_store.append(parent_iter, [
            device.get_display_name(),
            icon,
            device
        ])

        # Add children recursively
        for child in device.children:
            self._add_device_to_tree(child, iter)

    def _get_icon_for_device_class(self, device_class: str) -> str:
        """Get icon name for device class.

        Args:
            device_class: USB device class code

        Returns:
            Icon name
        """
        # USB device class codes
        class_icons = {
            '01': 'audio-headphones-symbolic',      # Audio
            '02': 'network-wired-symbolic',         # Communications
            '03': 'input-keyboard-symbolic',        # HID
            '05': 'input-dialpad-symbolic',         # Physical
            '06': 'camera-photo-symbolic',          # Image
            '07': 'printer-symbolic',               # Printer
            '08': 'drive-harddisk-symbolic',        # Mass Storage
            '09': 'network-wired-symbolic',         # Hub
            '0a': 'network-wired-symbolic',         # CDC Data
            '0b': 'smartcard-symbolic',             # Smart Card
            '0d': 'security-high-symbolic',         # Content Security
            '0e': 'camera-video-symbolic',          # Video
            '0f': 'security-medium-symbolic',       # Personal Healthcare
            '10': 'audio-headphones-symbolic',      # Audio/Video
            '11': 'computer-symbolic',              # Billboard
            'e0': 'network-wireless-symbolic',      # Wireless
            'ef': 'network-wired-symbolic',         # Miscellaneous
            'fe': 'application-x-executable-symbolic',  # Application Specific
            'ff': 'preferences-system-symbolic',    # Vendor Specific
        }

        return class_icons.get(device_class, 'drive-removable-media-symbolic')

    def _on_selection_changed(self, selection: Gtk.TreeSelection):
        """Handle tree selection change.

        Args:
            selection: Tree selection object
        """
        model, tree_iter = selection.get_selected()
        if tree_iter is None:
            self._clear_details()
            return

        device = model.get_value(tree_iter, 2)
        self.current_device = device
        self._show_device_details(device)

    def _show_device_details(self, device: USBDevice):
        """Show device details in the details panel.

        Args:
            device: USB device to show details for
        """
        # Clear existing details without showing placeholder
        self._clear_details_content()

        # Create header
        header = Adw.PreferencesGroup()
        header.set_title(device.get_display_name())

        if device.manufacturer:
            header.set_description(device.manufacturer)

        self.details_box.append(header)

        # Basic information
        basic_group = Adw.PreferencesGroup()
        basic_group.set_title('Basic information')
        self.details_box.append(basic_group)

        # Add property rows
        properties = [
            ('Vendor ID', device.vendor_id, True),
            ('Product ID', device.product_id, True),
            ('Manufacturer', device.manufacturer, False),
            ('Product', device.product),
            ('Serial number', device.serial, True),
        ]

        for prop_info in properties:
            title = prop_info[0]
            value = prop_info[1]
            copyable = prop_info[2] if len(prop_info) > 2 else False

            if value:
                row = Adw.ActionRow()
                row.set_title(title)
                row.set_subtitle(value)
                row.set_subtitle_selectable(True)

                # Add copy button for copyable values
                if copyable:
                    copy_button = Gtk.Button()
                    copy_button.set_icon_name('edit-copy-symbolic')
                    copy_button.set_valign(Gtk.Align.CENTER)
                    copy_button.add_css_class('flat')
                    copy_button.set_tooltip_text(f'Copy {title}')
                    copy_button.connect('clicked', lambda b, v=value: self._copy_to_clipboard(v))
                    row.add_suffix(copy_button)

                basic_group.add(row)

        # Connection information
        conn_group = Adw.PreferencesGroup()
        conn_group.set_title('Connection information')
        self.details_box.append(conn_group)

        connection_props = [
            ('Bus number', device.bus_number),
            ('Device number', device.device_number),
            ('Speed', device.speed),
            ('USB version', device.version),
            ('Device class', device.device_class),
            ('Maximum power', device.max_power),
        ]

        for title, value in connection_props:
            if value:
                row = Adw.ActionRow()
                row.set_title(title)
                row.set_subtitle(value)
                row.set_subtitle_selectable(True)
                conn_group.add(row)

        # Driver/Module information
        if device.driver or device.module:
            driver_group = Adw.PreferencesGroup()
            driver_group.set_title('Driver information')
            self.details_box.append(driver_group)

            driver_props = [
                ('Kernel driver', device.driver),
                ('Kernel module', device.module),
            ]

            for title, value in driver_props:
                if value:
                    row = Adw.ActionRow()
                    row.set_title(title)
                    row.set_subtitle(value)
                    row.set_subtitle_selectable(True)

                    # Add copy button
                    copy_button = Gtk.Button()
                    copy_button.set_icon_name('edit-copy-symbolic')
                    copy_button.set_valign(Gtk.Align.CENTER)
                    copy_button.add_css_class('flat')
                    copy_button.set_tooltip_text(f'Copy {title}')
                    copy_button.connect('clicked', lambda b, v=value: self._copy_to_clipboard(v))
                    row.add_suffix(copy_button)

                    driver_group.add(row)

        # Additional properties
        all_props = device.get_all_properties()
        if all_props:
            # Find properties not already shown
            shown_keys = {
                'idVendor', 'idProduct', 'manufacturer', 'product', 'serial',
                'busnum', 'devnum', 'speed', 'version', 'bDeviceClass', 'bMaxPower',
                'driver', 'module'
            }
            additional_props = {k: v for k, v in all_props.items() if k not in shown_keys}

            if additional_props:
                extra_group = Adw.PreferencesGroup()
                extra_group.set_title('Additional properties')
                self.details_box.append(extra_group)

                for key, value in sorted(additional_props.items()):
                    row = Adw.ActionRow()
                    row.set_title(key)
                    row.set_subtitle(value)
                    row.set_subtitle_selectable(True)
                    extra_group.add(row)

    def _clear_details_content(self):
        """Clear the details panel content."""
        # Remove all children
        while True:
            child = self.details_box.get_first_child()
            if child is None:
                break
            self.details_box.remove(child)

    def _clear_details(self):
        """Clear the details panel and show placeholder."""
        self._clear_details_content()

        # Add placeholder
        status_page = Adw.StatusPage()
        status_page.set_icon_name('drive-removable-media-symbolic')
        status_page.set_title('No device selected')
        status_page.set_description('Select a USB device from the list to view its details')
        self.details_box.append(status_page)

    def _on_refresh_clicked(self, button: Gtk.Button):
        """Handle refresh button click.

        Args:
            button: Refresh button
        """
        self._do_refresh()

    def _on_refresh_action(self, action: Gio.SimpleAction, param):
        """Handle refresh action (keyboard shortcut).

        Args:
            action: The action
            param: Action parameters
        """
        self._do_refresh()

    def _do_refresh(self):
        """Perform device list refresh."""
        self._load_devices()
        self._clear_details()

    def _copy_to_clipboard(self, text: str):
        """Copy text to clipboard.

        Args:
            text: Text to copy
        """
        clipboard = self.get_clipboard()
        clipboard.set(text)
