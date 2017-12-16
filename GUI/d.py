#!/usr/bin/python
#-*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#Importamos el módulo que gestiona la base de datos.
import DB_funcionality as DBlib

#Hacemos un clear de la terminal para que no se acumule basura.
import os
os.system("clear")


class Handler:
    builder=None
    def __init__(self):

        #----------------------------VARIABLLES "ÚTILES"----------------------------

        self.DB_initializated = False   #No se carga ninguna base de datos por defecto.
        self.treeIter = None    #Necesaria para que no levante una excepción.
        self.add_edit_visible = True    #Cuando se inicia, el grid de editar y añadir aparece visible.

        #----------------------------INICIALIZACION GLADE----------------------------
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./GUI/GUI.glade")
        self.handlers = {
                        "on_main_destroy" : Gtk.main_quit,
                        "on_add_button_clicked" : self.on_add_button_clicked,
                        "on_delete_button_clicked" : self.on_delete_button_clicked,
                        "on_edit_button_clicked" : self.on_edit_button_clicked,
                        "on_about_button_clicked" : self.on_about_button_clicked,
                        "on_load_clicked" : self.on_load_clicked
                        }
        self.builder.connect_signals(self.handlers)

        #Cogemos las distintas ventanas y grid para trabajar más adelante con ellas.
        self.window = self.builder.get_object("main")

        self.window_grid = self.builder.get_object("window_grid")
        self.about_dialog = self.builder.get_object("about_dialog")

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

        self.about_button = Gtk.ToolButton()
        self.about_button.set_label("About")
        self.about_button.set_is_important(True)
        self.about_button.set_icon_name("help-about")
        self.toolbar.add(self.about_button)

        self.about_button.connect("clicked", self.on_about_button_clicked)
        
        
        #----------------------------BOTONES DE AÑADIR, BORRAR Y EDITAR----------------------------
        
        self.crud_buttons_grid = self.builder.get_object("crud_buttons_grid")

        self.add_button = self.builder.get_object("add_button")
        self.delete_button = self.builder.get_object("delete_button")
        self.edit_button = self.builder.get_object("edit_button")

        #----------------------------WIDGETS DE ENTRADA DE TEXTO------------------

        self.entry1 = self.builder.get_object("entry1")     #Entradas de la sección Add/Edit.
        self.entry2 = self.builder.get_object("entry2")
        self.entry3 = self.builder.get_object("entry3")
        self.entry4 = self.builder.get_object("entry4")
        self.entry5 = self.builder.get_object("entry5")

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

        self.model = Gtk.ListStore(int, str, str, str, str, str)        #Creamos el modelo que usará el TreeView.

        self.treeView_DB.set_model(self.model)

        #Explico solo esta ya que las otras son iguales.
        renderer0 = Gtk.CellRendererText(xalign=0.5)        #Creamos un CellRendererText para poder hacer un display del texto.
        column0 = Gtk.TreeViewColumn("Field 0", renderer0, text=0)      #Creamos una columna en el TreeView. El parámetro 'text' indica que campo del modelo se verá en ella.
        self.treeView_DB.append_column(column0)         #Añadimos dicha columna.

        renderer1 = Gtk.CellRendererText(xalign=0.5)
        column1 = Gtk.TreeViewColumn("Field 1", renderer1, text=1)
        self.treeView_DB.append_column(column1)

        renderer2 = Gtk.CellRendererText(xalign=0.5)
        column2 = Gtk.TreeViewColumn("Field 2", renderer2, text=2)
        self.treeView_DB.append_column(column2)

        renderer3 = Gtk.CellRendererText(xalign=0.5)
        column3 = Gtk.TreeViewColumn("Field 3", renderer3, text=3)
        self.treeView_DB.append_column(column3)

        renderer4 = Gtk.CellRendererText(xalign=0.5)
        column4 = Gtk.TreeViewColumn("Field 4", renderer4, text=4)
        self.treeView_DB.append_column(column4)

        renderer5 = Gtk.CellRendererText(xalign=0.5)
        column5 = Gtk.TreeViewColumn("Field 5", renderer5, text=5)
        self.treeView_DB.append_column(column5)

        #----------------------------ID COMBO BOX (donde seleccionamos el ID para edit,add,delete)----------------------------

        self.id_model = Gtk.ListStore(int)      #Creamos un modelo para el Gtk.ComboBox

        self.id_combo_box = Gtk.ComboBox.new_with_model(self.id_model)      #Creamos el Gtk.ComboBox a partir de ese modelo.
        self.crud_buttons_grid.attach(self.id_combo_box, 1, 1, 1, 1)        #Lo situamos.

        renderer_text = Gtk.CellRendererText()
        self.id_combo_box.pack_start(renderer_text, True)
        self.id_combo_box.add_attribute(renderer_text, "text", 0)
        self.id_combo_box.connect("changed", self.on_id_combo_box_changed)      #Detectamos cuando un nuevo ID ha sido seleccionado.

        #----------------------------WINDOW PREFERENCES----------------------------

        self.window.resize(500,300)     #Ajustamos el tamaño de la ventana a uno adecuado.
        self.window.show_all()          #Mostramos la ventana.

    #----------------------------FUNCIONES----------------------------
    
    def on_add_button_clicked(self,button):
        if self.DB_initializated:   #Si no se ha cargado ningnua base de datos, no se añade nada.
            if self.entry1.get_text() and self.entry2.get_text() and self.entry3.get_text() and self.entry4.get_text() and self.entry5.get_text() :
                self.DB.addRegister(self.entry1.get_text(),self.entry2.get_text(),self.entry3.get_text(),self.entry4.get_text(),self.entry5.get_text())
                print("Register added")
                self.on_update_button_clicked(button)       #Actualizamos el display para que se vean los cambios.
            else:
                print("Error while adding.")
        else:
            print("Error: Data Base not initializated")

    def on_delete_button_clicked(self,button):
        if self.treeIter != None:       #Si no hay ningún id seleccionado, no se borra nada.
            self.DB.remove(self.id_model[self.treeIter][0])     #id_model[treeIter] devuelve la fila a la que apunta treeIter, en el campo 0, se encuentra el id.
            print("Register deleted")
            self.on_update_button_clicked(button)       #Actualizamos el display para que se vean los cambios.
        else:
            print("Error: no ID register selected")
    
    def on_update_button_clicked(self,button):
        if self.DB_initializated:
            data = self.DB.getRegisters()

            self.clear_models()

            for reg in data:        #Añadimos todos los registros de la base de datos al modelo. (No es lo más eficiente, i know xdd).
                self.model.append(reg)

            ids = self.DB.getIDs()
            for i in ids:
                    self.id_model.append([i])
            print("DB updated")
        else:
            print("Error: Data Base not initializated")      
    
    def on_edit_button_clicked(self,button):
        if self.treeIter != None:
            self.DB.editRegisterWithID(self.id_model[self.treeIter][0],self.entry1.get_text(),self.entry2.get_text(),self.entry3.get_text(),self.entry4.get_text(),self.entry5.get_text())
            print("Register edited")
            self.on_update_button_clicked(button)
        else:
            print("Error: no ID register selected")
    
    def on_load_button_clicked(self, button):
        self.treeView_DB.hide()     #Escondemos el display de los datos.
        self.init_grid.show()       #Mostramos el init_grid que contiene los widgets necesarios para introducir los datos para iniciar la DB.

    def on_load_clicked(self, button):
        if not self.DB_initializated:
            self.DB = DBlib.DB_Handler()        #Creamos un objeto 'DB_Handler' para gestionar la base de datos.
            arg = [self.host_entry.get_text(), self.user_entry.get_text(), self.passwd_entry.get_text(), self.db_name_entry.get_text()] #Recogemos los datos.
            for reg in arg:     #Si alguno de los campos está vacío, devolvemos error.
                if not reg:
                    print("All fields must be filled")
                    return -1
            if self.DB.openDB(host=arg[0], user=arg[1], passwd=arg[2], db=arg[3]) < 0:      #Si alguno de los datos es incorrecto, o ha habido algún otro fallo al iniciar la base, openDB() devuelve -1.
                print("Error Opening Data Base, please check the input (maybe the user does not have enough permissions).")
                return -1
            data = self.DB.getRegisters()
            for reg in data:
                self.model.append(reg)
            self.DB_initializated = True

            ids = self.DB.getIDs()
            for i in ids:
                self.id_model.append([i])

            self.init_grid.hide()
            self.treeView_DB.show()

            print("DB loaded")
        else:
            print("Error: DB is already loaded")

    def on_clear_button_clicked(self, button):
        if self.DB_initializated:
            self.DB.clear()
            self.on_update_button_clicked(button)
            print("DB cleared")
        else:
            print("Error: Data Base not initializated")

    def on_id_combo_box_changed(self, combo):
        self.treeIter = combo.get_active_iter()
        if self.treeIter != None:
            reg = self.DB.getRegisterWithID(self.id_model[self.treeIter][0])
            self.entry1.set_text(reg[0][1])     #Ponemos el registro seleccionado en las entradas, para que la edición sea más cómoda.
            self.entry2.set_text(reg[0][2])
            self.entry3.set_text(reg[0][3])
            self.entry4.set_text(reg[0][4])
            self.entry5.set_text(reg[0][5])

    def on_add_edit_clicked(self, button):
        if self.add_edit_visible:       #Mostramos el crud_buttons_grid dependiendo de si ya está siendo mostrado o no.
            self.add_edit_visible = False
            self.crud_buttons_grid.hide()
        else:
            self.add_edit_visible = True
            self.crud_buttons_grid.show()
            
    def on_about_button_clicked(self, button):  #Mostramos la ventana de 'about'.
        self.about_dialog.show()
    
    def on_close_button_clicked(self, button):
        if self.DB_initializated:
            self.DB = None
            self.DB_initializated = False
            self.clear_models()
            self.on_load_button_clicked(button)
        else:
            print("Error: No Data Base initializated")

    def clear_models(self):
        if self.model != None and self.id_model != None:
            for row in self.model:      #Borramos los datos del modelo.
                treeIter = self.model.get_iter_first()
                self.model.remove(treeIter)
            for row in self.id_model:      #Borramos los datos del modelo.
                treeIter = self.id_model.get_iter_first()
                self.id_model.remove(treeIter)

def main():
    window = Handler()
    Gtk.main()
    return 0

if __name__ == '__main__':
main()