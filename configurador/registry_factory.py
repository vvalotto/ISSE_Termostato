"""
Clase base para factories con registro dinamico de implementaciones.

Patron de Diseno:
    - Registry: Permite registrar implementaciones sin modificar la factory
    - OCP: Abierto para extension, cerrado para modificacion
"""


class RegistryFactory:
    """
    Factory base con registro dinamico de implementaciones.

    Cada subclase debe declarar su propio atributo de clase `_registry = {}`
    para mantener registros separados por tipo de componente.

    Uso:
        class MiFactory(RegistryFactory):
            _registry = {}

        MiFactory.registrar("tipo", lambda **kw: MiClase(**kw))
        instancia = MiFactory.crear("tipo", param=valor)

    Patron de Diseno:
        - Registry: Mapa de tipo -> callable para construccion
        - OCP: Agregar un nuevo tipo solo requiere llamar a registrar()
    """

    _registry = {}

    @classmethod
    def registrar(cls, tipo, factory_fn):
        """
        Registra una funcion constructora para un tipo dado.

        Args:
            tipo (str): Identificador del tipo de componente.
            factory_fn (callable): Funcion que crea la instancia.
                Debe aceptar **kwargs y retornar el objeto construido.
        """
        cls._registry[tipo] = factory_fn

    @classmethod
    def crear(cls, tipo, **kwargs):
        """
        Crea una instancia del tipo registrado.

        Args:
            tipo (str): Tipo de componente a crear.
            **kwargs: Argumentos de construccion (host, puerto, api_url, etc.).

        Returns:
            Instancia del componente, o None si el tipo no esta registrado.
        """
        factory_fn = cls._registry.get(tipo)
        if factory_fn is None:
            return None
        return factory_fn(**kwargs)
