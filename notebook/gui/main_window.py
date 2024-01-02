import tkinter as tk
from tkinter import ttk
from notebook.notebook import Notebook
from PIL import Image, ImageTk
from tkinter import messagebox  
import datetime
import json
from tkcalendar import Calendar
import os

class MainWindow:
    def __init__(self, root):
        self.root = root
        
        self.root.title("Miguel's Notebook")

        current_dir = os.path.dirname(__file__)
        two_levels_up = os.path.abspath(os.path.join(current_dir, "../../"))
        icon_path = os.path.join(two_levels_up, "data", "logo.ico")
        root.iconbitmap(icon_path)

        # Crear un objeto Notebook
        self.notebook = Notebook()

    # Cambiar el color de fondo de la barra de título
        self.change_titlebar_color(self.root, "#01add3")  # Cambia el valor hexadecimal al color que desees


        self.set_window_size_to_percentage(20, 40)

       # logo_image= Image.open("data\logoGrande.png")
        #logo_image = ImageTk.PhotoImage(logo_image)
        #root.iconphoto(True,logo_image)
       
        
        #Cargar notas del archivo JSON
        self.load_notes()

        # Crear un estilo personalizado para el Frame
        style = ttk.Style()
        style.configure("My.TFrame", background="#0453a1")  # Cambia el valor hexadecimal al color que desees
        style.configure("My.TButton", background="#0453a1")
        style.configure("Second.TButton", background="#01add3")
        style.configure("Third.TButton", background="#01add3",padding=(3, 3), font=("Helvetica", 10))
        
        
        style.configure("My.TText", background="#0453a1",foreground="white", font=("Helvetica", 8))
        
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
        font = ("Helvetica", 14)  # Cambia el tamaño (14) y la fuente según tus preferencias
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

        view_noteBTN = ttk.Button(add_frame, text="Ver Nota", command=self.view_note, style="My.TButton")
        view_noteBTN.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.update_note_listbox()

        self.update_window_size()

        self.calendar_frame = None  # Frame para el calendario
        self.calendar = None  # Calendario
        self.selected_date = None



    def open_calendar(self):
        # Crear una nueva ventana emergente
        self.calendar_frame = tk.Toplevel(self.root)
        self.calendar_frame.title("Seleccionar Fecha")

        current_dir = os.path.dirname(__file__)
        two_levels_up = os.path.abspath(os.path.join(current_dir, "../../"))
        icon_path = os.path.join(two_levels_up, "data", "logo.ico")
        self.calendar_frame.iconbitmap(icon_path)

        self.calendar = Calendar(self.calendar_frame, selectmode="day", year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.calendar.pack(padx=10, pady=10)

        self.select_button = ttk.Button(self.calendar_frame, text="Seleccionar Fecha", command=self.add_note_with_date,style="Second.TButton")
        self.select_button.pack(padx=20, pady=10)
        screen_width = self.calendar_frame.winfo_screenwidth()
        screen_height = self.calendar_frame.winfo_screenheight()

        window_width = int(screen_width * 20 / 100)
        window_height = int(screen_height * 10 / 100)

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.calendar_frame.geometry(f"{window_width}x{window_height+160}+{x}+{y}")

        
    def add_note_with_date(self):
        selected = self.calendar.get_date()

        mes, dia, año = selected.split('/')
#        año="20"+año
        self.selected_date = f"{dia}/{mes}/{año}"
        fecha_objeto = datetime.datetime.strptime(self.selected_date, "%d/%m/%y")
        dia_semana_numero = fecha_objeto.weekday()

        # Convertir el número a nombre del día de la semana
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        nombre_dia_semana = dias_semana[dia_semana_numero]
        
        self.selected_date = nombre_dia_semana +", "+self.selected_date
        self.calendar_frame.destroy()  
        


    def update_window_size(self):
        maxNoteLengthX=15
        for note in self.notebook.notes:
            if self.text_size(note)>maxNoteLengthX:
                maxNoteLengthX=self.text_size(note)
        if(maxNoteLengthX<80):
            self.set_window_size_to_percentage(maxNoteLengthX+8, 40)
        else:
            self.set_window_size_to_percentage(80, 40)


    def text_size(self, note):
        count=0
        for char in note:
            if not char.isdigit():
                count+=1
            else:
                count+=0.95
        return count

    def open_add_note_window(self):
        # Crea una nueva ventana para agregar una nota
        add_note_window = tk.Toplevel(self.root)
        
        add_note_window.title("Agregar Nota")

        current_dir = os.path.dirname(__file__)
        two_levels_up = os.path.abspath(os.path.join(current_dir, "../../"))
        icon_path = os.path.join(two_levels_up, "data", "logo.ico")
        add_note_window.iconbitmap(icon_path)

        note_label = ttk.Label(add_note_window, text="Ingrese la nota:", background="#01add3",foreground="white",font={"Helvetica",16})
        note_label.pack(padx=15, pady=(20, 0))  # Ajusta el espaciado según sea necesario

        # Crear un campo de texto para ingresar la nota
        note_entry = tk.Entry(add_note_window)
        note_entry.pack(padx=15, pady=10, ipadx=85)

        date_label = ttk.Label(add_note_window, text="Ingrese la fecha (opcional):", background="#01add3",foreground="white",font={"Helvetica",16})
        date_label.pack(padx=15, pady=10)
        

        date_entry = ttk.Button(add_note_window, text="Agregar fecha límite", command=self.open_calendar, style="Third.TButton")
        date_entry.pack(padx=10, pady=10)


        screen_width = add_note_window.winfo_screenwidth()
        screen_height = add_note_window.winfo_screenheight() 
    
        window_width = int(screen_width * 20 / 100)
        window_height = int(screen_height * 20 / 100)
    
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
    
        add_note_window.geometry(f"{window_width}x{window_height+30}+{x}+{y}")

        # Botón para guardar la nota
        save_button = ttk.Button(add_note_window, text="Guardar Nota", command=lambda: self.save_note_and_close(add_note_window, note_entry.get()), style="Second.TButton")
        save_button.pack(padx=10, pady=10)
        

    def delete_note(self):
        # Obtener el índice de la nota seleccionada
        selected_index = self.note_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            # Eliminar la nota de la Listbox y de la lista de notas
            self.note_listbox.delete(index)
            self.notebook.delete_index(index)

            current_dir = os.path.dirname(__file__)
            two_levels_up = os.path.abspath(os.path.join(current_dir, "../../"))
            notes_path = os.path.join(two_levels_up, "data", "notes.json")
            with open(notes_path, "w") as file:
                
                json.dump(self.notebook.notes, file)
            self.update_window_size()
    def view_note(self):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            note_data = self.notebook.get_notes()[index]
            
            # Crear una nueva ventana para mostrar la nota y la fecha
            viewNote_window = tk.Toplevel(self.root)
            viewNote_window.title("Ver Nota")

            current_dir = os.path.dirname(__file__)
            two_levels_up = os.path.abspath(os.path.join(current_dir, "../../"))
            icon_path = os.path.join(two_levels_up, "data", "logo.ico")
            viewNote_window.iconbitmap(icon_path)

            text = note_data.get("text")
            note_text=text[3:].strip()
            note_date = note_data.get("date")
            
            note_limit = note_data.get("limit")

            # Mostrar el texto de la nota y la fecha en la nueva ventana
            # Primera etiqueta: Nota
            note_label = ttk.Label(viewNote_window, text=f"Nota: \"{note_text}\"", background="#01add3", foreground="white", font=("Helvetica", 18))
            note_label.pack(padx=15, pady=5)

            # Segunda etiqueta: Fecha de creación
            created_label = ttk.Label(viewNote_window, text=f"Fecha de creación: {note_date}", background="#01add3", foreground="white", font=("Helvetica", 13))
            created_label.pack(padx=15, pady=5)

            # Tercera etiqueta: Fecha límite
            if note_limit:
                limit_label = ttk.Label(viewNote_window, text=f"Fecha límite: {note_limit}", background="#01add3", foreground="white", font=("Helvetica", 13))
                limit_label.pack(padx=15, pady=5)

            screen_width = viewNote_window.winfo_screenwidth()
            screen_height = viewNote_window.winfo_screenheight()

            window_width = int(screen_width * 20 / 100)
            window_height = int(screen_height * 10 / 100)

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2

            viewNote_window.geometry(f"{window_width}x{window_height}+{x}+{y}")


    def save_note_and_close(self, window, note_text):
        if note_text in (None, ""):
            messagebox.showwarning("Advertencia", "¡Ingrese una nota!")
            window.destroy()
        # Guardar la nueva nota
        current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not(self.selected_date in ("",None)):
            note_with_time = {"text": "  • "+note_text, "date": current_time, "limit":self.selected_date}
        else :
            note_with_time = {"text": "  • "+note_text, "date": current_time}

        self.notebook.add_note(note_with_time)
        # Guardar todas las notas en el archivo JSON
        self.save_notes()
        self.update_note_listbox()
        self.update_window_size()
        window.destroy()

    def load_notes(self):
        try:
            current_dir = os.path.dirname(__file__)
            two_levels_up = os.path.abspath(os.path.join(current_dir, "../../"))
            notes_path = os.path.join(two_levels_up, "data", "notes.json")
            with open(notes_path, "r") as file:
               
                notes = json.load(file)
                
                for note in notes:
                    self.notebook.add_note(note)
        except FileNotFoundError:
            # Si el archivo no existe, no se cargan notas (puede ser la primera ejecución)
            pass
        except json.JSONDecodeError:
            # Si hay un error en el formato JSON, se cargan las notas existentes
            pass

    def save_notes(self):
        notes = self.notebook.get_notes()
        current_dir = os.path.dirname(__file__)
        two_levels_up = os.path.abspath(os.path.join(current_dir, "../../"))
        notes_path = os.path.join(two_levels_up, "data", "notes.json")
        with open(notes_path, "w") as file:
            json.dump(notes, file)

    def update_note_listbox(self):
        # Actualizar el listado de notas en el ListBox
        notes = self.notebook.get_notes()
        self.note_listbox.delete(0, tk.END)
        for note in notes:
            self.note_listbox.insert(tk.END, note.get("text"))

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