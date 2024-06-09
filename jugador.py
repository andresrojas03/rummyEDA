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

    def mostrar_jugadas(self, jugadas):
        if len(jugadas) == 0:
            print("[]")
        else:
            print("Tus jugadas: ")
            for jugada in jugadas:
                for ficha in jugada:
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
                print()

    def haciendo_jugada(self, jugada):
        if len(jugada) == 0:
            print('[]')
        else:
            for ficha in jugada:
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
        if len(pozo) == 0:
            print("No hay mas fichas en el pozo")
            return
        comer = pozo.pop()

        print(f"Tomaste la ficha {comer.numero} de color {comer.color}")
        self.mano.append(comer)
        
        return 


    def armar_jugada(self, pozo):
        cont_jugadas = len(self.jugadas)
        jugadas = []
        jugada = []
        self.ordenar_mano()
        self.mostrar_mano(self.mano)
        while True:
            print()
            opcion = int(input("Que desea hacer? 1.Armar jugada 2.Comer  3. Agregar a jugada 4. Terminar turno "))
            if opcion == 1:
                while len(jugada) < 14:
                    time.sleep(.4)
                    os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
                    self.mostrar_mano(self.mano)
                    self.haciendo_jugada(jugada)
                    print()
                    indice = input("Ingrese el indice de la ficha que desea agregar (Para salir presione q): ")
                    if indice.lower() == "q":
                        self.mano.extend(jugada)
                        jugada.clear()
                        break
                    indice = int(indice)
                    if indice < 0 or indice > len(self.mano):
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
                                nueva_jugada = int(input("Desea realizar otra jugada? 1.Si 2.No"))
                                if nueva_jugada == 1:
                                    jugadas.append(list(jugada))
                                    jugada.clear()
                                    continue
                                elif nueva_jugada == 2:
                                    jugadas.append(list(jugada))
                                    jugada.clear()
                                    if self.validar(jugadas):
                                        self.mostrar_jugadas(self.jugadas)
                                        jugadas.clear()
                                        break
                                    else:
                                        print('Hubo una jugada invalida')
                                        jugada.clear()
                                        jugadas.clear()
                                        continue
                                else:
                                    time.sleep(.4)
                                    continue
                        else:
                            continue
            elif opcion == 2:
                if cont_jugadas != len(self.jugadas):
                    print('No puedes comer si realizaste al menos una jugada valida')
                    continue
                else:
                    self.comer(pozo)
                    break

            elif opcion == 4:
                if cont_jugadas != len(self.jugadas):
                    break
                else:
                    print("Para terminar el turno debes de haber realizado una jugada antes")
        
    def validar(self, jugadas):
        suma_jugadas = 0
        cont_comodines = 0
        cont_jugadas = len(self.jugadas)
        for jugada in jugadas:
            for ficha in jugada:
                if ficha.numero == 0 or ficha.color == 'comodin':
                    cont_comodines += 1
                    pass
                suma_jugadas += ficha.numero
        
        if not self.jugadas:
            if suma_jugadas >= 25:
                print('jugada(s) de 25 o mas puntos')
                for jugada in jugadas:
                    if self.validar_tercia(jugada):
                        self.jugadas.append(jugada)
                        pass
                    else:
                        if self.validar_escalera(jugada):
                            self.jugadas.append(jugada)
                            pass
                        else:
                            self.mano.extend(jugada)
                            pass
            elif suma_jugadas > 16 and cont_comodines == 1:
                for jugada in jugadas:
                    if self.validar_tercia(jugada):
                        self.jugadas.append(jugada)
                        pass
                    else:
                        if self.validar_escalera(jugada):
                            self.jugadas.append(jugada)
                            pass
                        else:
                            self.mano.extend(jugada)
                            return False
            elif suma_jugadas > 9 and cont_comodines == 2:
                for jugada in jugadas:
                    if self.validar_tercia(jugada):
                        self.jugadas.append(jugada)
                        return True
                    else:
                        if self.validar_escalera(jugada):
                            self.jugadas.append(jugada)
                            return True
                        else:
                            self.mano.extend(jugada)
                            return False
        else:
            for jugada in jugadas:
                    if self.validar_tercia(jugada):
                        self.jugadas.append(jugada)
                        pass
                    else:
                        if self.validar_escalera(jugada):
                            self.jugadas.append(jugada)
                            pass
                        else:
                            self.mano.extend(jugada)
                            pass
        if len(self.jugadas) == cont_jugadas:
            return False
        else:
            return True

    def validar_tercia(self, jugada):
        print('validando tercia')
        for i in range(len(jugada)-1):
            ficha = jugada[i]
            if ficha.numero == 0 or ficha.color == 'comodin':
                pass
            if ficha.numero == jugada[0].numero and ficha.color != jugada[i-1].color:
                continue
            else:
                return False
        return True
        
    def validar_escalera(self, jugada):
        comodin = False
        print('validando escalera')
        for i, ficha in enumerate(jugada):            
            if i == 0:
                continue
            if ficha.numero == 0 or ficha.color == 'comodin':
                comodin = True
                pass
            if abs(ficha.numero - jugada[i-1].numero) > 1 and not comodin:
                return False
            
            if abs(ficha.numero - jugada[i-1].numero) == 1 and ficha.color == jugada[0].color:
                continue
            else:
                return False
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
    

