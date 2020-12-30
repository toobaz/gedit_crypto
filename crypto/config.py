from gi.repository import Gio
from os import path

# FIXME: detect
SYSTEM_INSTALL = False

SCHEMA_ID = "org.gnome.gedit.plugins.crypto"


def load_config():
    if SYSTEM_INSTALL:
        settings = Gio.Settings.new(SCHEMA_ID)
    else:
        import subprocess

        schema_path = path.join(path.dirname(__file__), "schemas")
        subprocess.call(['glib-compile-schemas', schema_path])

        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            schema_path,
            Gio.SettingsSchemaSource.get_default(),
            False)
        schema = schema_source.lookup(SCHEMA_ID, False)
        settings = Gio.Settings.new_full(schema, None, None)
    return settings
