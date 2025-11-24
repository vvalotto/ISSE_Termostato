"""
Tests unitarios para la entidad Bateria

Casos de prueba del Plan de Pruebas:
- BAT-001: Carga sobre umbral -> indicador="NORMAL"
- BAT-002: Carga igual a umbral -> indicador="NORMAL"
- BAT-003: Carga bajo umbral -> indicador="BAJA"
- BAT-004: Carga cero -> indicador="BAJA"
- BAT-005: Carga maxima -> indicador="NORMAL"
- BAT-006: Valor limite inferior -> indicador="BAJA"
"""
import pytest
from entidades.bateria import Bateria


class TestBateria:
    """Tests para la clase Bateria"""

    # BAT-001: Carga sobre umbral
    def test_carga_sobre_umbral_indicador_normal(self, bateria_default):
        """Cuando la carga esta sobre el umbral (80%), el indicador debe ser NORMAL"""
        bateria_default.nivel_de_carga = 4.5  # 90% de 5
        assert bateria_default.indicador == "NORMAL"

    # BAT-002: Carga igual a umbral
    def test_carga_igual_umbral_indicador_baja(self, bateria_default):
        """Cuando la carga es exactamente el umbral (80%), el indicador debe ser BAJA (umbral inclusive)"""
        bateria_default.nivel_de_carga = 4.0  # 80% de 5
        assert bateria_default.indicador == "BAJA"

    # BAT-003: Carga bajo umbral
    def test_carga_bajo_umbral_indicador_baja(self, bateria_default):
        """Cuando la carga esta bajo el umbral (80%), el indicador debe ser BAJA"""
        bateria_default.nivel_de_carga = 3.9  # 78% de 5
        assert bateria_default.indicador == "BAJA"

    # BAT-004: Carga cero
    def test_carga_cero_indicador_baja(self, bateria_default):
        """Cuando la carga es cero, el indicador debe ser BAJA"""
        bateria_default.nivel_de_carga = 0
        assert bateria_default.indicador == "BAJA"

    # BAT-005: Carga maxima
    def test_carga_maxima_indicador_normal(self, bateria_default):
        """Cuando la carga es maxima, el indicador debe ser NORMAL"""
        bateria_default.nivel_de_carga = 5  # 100% de 5
        assert bateria_default.indicador == "NORMAL"

    # BAT-006: Valor limite inferior
    def test_valor_limite_inferior_indicador_baja(self, bateria_default):
        """Un valor muy pequeno (0.01) debe indicar BAJA"""
        bateria_default.nivel_de_carga = 0.01
        assert bateria_default.indicador == "BAJA"


class TestBateriaParametrizado:
    """Tests parametrizados para cobertura adicional"""

    @pytest.mark.parametrize("nivel,carga_max,umbral,esperado", [
        (4.5, 5, 0.8, "NORMAL"),   # Sobre umbral
        (4.0, 5, 0.8, "BAJA"),     # Igual a umbral (inclusive)
        (3.9, 5, 0.8, "BAJA"),     # Bajo umbral
        (0, 5, 0.8, "BAJA"),       # Cero
        (5, 5, 0.8, "NORMAL"),     # Maxima
        (0.01, 5, 0.8, "BAJA"),    # Limite inferior
        (10, 10, 0.5, "NORMAL"),   # Diferentes valores
        (4.9, 10, 0.5, "BAJA"),    # Justo bajo umbral 50%
        (5.0, 10, 0.5, "BAJA"),    # Justo en umbral 50% (inclusive)
        (5.1, 10, 0.5, "NORMAL"),  # Justo sobre umbral 50%
    ])
    def test_indicador_segun_nivel_de_carga(self, nivel, carga_max, umbral, esperado):
        """Verifica el indicador para diferentes combinaciones de parametros"""
        bateria = Bateria(carga_maxima=carga_max, umbral_del_carga=umbral)
        bateria.nivel_de_carga = nivel
        assert bateria.indicador == esperado

    def test_nivel_de_carga_se_almacena_correctamente(self, bateria_default):
        """Verifica que el nivel de carga se almacene correctamente"""
        bateria_default.nivel_de_carga = 3.5
        assert bateria_default.nivel_de_carga == 3.5
