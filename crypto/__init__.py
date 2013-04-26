from gi.repository import GObject, Gedit, Gtk, Gedit
import os
from encrypter import Encrypter

class GeditCrypto(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "CryptoPlugin"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        
        self.enc = None
        
        try:
            print "Initialized"
        except Exception, msg:
            print "oh no init", msg
    
    def do_activate(self):
        try:
            from crypto_ui import Ui
            DATA_DIR = self.plugin_info.get_data_dir()
            ui_path = os.path.join( DATA_DIR, "crypto.glade" )
            self.ui = Ui( "gedit-crypto", ui_path )
            print self.plugin_info.get_data_dir()
            self.insert_menu_items()
            print "Window %s activated oh yes." % self.window
            
            self.ui.connect_signals( self )
        except Exception, msg:
            import traceback
            print "oh no"
            print traceback.print_exc()

    def do_deactivate(self):
        print "Window %s deactivated." % self.window

    def do_update_state(self):
        print "Window %s state updated." % self.window
    
    def insert_menu_items(self):
        manager = self.window.get_ui_manager()
        
        self.ui_id = manager.new_merge_id()
        
        self.action_group = Gtk.ActionGroup("CryptoActions")
        
        self.action_group.add_action( self.ui.EncryptAction )
        self.action_group.add_action( self.ui.CryptoAction )
        
        manager.insert_action_group( self.action_group )
        
        DATA_DIR = self.plugin_info.get_data_dir()
        menu_ui_path = os.path.join( DATA_DIR, "menu_ui.xml" )
        
        manager.add_ui_from_file( menu_ui_path )
        
        manager.ensure_update()
    
    def encrypt(self, action):
        if self.enc == None:
            self.enc = Encrypter(self.ui)
        
        view = self.window.get_active_view()
        doc = view.get_buffer()
        start = doc.get_start_iter()
        end = doc.get_end_iter()
        cleartext = doc.get_text( start, end, False )
        
        encrypted = self.enc.encrypt( cleartext )
        
        self.window.create_tab( True )
        new_view = self.window.get_active_view()
        new_doc = new_view.get_buffer()
        new_doc.set_text( encrypted )
