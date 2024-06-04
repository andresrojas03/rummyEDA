import random
import os
import time
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_WHITE = '\033[97m'
COLOR_RESET = '\033[0m'

class fichas():
    #crear mazos de los distintos colores y los comodines 
    amarillo =  []
    azul = []
    rojo = []
    verde = []
    comodin = []
    def __init__(self, numero, color):
        self.numero = numero
        self.color = color

class player:
    def __init__(self, nombre):
        self.nombre = nombre
        self.jugadas = []
        self.mano = []

    def llenar_mano(self):
        return self.mano
    
    def mostrar_mano(self, fichas):
        if len(self.mano) == 0:
            print("El jugador no tiene fichas en su mano")
        else:
            print("Tu mano: (el numero a la izquierda es el indice de la ficha)")
            cont = 0
            for i,ficha in enumerate(fichas):
                color = COLOR_RESET
                if ficha.color == "amarillo":
                    color = COLOR_YELLOW
                elif ficha.color == "azul":
                    color = COLOR_BLUE
                elif ficha.color == "rojo":
                    color = COLOR_RED
                elif ficha.color == "verde":
                    color = COLOR_GREEN
                elif ficha.color == "comodin":
                    color = COLOR_WHITE
                cont += 1
                print(f"{cont}:" + '[' + color + f"{ficha.numero}" + COLOR_RESET + '] ', end='')

                if (i + 1) % 7 == 0:
                    print()
            print()

    def mostrar_jugadas(self, fichas):
        if len(fichas) == 0:
            print("[]")
        else:
            print("Tus jugadas: ")
            for ficha in fichas:
                color = COLOR_RESET
                if ficha.color == "amarillo":
                    color = COLOR_YELLOW
                elif ficha.color == "azul":
                    color = COLOR_BLUE
                elif ficha.color == "rojo":
                    color = COLOR_RED
                elif ficha.color == "verde":
                    color = COLOR_GREEN
                elif ficha.color == "comodin":
                    color = COLOR_WHITE
                print('[' + color + f"{ficha.numero}" + COLOR_RESET + '] ', end='')

    def ordenar_mano(self):
        #ordenar mano usando insertion sort
        for i in range(1, len(self.mano)):
            ficha_actual = self.mano[i]
            j = i - 1
            while j >= 0 and (self.mano[j].color > ficha_actual.color or (self.mano[j].color == ficha_actual.color and self.mano[j].numero > ficha_actual.numero)):
                self.mano[j + 1] = self.mano[j]
                j -= 1
            self.mano[j + 1] = ficha_actual
        #mover los comodines al final del arreglo
        comodines = [ficha for ficha in self.mano if ficha.numero == 0 and ficha.color == "comodin"]
        self.mano = [ficha for ficha in self.mano if ficha.numero != 0 and ficha.color != "comodin"]
        self.mano.extend(comodines)
    
    def comer(self, pozo):
        comer = pozo.pop()
        print(f"Tomaste la ficha {comer.numero} de color {comer.color}")
        self.mano.append(comer)
        
        return 


    def armar_jugada(self, pozo):
        jugada = []
        self.ordenar_mano()
        self.mostrar_mano(self.mano)
        while True:
            print()
            opcion = int(input("Que desea hacer? 1.Armar jugada 2.Comer 3. Terminar turno "))
            if opcion == 1:
                while len(jugada) < 14:
                    time.sleep(.4)
                    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
                    self.mostrar_mano(self.mano)
                    self.mostrar_jugadas(jugada)
                    print()
                    indice = input("Ingrese el indice de la ficha que desea agregar (Para salir presione q): ")
                    if indice.lower() == "q":
                        self.mano.extend(jugada)
                        jugada.clear()
                        break
                    indice = int(indice)
                    if indice < 0 or indice > 14:
                        print("Ingrese un indice valido")
                        continue
                    else:
                        ficha = self.mano.pop(indice-1)
                        jugada.append(ficha)
                        if len(jugada) >= 3:
                            sel = int(input("Desea agregar otra ficha a su jugada? 1.Si 2.No"))
                            if sel == 1:
                                continue
                            elif sel == 2:
                                if self.validar(jugada):
                                    self.mostrar_jugadas(self.jugadas)
                                    break
                                else:
                                    time.sleep(.4)
                                    continue
                        else:
                            continue
            elif opcion == 2:
                self.comer(pozo)
                break
            elif opcion == 3:
                if len(jugada) >= 3 or len(self.jugadas) >= 3:
                    break
                else:
                    print("Para terminar el turno debes de haber realizado una jugada antes")
        return int(input("Desea seguir? 1.Si 2.No "))
        
    def validar(self, jugada):
        suma = 0
        comodin = False
        cont_comodin = 0
        for ficha in jugada:
            if ficha.color == "comodin":
                comodin = True
                cont_comodin += 1
            else:
                suma += ficha.numero

        if len(self.jugadas) < 3:
            if suma < 25:
                if cont_comodin == 1 and suma > 16:
                    if self.validar_tercia(jugada) or self.validar_escalera(jugada):
                        self.jugadas.extend(jugada)
                        jugada.clear()  
                        return True
                    else:
                        print("Jugada invalida, regresando las fichas")
                        self.mano.extend(jugada)
                        jugada.clear()  
                        return False
                elif cont_comodin == 2 and suma > 9:
                    if self.validar_tercia(jugada) or self.validar_escalera(jugada):
                        self.jugadas.extend(jugada)
                        jugada.clear()  
                        return True
                    else:
                        print("Jugada invalida, regresando las fichas")
                        self.mano.extend(jugada)
                        jugada.clear()  
                        return False
                    
                print("Tu primera jugada tiene que sumar un valor de 25 puntos")
                self.mano.extend(jugada)
                jugada.clear()  
                return False
            else:
                if self.validar_tercia(jugada) or self.validar_escalera(jugada):
                    self.jugadas.extend(jugada)
                    jugada.clear()  
                    return True
                else:
                    print("Jugada invalida, regresando las fichas")
                    self.mano.extend(jugada)
                    jugada.clear()  
                    return False
        else:
            if self.validar_tercia(jugada) or self.validar_escalera(jugada):
                self.jugadas.extend(jugada)
                jugada.clear()  
                return True
            else:
                print("Jugada invalida, regresando las fichas")
                self.mano.extend(jugada)
                jugada.clear()  
                return False


    def validar_tercia(self, jugada):
        for i in range(len(jugada)-1):
            ficha = jugada[i]
            if ficha.numero != jugada[i+1].numero or ficha.color == jugada[i+1].color:
                return False
            else:
                continue
        return True
        
    def validar_escalera(self, jugada):
        for i in range(len(jugada)-1):
            ficha = jugada[i]
            if ficha.numero == jugada[i+1].numero or ficha.color != jugada[i+1].color:
                return False
            else:
                continue
        return True

def crear_fichas():
    print("Creando las fichas...")
    #creando un diccionario con los colores para asignarlos
    colores = {
        "amarillo": fichas.amarillo,
        "azul": fichas.azul,
        "rojo": fichas.rojo,
        "verde": fichas.verde,
        "comodin": fichas.comodin,
    }
    #creando las fichas y asignandolas en su arreglo
    for color, arreglo in colores.items():
        if color == "comodin":
            for x in range(2):
                ficha = fichas(0, color)
                arreglo.append(ficha)
        else:
            for i in range(13):
                for j in range(2):
                    ficha = fichas(i + 1, color)
                    arreglo.append(ficha)

def mezclar_fichas(jugador):
    pozo = sum([fichas.amarillo, fichas.azul, fichas.verde, fichas.rojo, fichas.comodin], [])
    random.shuffle(pozo)
    if isinstance(jugador, player):
        mano_jugador = jugador.llenar_mano()
        for i in range(14):
            ficha = pozo.pop()
            mano_jugador.append(ficha)
    return pozo




crear_fichas()
jugador = player("andres")
pozo = mezclar_fichas(jugador)
while True:
    seguir = jugador.armar_jugada(pozo)
    if seguir == 1:
        continue
    elif seguir == 2:
        break
    

