project('usbsplore',
  version: '1.0.0',
  meson_version: '>= 0.59.0',
  license: 'GPL-3.0-or-later',
)

i18n = import('i18n')
gnome = import('gnome')
python = import('python')

# Project information
project_id = 'com.github.andypiper.USBSplore'
project_name = 'USBSplore'

# Directories
prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / project_id
pythondir = python.find_installation('python3').get_path('purelib')

# Dependencies
dependency('gtk4', version: '>= 4.12')
dependency('libadwaita-1', version: '>= 1.4')
dependency('pygobject-3.0', version: '>= 3.46')

# Subdirectories
subdir('data')
subdir('src')
subdir('po')

# Post-install scripts
gnome.post_install(
  gtk_update_icon_cache: true,
  glib_compile_schemas: true,
  update_desktop_database: true,
)
