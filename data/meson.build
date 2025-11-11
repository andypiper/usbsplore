# Desktop file
desktop_file = i18n.merge_file(
  input: configure_file(
    input: 'com.github.andypiper.USBSplore.desktop.in',
    output: '@BASENAME@',
    configuration: configuration_data(),
  ),
  output: 'com.github.andypiper.USBSplore.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: datadir / 'applications',
)

# Validate desktop file
desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

# AppStream metadata
appstream_file = i18n.merge_file(
  input: configure_file(
    input: 'com.github.andypiper.USBSplore.appdata.xml.in',
    output: '@BASENAME@',
    configuration: configuration_data(),
  ),
  output: 'com.github.andypiper.USBSplore.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: datadir / 'metainfo',
)

# Validate AppStream metadata
appstreamcli = find_program('appstreamcli', required: false)
if appstreamcli.found()
  test('Validate appstream file', appstreamcli, args: ['validate', '--no-net', appstream_file])
endif

# GSettings schema
install_data('com.github.andypiper.USBSplore.gschema.xml',
  install_dir: datadir / 'glib-2.0/schemas'
)

# Compile schemas for testing
compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
    compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif
