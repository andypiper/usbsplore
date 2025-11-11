#!/usr/bin/env python3
"""Development launcher for USBSplore.

This script allows you to run USBSplore directly from the source tree
without installing it system-wide.
"""

import os
import sys
import signal
from pathlib import Path

# Get the source directory
SOURCE_DIR = Path(__file__).parent.resolve()
SRC_DIR = SOURCE_DIR / 'src'

# Add src directory to path
sys.path.insert(0, str(SRC_DIR))

# Handle Ctrl+C gracefully
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Set up GSettings schema path for development
# This requires compiling the schema first
schema_dir = SOURCE_DIR / 'data'
if schema_dir.exists():
    os.environ['GSETTINGS_SCHEMA_DIR'] = str(schema_dir)

if __name__ == '__main__':
    import gi

    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')

    from usbsplore import main
    sys.exit(main.main())
