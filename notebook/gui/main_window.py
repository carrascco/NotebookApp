import tkinter as tk
from tkinter import ttk
from notebook.notebook import Notebook

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook App")

        # Crear un objeto Notebook
        self.notebook = Notebook()

        # Crear un Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Crear un Frame a la izquierda para el listado de notas
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Crear un ListBox para mostrar las notas
        self.note_listbox = tk.Listbox(list_frame)
        self.note_listbox.pack(fill="both", expand=True)

        # Crear un Frame a la derecha para agregar notas
        add_frame = ttk.Frame(main_frame)
        add_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

        # Botón para agregar una nueva nota
        add_button = ttk.Button(add_frame, text="Agregar Nota", command=self.open_add_note_window)
        add_button.pack(padx=10, pady=10)

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

    def save_note_and_close(self, window, note_text):
        # Guardar la nueva nota
        self.notebook.add_note(note_text)
        self.update_note_listbox()
        window.destroy()

    def update_note_listbox(self):
        # Actualizar el listado de notas en el ListBox
        notes = self.notebook.get_notes()
        self.note_listbox.delete(0, tk.END)
        for note in notes:
            self.note_listbox.insert(tk.END, note)

    if __name__ == "__main__":
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()