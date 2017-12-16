#!/usr/bin/python
#-*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os
os.system("clear")

class Handler:
    builder=None
    def __init__(self):

        #----------------------------VARIABLLES "ÚTILES"----------------------------

        self.DB_initializated = False
        self.treeIter = None    
        self.add_edit_visible = True    

        #----------------------------INICIALIZACION GLADE----------------------------
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./GUI/GUI.glade")
        self.handlers = {
                        "on_main_destroy" : Gtk.main_quit
                        }
        self.builder.connect_signals(self.handlers)

        self.window = self.builder.get_object("main")
        self.window_grid = self.builder.get_object("window_grid")

        #----------------------------CREACIÓN DE LA TOOLBAR----------------------------

        self.toolbar = Gtk.Toolbar()        #Creo la toolbar desde código porque desde Glade me ha dado problemas que no he sabido solucionar.
        self.window_grid.attach(self.toolbar, 0,0,3,1)  #La añado al top del grid principal.

        #Creación del botón 'Load DB' (Explico este solo ya que los demás son iguales) 
        self.load_button = Gtk.ToolButton()     #Creamos el botón.
        self.load_button.set_label("Load DB")       #Le ponemos una etiqueta.
        self.load_button.set_is_important(True)     #Lo ponemos a True para que funcione bien.
        self.load_button.set_icon_name("system-software-install")       #Le ponemos un icono (he usado los disponibles en Ubuntu, con 'gtk3-icon-browser' desde la terminal se pueden ver los iconos disponibles.)
        self.toolbar.add(self.load_button)

        self.load_button.connect("clicked", self.on_load_button_clicked)        #Asociamos una señal al botón.

        self.close_button = Gtk.ToolButton()
        self.close_button.set_label("Close DB")
        self.close_button.set_is_important(True)
        self.close_button.set_icon_name("window-close")
        self.toolbar.add(self.close_button)

        self.close_button.connect("clicked", self.on_close_button_clicked)

        self.clear_button = Gtk.ToolButton()
        self.clear_button.set_label("Clear DB")
        self.clear_button.set_is_important(True)
        self.clear_button.set_icon_name("emblem-important")
        self.toolbar.add(self.clear_button)

        self.clear_button.connect("clicked", self.on_clear_button_clicked)

        self.add_edit_button = Gtk.ToolButton()
        self.add_edit_button.set_label("Add/Edit DB")
        self.add_edit_button.set_is_important(True)
        self.add_edit_button.set_icon_name("edit-find-replace")
        self.toolbar.add(self.add_edit_button)

        self.add_edit_button.connect("clicked", self.on_add_edit_clicked)

        self.update_button = Gtk.ToolButton()
        self.update_button.set_label("Update DB")
        self.update_button.set_is_important(True)
        self.update_button.set_icon_name("system-software-update")
        self.toolbar.add(self.update_button)

        self.update_button.connect("clicked", self.on_update_button_clicked)

        #----------------------------WINDOW PREFERENCES----------------------------

        self.window.resize(800,300)     #Ajustamos el tamaño de la ventana a uno adecuado.
        self.window.show_all()          #Mostramos la ventana.

    def on_load_button_clicked(self, button):
        pass
    def on_close_button_clicked(self, button):
        pass
    def on_clear_button_clicked(self, button):
        pass
    def on_add_edit_clicked(self, button):
        pass
    def on_update_button_clicked(self, button):
        pass

def main():
    window = Handler()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()