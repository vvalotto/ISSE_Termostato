"""
Tests unitarios para las Factories

Casos de prueba del Plan de Pruebas:

FactoryProxyBateria:
- FPB-001: tipo="archivo" -> ProxyBateriaArchivo
- FPB-002: tipo="socket" -> ProxyBateriaSocket
- FPB-003: tipo="invalido" -> None
- FPB-004: tipo="" -> None

FactoryProxySensorTemperatura:
- FAC-001: tipo="archivo" -> ProxySensorTemperaturaArchivo
- FAC-002: tipo="socket" -> ProxySensorTemperaturaSocket

FactoryActuadorClimatizador:
- FAC-003: tipo="general" -> ActuadorClimatizadorGeneral con registrador y auditor inyectados

FactoryVisualizadorBateria:
- FAC-004: tipo="archivo" -> VisualizadorBateria
- FAC-005: tipo="socket" -> VisualizadorBateriaSocket
- FAC-006: tipo="api"    -> VisualizadorBateriaApi

FactoryVisualizadorClimatizador:
- FAC-007: tipo="archivo" -> VisualizadorClimatizador
- FAC-008: tipo="socket"  -> VisualizadorClimatizadorSocket
- FAC-009: tipo="api"     -> VisualizadorClimatizadorApi

FactorySelectorTemperatura:
- FAC-010: tipo="archivo" -> SelectorTemperaturaArchivo
- FAC-011: tipo="socket"  -> SelectorTemperaturaSocket

FactorySeteoTemperatura:
- FAC-012: tipo="consola" -> SeteoTemperatura
- FAC-013: tipo="socket"  -> SeteoTemperaturaSocket

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
from unittest.mock import patch, Mock
from configurador.factory_climatizador import FactoryClimatizador
from configurador.factory_proxy_bateria import FactoryProxyBateria
from configurador.factory_visualizador_temperatura import FactoryVisualizadorTemperatura
from configurador.factory_sensor_temperatura import FactoryProxySensorTemperatura
from configurador.factory_actuador_climatizador import FactoryActuadorClimatizador
from configurador.factory_visualizador_bateria import FactoryVisualizadorBateria
from configurador.factory_visualizador_climatizador import FactoryVisualizadorClimatizador
from configurador.factory_selector_temperatura import FactorySelectorTemperatura
from configurador.factory_seteo_temperatura import FactorySeteoTemperatura
from entidades.climatizador import Climatizador, Calefactor
from agentes_sensores.proxy_bateria import ProxyBateriaArchivo, ProxyBateriaSocket
from agentes_sensores.proxy_sensor_temperatura import (
    ProxySensorTemperaturaArchivo,
    ProxySensorTemperaturaSocket,
)
from agentes_sensores.proxy_selector_temperatura import (
    SelectorTemperaturaArchivo,
    SelectorTemperaturaSocket,
)
from agentes_sensores.proxy_seteo_temperatura import SeteoTemperatura, SeteoTemperaturaSocket
from agentes_actuadores.actuador_climatizador import ActuadorClimatizadorGeneral
from agentes_actuadores.visualizador_bateria import (
    VisualizadorBateria,
    VisualizadorBateriaSocket,
    VisualizadorBateriaApi,
)
from agentes_actuadores.visualizador_climatizador import (
    VisualizadorClimatizador,
    VisualizadorClimatizadorSocket,
    VisualizadorClimatizadorApi,
)
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


class TestFactoryProxySensorTemperatura:

    # FAC-001
    def test_crear_tipo_archivo(self):
        """tipo 'archivo' retorna ProxySensorTemperaturaArchivo"""
        resultado = FactoryProxySensorTemperatura.crear("archivo")
        assert isinstance(resultado, ProxySensorTemperaturaArchivo)

    # FAC-002
    def test_crear_tipo_socket(self):
        """tipo 'socket' retorna ProxySensorTemperaturaSocket con host/puerto"""
        resultado = FactoryProxySensorTemperatura.crear("socket", host="0.0.0.0", puerto=12000)
        assert isinstance(resultado, ProxySensorTemperaturaSocket)


class TestFactoryActuadorClimatizador:

    # FAC-003
    def test_crear_tipo_general_con_di(self):
        """tipo 'general' retorna ActuadorClimatizadorGeneral con registrador y auditor inyectados"""
        resultado = FactoryActuadorClimatizador.crear("general")
        assert isinstance(resultado, ActuadorClimatizadorGeneral)
        assert resultado._registrador is not None
        assert resultado._auditor is not None


class TestFactoryVisualizadorBateria:

    # FAC-004
    def test_crear_tipo_archivo(self):
        """tipo 'archivo' retorna VisualizadorBateria"""
        resultado = FactoryVisualizadorBateria.crear("archivo")
        assert isinstance(resultado, VisualizadorBateria)

    # FAC-005
    def test_crear_tipo_socket(self):
        """tipo 'socket' retorna VisualizadorBateriaSocket"""
        resultado = FactoryVisualizadorBateria.crear("socket", host="0.0.0.0", puerto=11000)
        assert isinstance(resultado, VisualizadorBateriaSocket)

    # FAC-006
    def test_crear_tipo_api(self):
        """tipo 'api' retorna VisualizadorBateriaApi"""
        resultado = FactoryVisualizadorBateria.crear("api", api_url="http://localhost/api")
        assert isinstance(resultado, VisualizadorBateriaApi)


class TestFactoryVisualizadorClimatizador:

    # FAC-007
    def test_crear_tipo_archivo(self):
        """tipo 'archivo' retorna VisualizadorClimatizador"""
        resultado = FactoryVisualizadorClimatizador.crear("archivo")
        assert isinstance(resultado, VisualizadorClimatizador)

    # FAC-008
    def test_crear_tipo_socket(self):
        """tipo 'socket' retorna VisualizadorClimatizadorSocket"""
        resultado = FactoryVisualizadorClimatizador.crear("socket", host="0.0.0.0", puerto=14002)
        assert isinstance(resultado, VisualizadorClimatizadorSocket)

    # FAC-009
    def test_crear_tipo_api(self):
        """tipo 'api' retorna VisualizadorClimatizadorApi"""
        resultado = FactoryVisualizadorClimatizador.crear("api", api_url="http://localhost/api")
        assert isinstance(resultado, VisualizadorClimatizadorApi)


class TestFactorySelectorTemperatura:

    # FAC-010
    def test_crear_tipo_archivo(self):
        """tipo 'archivo' retorna SelectorTemperaturaArchivo"""
        resultado = FactorySelectorTemperatura.crear("archivo")
        assert isinstance(resultado, SelectorTemperaturaArchivo)

    # FAC-011
    def test_crear_tipo_socket(self):
        """tipo 'socket' retorna SelectorTemperaturaSocket"""
        mock_srv = Mock()
        mock_srv.accept.side_effect = __import__("socket").timeout
        with patch("socket.socket", return_value=mock_srv):
            resultado = FactorySelectorTemperatura.crear("socket", host="0.0.0.0", puerto=14000)
        assert isinstance(resultado, SelectorTemperaturaSocket)


class TestFactorySeteoTemperatura:

    # FAC-012
    def test_crear_tipo_consola(self):
        """tipo 'consola' retorna SeteoTemperatura"""
        resultado = FactorySeteoTemperatura.crear("consola")
        assert isinstance(resultado, SeteoTemperatura)

    # FAC-013
    def test_crear_tipo_socket(self):
        """tipo 'socket' retorna SeteoTemperaturaSocket"""
        mock_srv = Mock()
        with patch("socket.socket", return_value=mock_srv):
            resultado = FactorySeteoTemperatura.crear("socket", host="0.0.0.0", puerto=13000)
        assert isinstance(resultado, SeteoTemperaturaSocket)
