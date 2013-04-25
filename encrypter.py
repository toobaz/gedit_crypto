import dbus
from gi.repository import GLib, Gtk
from gedit_seahorse_ui import Ui

class Encrypter(object):
    def __init__(self):
        GLib.idle_add( self.run )
        GLib.timeout_add( 3000, self.quit )
        self.ui = Ui( "gedit-seahorse", "gedit-seahorse.glade" )
    
    def run(self):
    
        self.bus = dbus.SessionBus()
        proxy_obj = self.bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        dbus_iface = dbus.Interface(proxy_obj, 'org.freedesktop.DBus')

        
    def populate_keys_list(self):
        keys = self.keyset.ListKeys()
        
        self.shown = Gtk.TreeModelFilter( child_model=self.ui.keys )
        self.shown.set_visible_func( self.show_key, None )
                
        self.ui.keys_view.set_model( self.shown )
        self.ui.search.connect( "changed", (lambda x : self.shown.refilter()) )
        self.ui.key_selection.connect( "changed", self.activate_OK_button )
        
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
        print selection.get_selected()
        self.ui.OK_button.set_sensitive( selection.get_selected()[1] )
    
    def encrypt(self, text):
        proxy_obj = self.bus.get_object('org.gnome.seahorse', '/org/gnome/seahorse/keys')
        service = dbus.Interface(proxy_obj, 'org.gnome.seahorse.KeyService')
        

        proxy_obj = self.bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
        dbus_iface = dbus.Interface(proxy_obj, 'org.freedesktop.DBus')
        
        types = service.GetKeyTypes()
        print "GetKeyTypes(): ", types

        path = service.GetKeyset(types[0])
        print "GetKeySet(): ", path
        
        if not len(types):
            print "No key types found"
            sys.exit(0)

        proxy_obj = self.bus.get_object('org.gnome.seahorse', path)
        self.keyset = dbus.Interface(proxy_obj, "org.gnome.seahorse.Keys")
        self.populate_keys_list()
        
        resp = self.ui.main.run()
        if resp != 1:
            return
        
        chosen = list( self.shown[self.ui.key_selection.get_selected()[1]] )
        print chosen
    
    def quit(self):
        Gtk.main_quit()


if __name__ == "__main__":
    sgp = Encrypter()
    GLib.idle_add( sgp.encrypt, "ciao" )
    Gtk.main()
