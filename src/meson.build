moduledir = pkgdatadir / 'usbsplore'

# Install Python modules
python_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'usb_device.py',
]

install_data(python_sources, install_dir: moduledir)

# Create launcher script
launcher_conf = configuration_data()
launcher_conf.set('PYTHON', python.find_installation('python3').full_path())
launcher_conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'usbsplore.in',
  output: 'usbsplore',
  configuration: launcher_conf,
  install: true,
  install_dir: bindir,
  install_mode: 'rwxr-xr-x'
)
