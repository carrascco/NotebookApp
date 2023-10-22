# main.py
from tkinter import Tk
from notebook.gui.main_window import MainWindow

def main():
    # Inicializa la ventana principal de la aplicación
    root = Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
