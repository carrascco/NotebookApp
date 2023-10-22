import tkinter as tk
from tkinter import ttk
from notebook.notebook import Notebook
import json

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook App")


        # Crear un objeto Notebook
        self.notebook = Notebook()

    # Cambiar el color de fondo de la barra de título
        self.change_titlebar_color(self.root, "#01add3")  # Cambia el valor hexadecimal al color que desees


        self.set_window_size_to_percentage(20, 40)

        #Cargar notas del archivo JSON
        self.load_notes()

        # Crear un estilo personalizado para el Frame
        style = ttk.Style()
        style.configure("My.TFrame", background="#0453a1")  # Cambia el valor hexadecimal al color que desees
        style.configure("My.TButton", background="#0453a1")

        # Crear un Frame principal
        main_frame = ttk.Frame(self.root, style="My.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew")

        

        # Configurar el sistema de geometría "grid" para que se ajuste a la ventana
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Crear un Frame a la izquierda para el listado de notas
        list_frame = ttk.Frame(main_frame, style="My.TFrame")
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configurar el sistema de geometría "grid" para que se ajuste al Frame principal
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Crear un ListBox para mostrar las notas
        self.note_listbox = tk.Listbox(list_frame)
        self.note_listbox.pack(fill="both", expand=True)

        # Ajustar el tamaño de fuente
        font = ("Helvetica", 20)  # Cambia el tamaño (14) y la fuente según tus preferencias
        self.note_listbox.configure(font=font)


        # Crear un Frame a la derecha para agregar notas
        add_frame = ttk.Frame(main_frame, style="My.TFrame")
        add_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Botón para agregar una nueva nota
        
        add_button = ttk.Button(add_frame, text="Agregar Nota", command=self.open_add_note_window, style="My.TButton")
        add_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Ajustar el tamaño del botón
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 16))  # Cambia el tamaño de fuente (16) según tus preferencias
        style.map("TButton", background=[("active", "#0453a1")])  # Cambia el color "yellow" al que desees


        # Botón para eliminar la nota seleccionada
        delete_button = ttk.Button(add_frame, text="Eliminar Nota", command=self.delete_note, style="My.TButton")
        delete_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.update_note_listbox()

        self.update_window_size()


    def update_window_size(self):
        maxNoteLengthX=10
        maxNoteLengthY=40
        for note in self.notebook.notes:
            if len(note)>maxNoteLengthX:
                maxNoteLengthX=len(note)
        if(len(self.notebook.notes)*3>maxNoteLengthY):
            maxNoteLengthY=len(self.notebook.notes)*3
        self.set_window_size_to_percentage(maxNoteLengthX+9, maxNoteLengthY)



    def open_add_note_window(self):
        # Crea una nueva ventana para agregar una nota
        add_note_window = tk.Toplevel(self.root)
        
        add_note_window.title("Agregar Nota")

        # Crear un campo de texto para ingresar la nota
        note_entry = tk.Entry(add_note_window)
        note_entry.pack(padx=10, pady=10)

        # Botón para guardar la nota
        save_button = ttk.Button(add_note_window, text="Guardar Nota", command=lambda: self.save_note_and_close(add_note_window, note_entry.get()))
        save_button.pack(padx=10, pady=10)

    def delete_note(self):
        # Obtener el índice de la nota seleccionada
        selected_index = self.note_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            # Eliminar la nota de la Listbox y de la lista de notas
            self.note_listbox.delete(index)
            self.notebook.delete_index(index)
            with open("data/notes.json", "w") as file:
                
                json.dump(self.notebook.notes, file)
            self.update_window_size()

    def save_note_and_close(self, window, note_text):
        # Guardar la nueva nota
        self.notebook.add_note(note_text)
        # Guardar todas las notas en el archivo JSON
        self.save_notes()
        self.update_note_listbox()
        self.update_window_size()
        window.destroy()

    def load_notes(self):
        try:
            with open("data/notes.json", "r") as file:
               
                notes = json.load(file)
                
                for note in notes:
                    self.notebook.add_note(note)
        except FileNotFoundError:
            # Si el archivo no existe, no se cargan notas (puede ser la primera ejecución)
            pass

    def save_notes(self):
        notes = self.notebook.get_notes()
        with open("data/notes.json", "w") as file:
            json.dump(notes, file)

    def update_note_listbox(self):
        # Actualizar el listado de notas en el ListBox
        notes = self.notebook.get_notes()
        self.note_listbox.delete(0, tk.END)
        for note in notes:
            self.note_listbox.insert(tk.END, note)

    def change_titlebar_color(self, root, color):
        if root.tk_setPalette:
            root.tk_setPalette(background=color)
        elif root.option_add:
            root.option_add("*TButton*Background", color)
        
    def set_window_size_to_percentage(self, width_percentage, height_percentage):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
    
        window_width = int(screen_width * width_percentage / 100)
        window_height = int(screen_height * height_percentage / 100)
    
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
    
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")


    if __name__ == "__main__":
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()