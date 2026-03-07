"""
Tests unitarios para agentes_actuadores/actuador_climatizador.py

Casos de prueba:
- ACT-001: accionar_climatizador("calentar") -> llama auditar_funcion y escribe en archivo
- ACT-002: accionar_climatizador("enfriar")  -> idem para enfriamiento
- ACT-003: accionar_climatizador("apagar")   -> idem para apagado
- ACT-004: error de escritura en archivo     -> llama registrar_error en registrador
- ACT-005: constructor inyecta registrador y auditor -> asignados en _registrador y _auditor
- ACT-006: auditar_funcion recibe clase y mensaje correctos
"""
import pytest
from unittest.mock import Mock, patch
from agentes_actuadores.actuador_climatizador import ActuadorClimatizadorGeneral


@pytest.fixture
def actuador():
    registrador = Mock()
    auditor = Mock()
    return ActuadorClimatizadorGeneral(registrador, auditor)


class TestActuadorClimatizadorConstructor:

    # ACT-005
    def test_constructor_inyecta_registrador_y_auditor(self):
        """El constructor asigna registrador y auditor como atributos privados"""
        registrador = Mock()
        auditor = Mock()
        act = ActuadorClimatizadorGeneral(registrador, auditor)
        assert act._registrador is registrador
        assert act._auditor is auditor


class TestActuadorClimatizadorAccionar:

    # ACT-001
    def test_accionar_calentar_escribe_en_archivo(self, actuador, tmp_path, monkeypatch):
        """accionar_climatizador('calentar') escribe 'calentar' en el archivo climatizador"""
        monkeypatch.chdir(tmp_path)
        actuador.accionar_climatizador("calentar")
        assert (tmp_path / "climatizador").read_text() == "calentar"

    # ACT-002
    def test_accionar_enfriar_escribe_en_archivo(self, actuador, tmp_path, monkeypatch):
        """accionar_climatizador('enfriar') escribe 'enfriar' en el archivo climatizador"""
        monkeypatch.chdir(tmp_path)
        actuador.accionar_climatizador("enfriar")
        assert (tmp_path / "climatizador").read_text() == "enfriar"

    # ACT-003
    def test_accionar_apagar_escribe_en_archivo(self, actuador, tmp_path, monkeypatch):
        """accionar_climatizador('apagar') escribe 'apagar' en el archivo climatizador"""
        monkeypatch.chdir(tmp_path)
        actuador.accionar_climatizador("apagar")
        assert (tmp_path / "climatizador").read_text() == "apagar"

    # ACT-006
    def test_accionar_llama_auditar_con_clase_y_mensaje(self, actuador, tmp_path, monkeypatch):
        """accionar_climatizador llama auditar_funcion con el nombre de clase y mensaje correcto"""
        monkeypatch.chdir(tmp_path)
        actuador.accionar_climatizador("calentar")
        actuador._auditor.auditar_funcion.assert_called_once()
        args = actuador._auditor.auditar_funcion.call_args[0]
        assert args[0] == "ActuadorClimatizadorGeneral"
        assert args[1] == "accionando el climatizador"

    # ACT-004
    def test_accionar_ioerror_llama_registrar_error(self, actuador):
        """Cuando la escritura en archivo falla, llama registrar_error en el registrador"""
        with patch("builtins.open", side_effect=IOError("disco lleno")):
            actuador.accionar_climatizador("calentar")
        actuador._registrador.registrar_error.assert_called_once()
