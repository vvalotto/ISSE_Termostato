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
        """Si falta una clave debe lanzar KeyError al cargar configuracion"""
        # Configuracion incompleta (falta proxy_bateria)
        config_incompleta = json.dumps({
            "climatizador": "climatizador"
        })

        with patch("builtins.open", mock_open(read_data=config_incompleta)):
            with pytest.raises(KeyError):
                Configurador.cargar_configuracion()


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


class TestConfiguradorMetodosRed:
    """Tests para los métodos de configuración de red (Fase 1)"""

    def test_obtener_host_escucha_con_config(self):
        """Con configuración de red debe retornar el host configurado"""
        Configurador.configuracion_termostato = {
            "red": {
                "host_escucha": "0.0.0.0",
                "puertos": {
                    "bateria": 11000,
                    "temperatura": 12000,
                    "seteo_temperatura": 13000
                },
                "api_url": "http://192.168.1.100:5050"
            }
        }

        resultado = Configurador.obtener_host_escucha()
        assert resultado == "0.0.0.0"

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_host_escucha_sin_config_usa_default(self):
        """Sin configuración de red debe usar valor por defecto 'localhost'"""
        Configurador.configuracion_termostato = {
            "proxy_bateria": "socket"
        }

        resultado = Configurador.obtener_host_escucha()
        assert resultado == "localhost"

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_puerto_bateria_con_config(self):
        """Con configuración debe retornar puerto de batería configurado"""
        Configurador.configuracion_termostato = {
            "red": {
                "host_escucha": "0.0.0.0",
                "puertos": {
                    "bateria": 11000,
                    "temperatura": 12000,
                    "seteo_temperatura": 13000
                }
            }
        }

        resultado = Configurador.obtener_puerto("bateria")
        assert resultado == 11000

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_puerto_temperatura_con_config(self):
        """Con configuración debe retornar puerto de temperatura configurado"""
        Configurador.configuracion_termostato = {
            "red": {
                "puertos": {
                    "bateria": 11000,
                    "temperatura": 12000,
                    "seteo_temperatura": 13000
                }
            }
        }

        resultado = Configurador.obtener_puerto("temperatura")
        assert resultado == 12000

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_puerto_seteo_temperatura_con_config(self):
        """Con configuración debe retornar puerto de seteo temperatura configurado"""
        Configurador.configuracion_termostato = {
            "red": {
                "puertos": {
                    "bateria": 11000,
                    "temperatura": 12000,
                    "seteo_temperatura": 13000
                }
            }
        }

        resultado = Configurador.obtener_puerto("seteo_temperatura")
        assert resultado == 13000

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_puerto_sin_config_usa_default(self):
        """Sin configuración debe usar valores por defecto"""
        Configurador.configuracion_termostato = {
            "proxy_bateria": "socket"
        }

        resultado_bateria = Configurador.obtener_puerto("bateria")
        resultado_temperatura = Configurador.obtener_puerto("temperatura")
        resultado_seteo = Configurador.obtener_puerto("seteo_temperatura")

        assert resultado_bateria == 11000
        assert resultado_temperatura == 12000
        assert resultado_seteo == 13000

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_api_url_con_config(self):
        """Con configuración de red debe retornar la URL configurada"""
        Configurador.configuracion_termostato = {
            "red": {
                "host_escucha": "0.0.0.0",
                "puertos": {
                    "bateria": 11000
                },
                "api_url": "http://192.168.1.100:5050"
            }
        }

        resultado = Configurador.obtener_api_url()
        assert resultado == "http://192.168.1.100:5050"

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_api_url_sin_config_usa_default(self):
        """Sin configuración de red debe usar valor por defecto"""
        Configurador.configuracion_termostato = {
            "proxy_bateria": "socket"
        }

        resultado = Configurador.obtener_api_url()
        assert resultado == "http://localhost:5050"

        # Cleanup
        Configurador.configuracion_termostato = None

    def test_obtener_puerto_sensor_inexistente_retorna_none(self):
        """Si se solicita puerto de sensor inexistente debe retornar None"""
        Configurador.configuracion_termostato = {
            "red": {
                "puertos": {
                    "bateria": 11000,
                    "temperatura": 12000,
                    "seteo_temperatura": 13000
                }
            }
        }

        resultado = Configurador.obtener_puerto("sensor_inexistente")
        assert resultado is None

        # Cleanup
        Configurador.configuracion_termostato = None
