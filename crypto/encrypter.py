import dbus
from gi.repository import GLib, Gtk

class Encrypter(object):
    def __init__(self, ui):
        self.run
        self.ui = ui
        self.bus = dbus.SessionBus()
        self.init_dbus()
    
    def run(self):
    
        
        
        
        
        self.quit()
        
    def init_dbus(self):
        keys_proxy = self.bus.get_object('org.gnome.seahorse', '/org/gnome/seahorse/keys')
        key_service = dbus.Interface(keys_proxy, 'org.gnome.seahorse.KeyService')
        
        types = key_service.GetKeyTypes()
        print "GetKeyTypes(): ", types

        path = key_service.GetKeyset(types[0])
        print "GetKeySet(): ", path
        
        proxy_obj = self.bus.get_object('org.gnome.seahorse', path)
        self.keyset = dbus.Interface(proxy_obj, "org.gnome.seahorse.Keys")
    
    def select_key(self):
        self.populate_keys_list()
        
        resp = self.ui.main.run()
        self.ui.main.hide()
        if resp != 1:
            return
        return list( self.shown[self.ui.key_selection.get_selected()[1]] )
    
    def populate_keys_list(self):
        keys = self.keyset.ListKeys()
        
        self.shown = Gtk.TreeModelFilter( child_model=self.ui.keys )
        self.shown.set_visible_func( self.show_key, None )
                
        self.ui.keys_view.set_model( self.shown )
        self.ui.search.connect( "changed", (lambda x : self.shown.refilter()) )
        self.ui.key_selection.connect( "changed", self.activate_OK_button )
        
        self.ui.keys.clear()
        
        fields_names = [ "display-name", "display-id", "raw-id", "fingerprint", "key-desc", "flags", "expires" ]
        # Usually missing: "fingerprint"
        # Never found: "expires"
        # "display-id" always the same as "raw-id"
        
        for key in keys:
            fields = dict( self.keyset.GetKeyFields(key, fields_names ) )
#            if fields["flags"] != 0:
#                print "flags", fields["flags"]
            self.ui.keys.append( [unicode(fields["display-name"]), unicode(fields["raw-id"]), key] )
#            self.ui.keys.append( [unicode(fields["display-name"]), str(fields), ''] )
    
    def show_key(self, store, the_iter, data):
        search = self.ui.search.get_text()
        if not search:
            # No search currently active
            return True
        
        return search in self.ui.keys[the_iter][0]
    
    def activate_OK_button(self, selection):
        self.ui.OK_button.set_sensitive( bool( selection.get_selected()[1] ) )
    
    def encrypt(self, cleartext):
        self.chosen = self.select_key()
        if not self.chosen:
            return
        
        cr_proxy = self.bus.get_object('org.gnome.seahorse', '/org/gnome/seahorse/crypto')
        cr_service = dbus.Interface(cr_proxy, 'org.gnome.seahorse.CryptoService')
        
        encrypted = cr_service.EncryptText([self.chosen[2]], "", 0, cleartext)
        return encrypted
    
    def quit(self):
        Gtk.main_quit()


if __name__ == "__main__":
    sgp = Encrypter()
    Gtk.main()
