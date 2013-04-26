#! /usr/bin/python
# -*- coding: utf-8 -*-
# gedit-seahorse
#
# gedit-seahorse is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# gedit-seahorse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with gedit-seahorse; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# Copyright © 2013 Pietro Battiston <me@pietrobattiston.it>

from gi.repository import Gtk

class Ui(object):
    def __init__(self, APP, filename):
        self._builder = Gtk.Builder()
        self._builder.set_translation_domain(APP)
        self._builder.add_from_file(filename)
    
    def __getattr__(self, attr_name):
        try:
            return object.__getattribute__(self, attr_name)
        except AttributeError:
            obj = self._builder.get_object(attr_name)
            if obj:
                self.obj = obj
                return obj
            else:
                raise AttributeError, "no object named \"%s\" in the GUI." % attr_name
