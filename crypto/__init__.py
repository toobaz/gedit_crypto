import gi
gi.require_version('Gedit', '3.0')
from gi.repository import GObject, Gedit, Gio, Gtk
import os
from .encrypter import Encrypter

__version__ = '0.5'

ACTIONS = {'encrypt' : _("Encrypt document"),
           'decrypt' : _("Decrypt document")}

class GeditCrypto(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "CryptoPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self.window = None
        # Build encrypter when needed to not slow down Gedit startup
        self.enc = None

    def do_activate(self):
        try:
            self.initialize()
        except Exception as msg:
            import traceback
            print("Error initializing \"Crypto\" plugin")
            print(traceback.print_exc())

    def initialize(self):
        from .crypto_ui import Ui

        self.data_dir = self.plugin_info.get_data_dir()

        ui_path = os.path.join( self.data_dir, "crypto.glade" )
        self.ui = Ui( "gedit-crypto", ui_path )
        self.ui.connect_signals( self )

        self.actions = {}

        for action_name in ACTIONS:
            action = Gio.SimpleAction(name=action_name)
            self.actions[action_name] = action
            action.connect('activate', getattr(self, action_name))
            self.window.add_action(action)
            self.window.lookup_action(action_name).set_enabled(True)

        self.window.connect('tab-added', self.on_window_tab_added)

        for view in self.window.get_views():
            self.connect_view(view)

    def on_window_tab_added(self, window, tab):
        self.connect_view(tab.get_view())

    def do_deactivate(self):
        """
        Remove actions.
        """
        while self.actions:
            name, action = self.actions.popitem()
            self.window.remove_action(name)

    def do_update_state(self):
        pass

    def connect_view(self, view):
        view.connect('populate-popup', self.on_view_populate_popup)

    def on_view_populate_popup(self, view, menu):
        separator = Gtk.SeparatorMenuItem()
        separator.show();
        menu.append(separator)

        for action in ACTIONS:
            menu_item = Gtk.MenuItem(ACTIONS[action])
            menu_item.connect('activate', getattr(self, action))
            menu_item.show();
            menu.append(menu_item)

    def encrypt(self, *args):
        if self.enc == None:
            self.enc = Encrypter( self.ui )

        cleartext = self.get_current_text()

        encrypted = self.enc.encrypt( cleartext )

        if not encrypted:
            return

        self.show_in_new_document( encrypted )

    def decrypt(self, *args):
        if self.enc == None:
            self.enc = Encrypter( self.ui )

        encrypted_text = self.get_current_text()

        cleartext = self.enc.decrypt( encrypted_text )

        if not cleartext:
            return

        self.show_in_new_document( cleartext )

    def get_current_text(self):
        view = self.window.get_active_view()
        doc = view.get_buffer()
        start = doc.get_start_iter()
        end = doc.get_end_iter()
        return doc.get_text( start, end, False )

    def show_in_new_document(self, text):
        self.window.create_tab( True )
        new_view = self.window.get_active_view()
        new_doc = new_view.get_buffer()
        new_doc.set_text( text )


class GeditCryptoApp(GObject.Object, Gedit.AppActivatable):
    __gtype_name__ = "GeditCryptoApp"
    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)
        self.app = None

    def do_activate(self):
        self.submenu_ext = self.extend_menu("tools-section-1")
        submenu = Gio.Menu()
        item = Gio.MenuItem.new_submenu(_("Encrypt/decrypt"), submenu)
        self.submenu_ext.append_menu_item(item)

        for action in ACTIONS:
            item = Gio.MenuItem.new(ACTIONS[action], "win.%s" % action)
            submenu.append_item(item)

    def do_deactivate(self):
        del self.submenu_ext
