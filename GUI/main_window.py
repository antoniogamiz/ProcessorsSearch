#!/usr/bin/python
#-*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
sys.path.insert(0, "./scraper/scraper/data_base")
import db

import os
os.system("clear")

class Handler:
    builder=None
    def __init__(self):

        #----------------------------VARIABLLES "ÚTILES"----------------------------

        self.DB_initializated = False
        self.treeIter = None    

        #----------------------------INICIALIZACION GLADE----------------------------
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./GUI/GUI.glade")
        self.handlers = {
                        "on_main_destroy" : Gtk.main_quit,
                        "on_load_clicked" : self.on_load_clicked
                        }
        self.builder.connect_signals(self.handlers)

        self.window = self.builder.get_object("main")
        self.window_grid = self.builder.get_object("window_grid")
        self.init_grid = self.builder.get_object("init_grid")
        self.init_grid.hide()

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

        #----------------------------WIDGETS DE ENTRADA DE TEXTO------------------
        
        self.host_entry = self.builder.get_object("host_entry")     #Entradas para cargar la base de datos.
        self.user_entry = self.builder.get_object("user_entry")
        self.passwd_entry = self.builder.get_object("passwd_entry")
        self.db_name_entry = self.builder.get_object("db_name_entry")

        #----------------------------DISPLAY DE LOS REGISTROS DE LA BD----------------------------
        
        self.treeView_DB = Gtk.TreeView()       #Este también lo he creado desde código porque me resulta más fácil que desde Glade.

        self.scrollable_treelist = Gtk.ScrolledWindow()     #Creamos una barra para poder moverse dentro del display de los datos, para mayor comodidad.
        self.scrollable_treelist.set_vexpand(True)      #Desplazamiento vertical.
        self.scrollable_treelist.set_hexpand(True)      #Desplazamiento horizontal.
        self.window_grid.attach(self.scrollable_treelist,0,1,3,1)       #La añadimos a donde irá el display(Gtk.TreeView).

        self.scrollable_treelist.add(self.treeView_DB)

        self.model = Gtk.ListStore(int, str, str, str, int, str)        #Creamos el modelo que usará el TreeView.

        self.treeView_DB.set_model(self.model)

        #Explico solo esta ya que las otras son iguales.
        renderer0 = Gtk.CellRendererText(xalign=0.5)        #Creamos un CellRendererText para poder hacer un display del texto.
        column0 = Gtk.TreeViewColumn("ID", renderer0, text=0)      #Creamos una columna en el TreeView. El parámetro 'text' indica que campo del modelo se verá en ella.
        self.treeView_DB.append_column(column0)         #Añadimos dicha columna.

        renderer1 = Gtk.CellRendererText(xalign=0.5)
        column1 = Gtk.TreeViewColumn("Brand", renderer1, text=1)
        self.treeView_DB.append_column(column1)

        renderer2 = Gtk.CellRendererText(xalign=0.5)
        column2 = Gtk.TreeViewColumn("Model", renderer2, text=2)
        self.treeView_DB.append_column(column2)

        renderer3 = Gtk.CellRendererText(xalign=0.5)
        column3 = Gtk.TreeViewColumn("Frequency", renderer3, text=3)
        self.treeView_DB.append_column(column3)

        renderer4 = Gtk.CellRendererText(xalign=0.5)
        column4 = Gtk.TreeViewColumn("Price (euros)", renderer4, text=4)
        self.treeView_DB.append_column(column4)

        renderer5 = Gtk.CellRendererText(xalign=0.5)
        column5 = Gtk.TreeViewColumn("Availability", renderer5, text=5)
        self.treeView_DB.append_column(column5)


        #----------------------------WINDOW PREFERENCES----------------------------

        self.window.resize(800,300)     #Ajustamos el tamaño de la ventana a uno adecuado.
        self.window.show_all()          #Mostramos la ventana.

    def on_load_button_clicked(self, button):
        self.treeView_DB.hide()     #Escondemos el display de los datos.
        self.init_grid.show()       #Mostramos el init_grid que contiene los widgets necesarios para introducir los datos para iniciar la DB.

    def on_close_button_clicked(self, button):
        if self.DB_initializated:
            self.DB = None
            self.DB_initializated = False
            self.clear_models()
            self.on_load_button_clicked(button)
        else:
            print("Error: No Data Base initializated")
    def on_clear_button_clicked(self, button):
        if self.DB_initializated:
            self.DB.clear()
            self.on_update_button_clicked(button)
            print("DB cleared")
        else:
            print("Error: Data Base not initializated")
    def on_add_edit_clicked(self, button):
        pass
    def on_update_button_clicked(self, button):
        if self.DB_initializated:
            data = self.DB.getRegisters()

            self.clear_models()

            for reg in data:        #Añadimos todos los registros de la base de datos al modelo. (No es lo más eficiente, i know xdd).
                self.model.append(reg)

            print("DB updated")
        else:
            print("Error: Data Base not initializated")
    def on_load_clicked(self, button):
        if not self.DB_initializated:
            os.chdir('./scraper')       # Nos cambiamos a la carpeta donde está el projecto de scrapy, ejecutamos el spider, y volvemos al directorio padre.
            os.system('scrapy crawl processors')
            os.chdir('..')

            self.DB = db.DB_Handler()        #Creamos un objeto 'DB_Handler' para gestionar la base de datos.
            arg = [self.host_entry.get_text(), self.user_entry.get_text(), self.passwd_entry.get_text(), self.db_name_entry.get_text()] #Recogemos los datos.
            for reg in arg:     #Si alguno de los campos está vacío, devolvemos error.
                if not reg:
                    print("All fields must be filled")
                    return -1
            if self.DB.openDB(host=arg[0], user=arg[1], passwd=arg[2], db=arg[3]):      #Si alguno de los datos es incorrecto, o ha habido algún otro fallo al iniciar la base, openDB() devuelve -1.
                print("Error Opening Data Base, please check the input (maybe the user does not have enough permissions).")
                return -1
            data = self.DB.getRegisters()
            for reg in data:
                self.model.append(reg)
            self.DB_initializated = True

            self.init_grid.hide()
            self.treeView_DB.show()

            print("DB loaded")
        else:
            print("Error: DB is already loaded")

    def clear_models(self):
        if self.model != None:
            for row in self.model:      #Borramos los datos del modelo.
                treeIter = self.model.get_iter_first()
                self.model.remove(treeIter)

def main():
    window = Handler()
    Gtk.main()
    return 0

if __name__ == '__main__':
    main()