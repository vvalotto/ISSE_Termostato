from os import system


class Inicializador:

    @staticmethod
    def iniciar(gestor_bateria, gestor_ambiente, presentador):

        print("INICIO")

        gestor_ambiente.ambiente.temperatura_deseada = 24

        print("lee_bateria")
        gestor_bateria.verificar_nivel_de_carga()
        if gestor_bateria.obtener_indicador_de_carga() != "NORMAL":
            return False

        print("lee temperatura")
        gestor_ambiente.leer_temperatura_ambiente()
        if gestor_ambiente.obtener_temperatura_ambiente() is None:
            return False

        print("Muestra estado Termostato")
        presentador.ejecutar()

        system("clear")
        return True
