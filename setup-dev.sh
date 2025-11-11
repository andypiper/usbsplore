#!/bin/bash
# Setup script for development environment
# This compiles the GSettings schema locally for testing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"

echo "Setting up USBSplore development environment..."

# Compile GSettings schema
if command -v glib-compile-schemas &> /dev/null; then
    echo "Compiling GSettings schema..."
    glib-compile-schemas "$DATA_DIR"
    echo "✓ Schema compiled"
else
    echo "⚠ glib-compile-schemas not found - GSettings will not be available"
fi

# Make the dev launcher executable
chmod +x "$SCRIPT_DIR/run-dev.py"
echo "✓ Development launcher is now executable"

echo ""
echo "Development environment ready!"
echo "Run the application with: ./run-dev.py"
