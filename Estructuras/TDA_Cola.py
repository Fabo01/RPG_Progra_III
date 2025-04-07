class TDA_Cola:
    """
    Implementación de la estructura de datos Cola (FIFO - First In First Out)
    para gestionar misiones en el sistema RPG.
    """
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Añade un elemento al final de la cola"""
        self.items.append(item)
    
    def dequeue(self):
        """Elimina y retorna el primer elemento de la cola"""
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def first(self):
        """Retorna el primer elemento de la cola sin eliminarlo"""
        if self.is_empty():
            return None
        return self.items[0]
    
    def is_empty(self):
        """Verifica si la cola está vacía"""
        return len(self.items) == 0
    
    def size(self):
        """Retorna la cantidad de elementos en la cola"""
        return len(self.items)
