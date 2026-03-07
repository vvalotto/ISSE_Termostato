"""
Tests unitarios para registrador/registrador.py

Casos de prueba:
- REG-001: RegistradorArchivo.registrar_error con mensaje valido -> escribe en registro_errores
- REG-002: RegistradorArchivo.registrar_error con IOError -> lanza IOError
- REG-003: AuditorArchivo.auditar_funcion con datos validos -> escribe clase, fecha_hora y mensaje
- REG-004: AuditorArchivo.auditar_funcion con IOError -> lanza IOError
- REG-005: Contenido del archivo de auditoria -> formato correcto con separador *************
"""
import pytest
from unittest.mock import patch
from registrador.registrador import RegistradorArchivo, AuditorArchivo


class TestRegistradorArchivo:

    # REG-001
    def test_registrar_error_escribe_mensaje(self, tmp_path, monkeypatch):
        """Cuando se llama registrar_error, escribe el mensaje en registro_errores"""
        monkeypatch.chdir(tmp_path)
        RegistradorArchivo.registrar_error("error de prueba")
        contenido = (tmp_path / "registro_errores").read_text()
        assert contenido == "error de prueba"

    # REG-002
    def test_registrar_error_ioerror_lanza_excepcion(self):
        """Cuando el archivo no se puede escribir, lanza IOError con mensaje descriptivo"""
        with patch("builtins.open", side_effect=IOError("disco lleno")):
            with pytest.raises(IOError):
                RegistradorArchivo.registrar_error("error")


class TestAuditorArchivo:

    # REG-003
    def test_auditar_funcion_escribe_campos(self, tmp_path, monkeypatch):
        """Cuando se llama auditar_funcion, escribe clase, fecha_hora y mensaje en el archivo"""
        monkeypatch.chdir(tmp_path)
        AuditorArchivo.auditar_funcion("MiClase", "accion realizada", "2026-03-07T10:00:00")
        contenido = (tmp_path / "registro_auditoria").read_text()
        assert "clase: MiClase" in contenido
        assert "fecha_hora: 2026-03-07T10:00:00" in contenido
        assert "mensaje: accion realizada" in contenido

    # REG-004
    def test_auditar_funcion_ioerror_lanza_excepcion(self):
        """Cuando el archivo no se puede escribir, lanza IOError con mensaje descriptivo"""
        with patch("builtins.open", side_effect=IOError("disco lleno")):
            with pytest.raises(IOError):
                AuditorArchivo.auditar_funcion("MiClase", "mensaje", "2026-03-07")

    # REG-005
    def test_auditar_funcion_formato_separador(self, tmp_path, monkeypatch):
        """El contenido escrito incluye el separador ************* entre entradas"""
        monkeypatch.chdir(tmp_path)
        AuditorArchivo.auditar_funcion("ClaseTest", "evento test", "2026-03-07")
        contenido = (tmp_path / "registro_auditoria").read_text()
        assert "*************" in contenido
