# Guia 2 de la Unidad 2 Programacion Avanzada 2022, Matias Fonseca - Claudio Larosa
import gi
import json
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def open_file():
    """Se abre el archivo JSON creado para este proyecto"""
    try:
        with open("libreria.json", 'r') as archivo:
            data = json.load(archivo)
    except IOError:
        data = []
    return data

def save_file(data):
    """Guarda los datos ingresados en el archivo JSON"""
    with open("libreria.json", 'w') as archivo:
        json.dump(data, archivo, indent=3)

# Ventana principal del programa. 
class Ventana_principal(Gtk.Window):
    def __init__(self):
        super().__init__(title="Biblioteca CDMR")

        # Box de la ventana principal.
        self.caja = Gtk.Box(spacing = 10)
        self.caja.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.add(self.caja)

        # Boton que abre el dialogo principal.
        self.bton1 = Gtk.Button()
        self.bton1.set_label("Agregar/Eliminar un libro")
        self.bton1.connect("clicked", self.abrir)
        self.caja.add(self.bton1)

        # Boton para salir.
        self.bton2 = Gtk.Button()
        self.bton2.set_label("Salir")
        self.bton2.connect("clicked", self.cerrar)
        self.caja.add(self.bton2)

    # Funcion que abre el dialogo donde se agregan o eliminan los libros.
    def abrir(self, btn=None):
        dialogo = Dialogo_principal(self)
        dialogo.run()
        dialogo.destroy()
    
    # Funcion que cierra el programa.
    def cerrar(self, btn=None):
        Gtk.main_quit()

# Ventana de dialogo, donde se agregan o se eliminan los libros.
class Dialogo_principal(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Biblioteca CDMR", transient_for=parent, flags=0)

        # Box de la ventana donde se agregan o eliminan los libros.
        box = self.get_content_area()
        box.set_orientation(Gtk.Orientation.VERTICAL)

        # Se configura un TreeView para contener los datos de los libros.
        self.tree = Gtk.TreeView()
        self.modelo = Gtk.ListStore(str, str, str)
        self.tree.set_model(model=self.modelo)
        box.add(self.tree)

        nombre_columnas = ("Código", "Nombre", "Autor")
        cell = Gtk.CellRendererText()
        for item in range(len(nombre_columnas)):
            column = Gtk.TreeViewColumn(nombre_columnas[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)        

        # Se cargan los datos en la interfaz.
        self.load_data_from_json()

        # Boton para agregar los libros.
        self.boton_agregar = Gtk.Button()
        self.boton_agregar.set_label("Agregar Libro")
        self.boton_agregar.connect("clicked", self.agregar)
        box.add(self.boton_agregar)

        # Boton para eliminar el libro seleccionado.
        self.boton_eliminar = Gtk.Button()
        self.boton_eliminar.set_label("Eliminar Libro")
        self.boton_eliminar.connect("clicked", self.eliminar)
        box.add(self.boton_eliminar)    

        self.show_all()

    # Se cargan los datos del JSON para su manipulacion.
    def load_data_from_json(self):
        datos = open_file()

        for item in datos:
            line = [x for x in item.values()]
            #print(line)
            self.modelo.append(line)

    # Abre la ventana de dialogo para ingresar los datos de los libros.
    def agregar(self, btn=None):
        agregar_libro = Dialogo_agregar(self)
        agregar_libro.run()
        agregar_libro.destroy()

    # Se elimina el contenido del tree para su actualizacion.
    def delete_all_data(self):
        for index in range(len(self.modelo)):
            iter_ = self.modelo.get_iter(0)
            self.modelo.remove(iter_)
    
    # Se elimina el libro seleccionado.
    def eliminar(self, btn=None):
        pass
        model, it = self.tree.get_selection().get_selected()
        # Por si no se seleccionada nada.
        if model is None or it is None:
            print("Seleccione un libro.")
            return
            
        data = open_file()
        for item in data:
            if item['codigo'] == model.get_value(it, 0):
                data.remove(item)
        save_file(data)

        self.delete_all_data()
        self.load_data_from_json()

# Ventana de dialogo que permite agregar los libros.
class Dialogo_agregar(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Biblioteca CDMR", transient_for=parent, flags=0)
        
        # Box de la ventana donde se agregan los datos de los libros.
        box = self.get_content_area()
        box.set_orientation(Gtk.Orientation.VERTICAL)

        # Se Configura distintos Label y Entry para los datos.
        label = Gtk.Label(label= "Codigo")
        box.add(label)

        self.codigo = Gtk.Entry()
        box.add(self.codigo)
        
        label_1 = Gtk.Label(label="Nombre")
        box.add(label_1)

        self.nombre = Gtk.Entry()
        box.add(self.nombre)

        label_2 = Gtk.Label(label="Autor")
        box.add(label_2)

        self.autor = Gtk.Entry()
        box.add(self.autor)

        # Configuración del boton "Aceptar" de esta ventana.
        buton_OK = Gtk.Button()
        buton_OK.set_label("Agregar")
        buton_OK.connect("clicked", self.butonOK_clicked)
        box.add(buton_OK)

        self.show_all()

    # Se ingresan los datos y se agrega el nuevo libro a la lista mostrada en pantalla y al JSON.
    def butonOK_clicked(self, btn=None):
        codigo = self.codigo.get_text()
        nombre = self.nombre.get_text()
        autor = self.autor.get_text()

        data = open_file()
        new_data = {"codigo": codigo,
                    "nombre": nombre,
                    "autor": autor
                    }
        data.append(new_data)
        save_file(data)

if __name__ == "__main__":
    # Se llama a la Ventana principal del programa.
    win = Ventana_principal()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()