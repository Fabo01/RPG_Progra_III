class ColaVaciaError(Exception):
    """Excepción lanzada cuando se intenta acceder a una cola vacía."""
    pass

class MisionNoEncontradaError(Exception):
    """Excepción lanzada cuando no se encuentra una misión."""
    pass

class PersonajeNoEncontradoError(Exception):
    """Excepción lanzada cuando no se encuentra un personaje."""
    pass
