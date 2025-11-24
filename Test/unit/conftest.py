"""
Fixtures compartidas para tests unitarios de entidades
"""
import pytest

from entidades.bateria import Bateria
from entidades.ambiente import Ambiente
from entidades.climatizador import Climatizador, Calefactor


# ============ FIXTURES BATERIA ============

@pytest.fixture
def bateria_default():
    """Bateria con valores por defecto: carga_maxima=5, umbral=0.8"""
    return Bateria(carga_maxima=5, umbral_del_carga=0.8)


# ============ FIXTURES AMBIENTE ============

@pytest.fixture
def ambiente_default():
    """Ambiente con valores por defecto"""
    return Ambiente()


@pytest.fixture
def ambiente_frio():
    """Ambiente con temperatura baja (necesita calefaccion)"""
    ambiente = Ambiente()
    ambiente.temperatura_ambiente = 18
    ambiente.temperatura_deseada = 22
    return ambiente


@pytest.fixture
def ambiente_caliente():
    """Ambiente con temperatura alta (necesita enfriamiento)"""
    ambiente = Ambiente()
    ambiente.temperatura_ambiente = 28
    ambiente.temperatura_deseada = 22
    return ambiente


@pytest.fixture
def ambiente_normal():
    """Ambiente con temperatura normal (no requiere accion)"""
    ambiente = Ambiente()
    ambiente.temperatura_ambiente = 22
    ambiente.temperatura_deseada = 22
    return ambiente


# ============ FIXTURES CLIMATIZADOR ============

@pytest.fixture
def climatizador():
    """Climatizador (puede calentar y enfriar)"""
    return Climatizador()


@pytest.fixture
def calefactor():
    """Calefactor (solo puede calentar)"""
    return Calefactor()
