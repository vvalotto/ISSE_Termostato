"""
Tests de integracion cruzada entre registrador/ y agentes_actuadores/actuador_climatizador.py

Casos de prueba:
- REG-ACT-001: accionar() escribe la accion en el archivo 'climatizador'
- REG-ACT-002: accionar() escribe la auditoria en 'registro_auditoria' con clase y mensaje
- REG-ACT-003: si 'climatizador' no se puede escribir, registrar_error() escribe en 'registro_errores'
"""
import pytest
from unittest.mock import patch, mock_open, call
from agentes_actuadores.actuador_climatizador import ActuadorClimatizadorGeneral
from registrador.registrador import RegistradorArchivo, AuditorArchivo


@pytest.fixture
def actuador(monkeypatch, tmp_path):
    """ActuadorClimatizadorGeneral con RegistradorArchivo y AuditorArchivo reales en tmp_path."""
    monkeypatch.chdir(tmp_path)
    registrador = RegistradorArchivo()
    auditor = AuditorArchivo()
    return ActuadorClimatizadorGeneral(registrador, auditor), tmp_path


class TestRegistradorActuadorIntegracion:

    # REG-ACT-001
    def test_accionar_escribe_accion_en_archivo_climatizador(self, actuador):
        """accionar('calentando') escribe 'calentando' en el archivo 'climatizador'."""
        act, tmp_path = actuador
        act.accionar_climatizador("calentando")
        contenido = (tmp_path / "climatizador").read_text(encoding="utf-8")
        assert contenido == "calentando"

    # REG-ACT-002
    def test_accionar_escribe_auditoria_con_clase_y_mensaje(self, actuador):
        """accionar() escribe en 'registro_auditoria' la clase y el mensaje correctos."""
        act, tmp_path = actuador
        act.accionar_climatizador("enfriando")
        contenido = (tmp_path / "registro_auditoria").read_text(encoding="utf-8")
        assert "ActuadorClimatizadorGeneral" in contenido
        assert "accionando el climatizador" in contenido

    # REG-ACT-003
    def test_accionar_escribe_error_en_registro_si_falla_climatizador(self, actuador):
        """Si el archivo 'climatizador' no se puede escribir, se registra el error en 'registro_errores'."""
        act, tmp_path = actuador

        def open_con_error(path, *args, **kwargs):
            if "climatizador" in str(path) and "auditoria" not in str(path):
                raise IOError("disco lleno")
            return open.__wrapped__(path, *args, **kwargs)

        import builtins
        original_open = builtins.open
        with patch("builtins.open", side_effect=lambda p, *a, **kw: (
            (_ for _ in ()).throw(IOError("disco lleno"))
            if str(p) == "climatizador"
            else original_open(p, *a, **kw)
        )):
            act.accionar_climatizador("apagado")

        contenido = (tmp_path / "registro_errores").read_text(encoding="utf-8")
        assert "Error" in contenido
