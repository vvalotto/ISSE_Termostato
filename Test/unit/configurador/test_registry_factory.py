"""
Tests unitarios para configurador/registry_factory.py

Casos de prueba:
- REG-F-001: registrar + crear con tipo registrado -> retorna instancia correcta
- REG-F-002: crear con tipo no registrado -> retorna None
- REG-F-003: dos subclases con _registry propio -> registros independientes
- REG-F-004: registrar sobreescribe tipo existente -> nueva funcion reemplaza la anterior
- REG-F-005: crear pasa **kwargs a la factory function -> kwargs llegan correctamente
"""
from configurador.registry_factory import RegistryFactory


class TestRegistryFactory:

    # REG-F-001
    def test_registrar_y_crear_tipo_registrado(self):
        """registrar + crear con tipo registrado retorna la instancia producida por la factory"""
        class MiFactory(RegistryFactory):
            _registry = {}

        sentinel = object()
        MiFactory.registrar("tipo_a", lambda **kw: sentinel)
        resultado = MiFactory.crear("tipo_a")
        assert resultado is sentinel

    # REG-F-002
    def test_crear_tipo_no_registrado_retorna_none(self):
        """crear con tipo no registrado retorna None"""
        class MiFactory(RegistryFactory):
            _registry = {}

        resultado = MiFactory.crear("no_existe")
        assert resultado is None

    # REG-F-003
    def test_subclases_con_registry_propio_son_independientes(self):
        """Dos subclases con _registry propio no comparten sus registros"""
        class FactoryA(RegistryFactory):
            _registry = {}

        class FactoryB(RegistryFactory):
            _registry = {}

        FactoryA.registrar("exclusivo_a", lambda **kw: "instancia_a")

        assert FactoryA.crear("exclusivo_a") == "instancia_a"
        assert FactoryB.crear("exclusivo_a") is None

    # REG-F-004
    def test_registrar_sobreescribe_tipo_existente(self):
        """registrar sobre un tipo ya registrado reemplaza la factory anterior"""
        class MiFactory(RegistryFactory):
            _registry = {}

        MiFactory.registrar("tipo_x", lambda **kw: "primera")
        MiFactory.registrar("tipo_x", lambda **kw: "segunda")
        assert MiFactory.crear("tipo_x") == "segunda"

    # REG-F-005
    def test_crear_pasa_kwargs_a_factory_fn(self):
        """crear pasa los kwargs recibidos a la factory function"""
        class MiFactory(RegistryFactory):
            _registry = {}

        recibidos = {}

        def factory_captura(**kwargs):
            recibidos.update(kwargs)
            return object()

        MiFactory.registrar("con_kwargs", factory_captura)
        MiFactory.crear("con_kwargs", host="localhost", puerto=8080)

        assert recibidos["host"] == "localhost"
        assert recibidos["puerto"] == 8080
