from gi.repository import Gio, Gtk

class ConfigDialog(Gtk.Dialog):

    def __init__(self, config = None):
        self.config = config

        Gtk.Dialog.__init__(self,
                            _("Settings"),
                            None,
                            Gtk.DialogFlags.DESTROY_WITH_PARENT)

        self.set_resizable(False)

        close_button = self.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        close_button.grab_default()
        close_button.connect_object("clicked", Gtk.Widget.destroy, self)

        main_box = Gtk.VBox(False, 0)
        main_box.set_border_width(12)

        config_box = Gtk.VBox(False, 6)
        config_box.set_border_width(6)

        checkbox_label = _("Show popup menu (needs restart)")
        showpopup_checkbox = Gtk.CheckButton(checkbox_label,
                                              use_underline = True)
        showpopup_checkbox.connect('clicked',
                                    self.update_setting,
                                    'showpopup')
        showpopup_checkbox.set_active(self.config.get_bool('showpopup'))

        config_box.pack_start(showpopup_checkbox, True, True, 0)

        main_box.pack_start(config_box, True, True, 0)

        self.vbox.pack_start(main_box, True, True, 0)

        self.show_all()

    def update_setting(self, widget, data = None):
        self.config.set_bool(data, widget.get_active())



class ConfigSettings():
    SCHEMA_ID = "org.gnome.gedit.plugins.crypto"

    def __init__(self):
        self.settings = Gio.Settings.new(self.SCHEMA_ID)

    def assert_key(self, key):
        if key not in self.settings.list_keys():
            raise Exception('unknown gsettings key')

    def get_bool(self, key):
        self.assert_key(key);
        return self.settings.get_boolean(key);

    def set_bool(self, key, val):
        self.assert_key(key);
        self.settings.set_boolean(key, val);
