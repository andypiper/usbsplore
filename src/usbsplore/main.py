"""USBSplore - A modern GNOME USB device viewer.

This application displays USB devices connected to your system in a
tree view with detailed information about each device.
"""

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

from .window import USBSploreWindow


class USBSploreApplication(Adw.Application):
    """Main application class."""

    def __init__(self):
        """Initialize the application."""
        super().__init__(
            application_id='com.github.andypiper.USBSplore',
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        """Activate the application."""
        win = self.props.active_window
        if not win:
            win = USBSploreWindow(application=self)
        win.present()

    def on_quit_action(self, action, param):
        """Handle quit action.

        Args:
            action: The action
            param: Action parameters
        """
        self.quit()

    def on_about_action(self, action, param):
        """Show about dialog.

        Args:
            action: The action
            param: Action parameters
        """
        about = Adw.AboutDialog()
        about.set_application_name('USBSplore')
        about.set_version('1.0.0')
        about.set_developer_name('Andy Piper')
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website('https://github.com/andypiper/usbsplore')
        about.set_issue_url('https://github.com/andypiper/usbsplore/issues')
        about.set_developers(['Andy Piper'])
        about.set_copyright('© 2025 Andy Piper')
        about.set_application_icon('com.github.andypiper.USBSplore')
        about.set_comments(
            'A modern GNOME application for viewing USB devices connected to your system'
        )

        # Show the about dialog
        about.present(self.props.active_window)

    def create_action(self, name, callback, shortcuts=None):
        """Create an application action.

        Args:
            name: Action name
            callback: Callback function
            shortcuts: Optional keyboard shortcuts
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


def main(version='1.0.0'):
    """Run the application.

    Args:
        version: Application version
    """
    app = USBSploreApplication()
    return app.run(sys.argv)


if __name__ == '__main__':
    main()
