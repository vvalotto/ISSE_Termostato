"""
Tests unitarios para las Factories

Casos de prueba del Plan de Pruebas:

FactoryProxyBateria:
- FPB-001: tipo="archivo" -> ProxyBateriaArchivo
- FPB-002: tipo="socket" -> ProxyBateriaSocket
- FPB-003: tipo="invalido" -> None
- FPB-004: tipo="" -> None

FactoryClimatizador:
- FCL-001: tipo="climatizador" -> Climatizador
- FCL-002: tipo="calefactor" -> Calefactor
- FCL-003: tipo="invalido" -> None

FactoryVisualizador*:
- FVI-001: tipo="archivo" -> Visualizador* (consola/archivo)
- FVI-002: tipo="socket" -> Visualizador*Socket
- FVI-003: tipo="api" -> Visualizador*Api
- FVI-004: tipo="invalido" -> None
"""
import pytest
from configurador.factory_climatizador import FactoryClimatizador
from configurador.factory_proxy_bateria import FactoryProxyBateria
from configurador.factory_visualizador_temperatura import FactoryVisualizadorTemperatura
from entidades.climatizador import Climatizador, Calefactor
from agentes_sensores.proxy_bateria import ProxyBateriaArchivo, ProxyBateriaSocket
from agentes_actuadores.visualizador_temperatura import (
    VisualizadorTemperatura,
    VisualizadorTemperaturaSocket,
    VisualizadorTemperaturaApi
)


class TestFactoryClimatizador:
    """Tests para FactoryClimatizador"""

    # FCL-001: tipo="climatizador" -> Climatizador
    def test_crear_climatizador(self):
        """Con tipo 'climatizador' debe retornar instancia de Climatizador"""
        resultado = FactoryClimatizador.crear("climatizador")
        assert isinstance(resultado, Climatizador)

    # FCL-002: tipo="calefactor" -> Calefactor
    def test_crear_calefactor(self):
        """Con tipo 'calefactor' debe retornar instancia de Calefactor"""
        resultado = FactoryClimatizador.crear("calefactor")
        assert isinstance(resultado, Calefactor)

    # FCL-003: tipo="invalido" -> None
    def test_tipo_invalido_retorna_none(self):
        """Con tipo invalido debe retornar None"""
        resultado = FactoryClimatizador.crear("invalido")
        assert resultado is None

    def test_tipo_vacio_retorna_none(self):
        """Con tipo vacio debe retornar None"""
        resultado = FactoryClimatizador.crear("")
        assert resultado is None

    @pytest.mark.parametrize("tipo,clase_esperada", [
        ("climatizador", Climatizador),
        ("calefactor", Calefactor),
    ])
    def test_crear_tipos_validos(self, tipo, clase_esperada):
        """Verifica creacion de tipos validos"""
        resultado = FactoryClimatizador.crear(tipo)
        assert isinstance(resultado, clase_esperada)

    @pytest.mark.parametrize("tipo_invalido", [
        "invalido",
        "",
        "CLIMATIZADOR",  # Case sensitive
        "Calefactor",    # Case sensitive
        None,
    ])
    def test_tipos_invalidos_retornan_none(self, tipo_invalido):
        """Verifica que tipos invalidos retornan None"""
        resultado = FactoryClimatizador.crear(tipo_invalido)
        assert resultado is None


class TestFactoryProxyBateria:
    """Tests para FactoryProxyBateria"""

    # FPB-001: tipo="archivo" -> ProxyBateriaArchivo
    def test_crear_proxy_archivo(self):
        """Con tipo 'archivo' debe retornar instancia de ProxyBateriaArchivo"""
        resultado = FactoryProxyBateria.crear("archivo")
        assert isinstance(resultado, ProxyBateriaArchivo)

    # FPB-002: tipo="socket" -> ProxyBateriaSocket
    def test_crear_proxy_socket(self):
        """Con tipo 'socket' debe retornar instancia de ProxyBateriaSocket"""
        resultado = FactoryProxyBateria.crear("socket")
        assert isinstance(resultado, ProxyBateriaSocket)

    # FPB-003: tipo="invalido" -> None
    def test_tipo_invalido_retorna_none(self):
        """Con tipo invalido debe retornar None"""
        resultado = FactoryProxyBateria.crear("invalido")
        assert resultado is None

    # FPB-004: tipo="" -> None
    def test_tipo_vacio_retorna_none(self):
        """Con tipo vacio debe retornar None"""
        resultado = FactoryProxyBateria.crear("")
        assert resultado is None

    @pytest.mark.parametrize("tipo,clase_esperada", [
        ("archivo", ProxyBateriaArchivo),
        ("socket", ProxyBateriaSocket),
    ])
    def test_crear_tipos_validos(self, tipo, clase_esperada):
        """Verifica creacion de tipos validos"""
        resultado = FactoryProxyBateria.crear(tipo)
        assert isinstance(resultado, clase_esperada)


class TestFactoryVisualizadorTemperatura:
    """Tests para FactoryVisualizadorTemperatura"""

    # FVI-001: tipo="archivo" -> VisualizadorTemperatura
    def test_crear_visualizador_archivo(self):
        """Con tipo 'archivo' debe retornar instancia de VisualizadorTemperatura"""
        resultado = FactoryVisualizadorTemperatura.crear("archivo")
        assert isinstance(resultado, VisualizadorTemperatura)

    # FVI-002: tipo="socket" -> VisualizadorTemperaturaSocket
    def test_crear_visualizador_socket(self):
        """Con tipo 'socket' debe retornar instancia de VisualizadorTemperaturaSocket"""
        resultado = FactoryVisualizadorTemperatura.crear("socket")
        assert isinstance(resultado, VisualizadorTemperaturaSocket)

    # FVI-003: tipo="api" -> VisualizadorTemperaturaApi
    def test_crear_visualizador_api(self):
        """Con tipo 'api' debe retornar instancia de VisualizadorTemperaturaApi"""
        resultado = FactoryVisualizadorTemperatura.crear("api")
        assert isinstance(resultado, VisualizadorTemperaturaApi)

    # FVI-004: tipo="invalido" -> None
    def test_tipo_invalido_retorna_none(self):
        """Con tipo invalido debe retornar None"""
        resultado = FactoryVisualizadorTemperatura.crear("invalido")
        assert resultado is None

    def test_tipo_vacio_retorna_none(self):
        """Con tipo vacio debe retornar None"""
        resultado = FactoryVisualizadorTemperatura.crear("")
        assert resultado is None

    @pytest.mark.parametrize("tipo,clase_esperada", [
        ("archivo", VisualizadorTemperatura),
        ("socket", VisualizadorTemperaturaSocket),
        ("api", VisualizadorTemperaturaApi),
    ])
    def test_crear_tipos_validos(self, tipo, clase_esperada):
        """Verifica creacion de tipos validos"""
        resultado = FactoryVisualizadorTemperatura.crear(tipo)
        assert isinstance(resultado, clase_esperada)
