# notebook.py

class Notebook:
    def __init__(self):
        # Inicializa una lista para almacenar las notas
        self.notes = []

    def delete_index(self,index):
        del self.notes[index]

    def add_note(self, note):
        # Agrega una nota a la lista
        self.notes.append(note)

    def delete_note(self, note):
        # Elimina una nota de la lista
        if note in self.notes:
            self.notes.remove(note)

    def get_notes(self):
        # Obtiene la lista de notas
        return self.notes
