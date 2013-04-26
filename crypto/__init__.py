from gi.repository import GObject, Gedit, Gtk, Gedit
import os
from encrypter import Encrypter

class GeditCrypto(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "CryptoPlugin"
    window = GObject.property(type=Gedit.Window)
    
    def do_activate(self):
        try:
            self.initialize()
        except Exception, msg:
            import traceback
            print "Error initializing \"Crypto\" plugin"
            print traceback.print_exc()
    
    def initialize(self):
        from crypto_ui import Ui
        
        self.data_dir = self.plugin_info.get_data_dir()
        
        ui_path = os.path.join( self.data_dir, "crypto.glade" )
        self.ui = Ui( "gedit-crypto", ui_path )
        self.ui.connect_signals( self )
        
        self.insert_menu_items()
        
        # Build encrypter when needed to not slow down Gedit startup
        self.enc = None
    
    def do_deactivate(self):
        """
        Just remove submenu.
        """
        manager = self.window.get_ui_manager()
        manager.remove_ui( self.ui_id )
        manager.ensure_update()
    
    def do_update_state(self):
        pass
    
    def insert_menu_items(self):
        """
        Insert submenu and menu items in Gedit "File" menu.
        """
        manager = self.window.get_ui_manager()
        
        self.action_group = Gtk.ActionGroup("CryptoActions")
        
        self.action_group.add_action( self.ui.EncryptAction )
        self.action_group.add_action( self.ui.CryptoAction )
        
        manager.insert_action_group( self.action_group )
        
        menu_ui_path = os.path.join( self.data_dir, "menu_ui.xml" )
        
        self.ui_id = manager.add_ui_from_file( menu_ui_path )
        
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
