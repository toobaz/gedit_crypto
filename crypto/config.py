from gi.repository import Gio
from os.path import expanduser

# FIXME: detect
SYSTEM_INSTALL = False

SCHEMA_ID = "org.gnome.gedit.plugins.crypto"

def load_config():
    if SYSTEM_INSTALL:
        settings = Gio.Settings.new(SCHEMA_ID)
    else:
        # TODO: install and compile automatically
        schema_path = expanduser("~/.local/share/gedit-crypto/schemas")
        schema_source = Gio.SettingsSchemaSource.new_from_directory(
                                    schema_path,
                                    Gio.SettingsSchemaSource.get_default(),
                                    False)
        schema = schema_source.lookup(SCHEMA_ID, False)
        settings = Gio.Settings.new_full(schema, None, None)
    return settings
