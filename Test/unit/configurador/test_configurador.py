"""
Tests unitarios para el Configurador

Casos de prueba del Plan de Pruebas:
- CFG-001: JSON valido -> Configuracion cargada
- CFG-002: Archivo no existe -> FileNotFoundError
- CFG-003: JSON malformado -> JSONDecodeError
- CFG-004: Clave faltante -> KeyError
"""
import pytest
import json
from unittest.mock import patch, mock_open
from configurador.configurador import Configurador


class TestConfiguradorCargarConfiguracion:
    """Tests para Configurador.cargar_configuracion()"""

    # CFG-001: JSON valido
    def test_cargar_configuracion_json_valido(self):
        """Con JSON valido debe cargar la configuracion correctamente"""
        config_json = json.dumps({
            "proxy_bateria": "archivo",
            "proxy_sensor_temperatura": "archivo",
            "actuador_climatizador": "archivo",
            "visualizador_temperatura": "archivo",
            "visualizador_bateria": "archivo",
            "visualizador_climatizador": "archivo",
            "climatizador": "climatizador",
            "selector_temperatura": "archivo",
            "seteo_temperatura": "archivo"
        })

        with patch("builtins.open", mock_open(read_data=config_json)):
            Configurador.cargar_configuracion()

        assert Configurador.configuracion_termostato is not None
        assert Configurador.configuracion_termostato["proxy_bateria"] == "archivo"
        assert Configurador.configuracion_termostato["climatizador"] == "climatizador"

    # CFG-002: Archivo no existe
    def test_cargar_configuracion_archivo_no_existe(self):
        """Si el archivo no existe debe lanzar FileNotFoundError"""
        with patch("builtins.open", side_effect=FileNotFoundError("No such file")):
            with pytest.raises(FileNotFoundError):
                Configurador.cargar_configuracion()

    # CFG-003: JSON malformado
    def test_cargar_configuracion_json_malformado(self):
        """Con JSON malformado debe lanzar JSONDecodeError"""
        json_invalido = "{ esto no es json valido }"

        with patch("builtins.open", mock_open(read_data=json_invalido)):
            with pytest.raises(json.JSONDecodeError):
                Configurador.cargar_configuracion()

    # CFG-004: Clave faltante (se prueba en los metodos configurar_*)
    def test_configurar_con_clave_faltante_lanza_keyerror(self):
        """Si falta una clave debe lanzar KeyError al configurar"""
        # Configuracion incompleta (falta proxy_bateria)
        config_incompleta = json.dumps({
            "climatizador": "climatizador"
        })

        with patch("builtins.open", mock_open(read_data=config_incompleta)):
            Configurador.cargar_configuracion()

        with pytest.raises(KeyError):
            Configurador.configurar_proxy_bateria()


class TestConfiguradorMetodosConfigurar:
    """Tests para los metodos configurar_* del Configurador"""

    @pytest.fixture(autouse=True)
    def setup_configuracion(self):
        """Setup: cargar configuracion valida antes de cada test"""
        Configurador.configuracion_termostato = {
            "proxy_bateria": "archivo",
            "proxy_sensor_temperatura": "archivo",
            "actuador_climatizador": "archivo",
            "visualizador_temperatura": "archivo",
            "visualizador_bateria": "archivo",
            "visualizador_climatizador": "archivo",
            "climatizador": "climatizador",
            "selector_temperatura": "archivo",
            "seteo_temperatura": "archivo"
        }
        yield
        # Teardown: limpiar configuracion
        Configurador.configuracion_termostato = None

    def test_configurar_proxy_bateria(self):
        """Debe crear el proxy de bateria segun configuracion"""
        from agentes_sensores.proxy_bateria import ProxyBateriaArchivo
        resultado = Configurador.configurar_proxy_bateria()
        assert isinstance(resultado, ProxyBateriaArchivo)

    def test_configurar_climatizador(self):
        """Debe crear el climatizador segun configuracion"""
        from entidades.climatizador import Climatizador
        resultado = Configurador.configurar_climatizador()
        assert isinstance(resultado, Climatizador)

    def test_configurar_visualizador_temperatura(self):
        """Debe crear el visualizador de temperatura segun configuracion"""
        from agentes_actuadores.visualizador_temperatura import VisualizadorTemperatura
        resultado = Configurador.configurar_visualizador_temperatura()
        assert isinstance(resultado, VisualizadorTemperatura)


class TestConfiguradorConfiguracionesAlternativas:
    """Tests para verificar configuraciones alternativas"""

    def test_configuracion_con_socket(self):
        """Debe soportar configuracion con socket"""
        Configurador.configuracion_termostato = {
            "proxy_bateria": "socket",
            "climatizador": "calefactor"
        }

        from agentes_sensores.proxy_bateria import ProxyBateriaSocket
        from entidades.climatizador import Calefactor

        proxy = Configurador.configurar_proxy_bateria()
        climatizador = Configurador.configurar_climatizador()

        assert isinstance(proxy, ProxyBateriaSocket)
        assert isinstance(climatizador, Calefactor)

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_configuracion_con_api(self):
        """Debe soportar configuracion con API"""
        Configurador.configuracion_termostato = {
            "visualizador_temperatura": "api"
        }

        from agentes_actuadores.visualizador_temperatura import VisualizadorTemperaturaApi
        resultado = Configurador.configurar_visualizador_temperatura()
        assert isinstance(resultado, VisualizadorTemperaturaApi)

        # Cleanup
        Configurador.configuracion_termostato = None
