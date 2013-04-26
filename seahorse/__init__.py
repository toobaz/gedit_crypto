from gi.repository import GObject, Gedit, Gtk

class GeditSeahorse(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "Gedit_seahorse"
    window = GObject.property(type=Gedit.Window)
    
    def __init__(self):
        GObject.Object.__init__(self)
        try:
            from gedit_seahorse_ui import Ui
            self.ui = Ui( "gedit-seahorse", "gedit-seahorse.glade" )
        except Exception, msg:
            print "oh no init", msg
    
    def do_activate(self):
        try:
            self.insert_menu_items()
            print "Window %s activated oh yes." % self.window
        except Exception, msg:
            print "oh no", msg

    def do_deactivate(self):
        print "Window %s deactivated." % self.window

    def do_update_state(self):
        print "Window %s state updated." % self.window
    
    def insert_menu_items(self):
        manager = self.window.get_ui_manager()
        
        self.ui_id = manager.new_merge_id()
        
        self.action_group = Gtk.ActionGroup("SeahorseActions")
        
        self.action_group.add_actions( self.ui.SeahorseEncrypt )
        
        print "done"
