import random
import time
import os

COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_WHITE = '\033[97m'
COLOR_RESET = '\033[0m'
fichas_jugador = 14
nJugadores = 4


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

class player():
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.jugadas = []

    def llenar_mano(self):
        return self.mano
    
    def ordenar_mano(self):
        comodines = [ficha for ficha in self.mano if ficha.numero == "*"]
        numeros = [ficha for ficha in self.mano if ficha.numero != "*"]
        
        # Ordenar las fichas numéricas en función de su número
        for i in range(len(numeros)):
            for j in range(len(numeros) - 1):
                if numeros[j].numero > numeros[j + 1].numero:
                    numeros[j], numeros[j + 1] = numeros[j + 1], numeros[j]
        
        # Combinar los comodines y las fichas numéricas ordenadas
        self.mano = comodines + numeros

    def mostrar_mano(self, fichas):
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
            print('[' + color + f"{ficha.numero}" + COLOR_RESET + ']', end='')

    def mostrar_jugadas(self, fichas):
        #para mostrar las jugadas que tiene el jugador 
        print("Tu(s) jugadas:")
        if len(fichas) == 0:
            print("[]")
        else:
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

                print('[' + color + f"{ficha.numero}" + COLOR_RESET + ']', end='')
            print()
        
    def comer(self, ficha):
        if len(ficha) == 0:
            print("No quedan mas fichas en el pozo")
            return
        
        print(f"Has agarrado la ficha {ficha[-1].numero} de color {ficha[-1].color}")
        print(f"Quedan: {len(ficha)-1} fichas en el pozo")
        self.mano.append(ficha.pop())
        time.sleep(1)
    
    def armar_jugada(self, pozo, ronda, jugadores): 
        self.ordenar_mano()
        jugada = []
        if ronda == 1:
            print("Tu mano:")
            nueva_jugada = 3
        else:
            self.mostrar_jugadas(self.jugadas)
            nueva_jugada = 3
        while len(jugada) < 14:
            self.mostrar_mano(self.mano)
            print()
            turno = int(input("Que desea hacer? 1.Hacer jugada 2.Comer 3.Jugar en la mesa 4. Terminar turno "))
            if turno == 1:    
                while len(jugada) < nueva_jugada or len(jugada) < (nueva_jugada+1):
                    while True:
                        try:
                            indice = int(input("Ingrese el índice de la ficha: ")) - 1  # Restar 1 para ajustar al índice base 0
                            if 0 <= indice < len(self.mano):
                                break
                            else:
                                print("Índice fuera de rango. Inténtelo de nuevo.")
                        except ValueError:
                            print("Entrada no válida. Inténtelo de nuevo.")
                    ficha_seleccionada = self.mano.pop(indice)
                    jugada.append(ficha_seleccionada)
                    self.mostrar_jugadas(jugada)
                    self.mostrar_mano(self.mano)
                    print()
                    if(len(jugada) == 3):
                        termino = int(input(("Agregar otra ficha? 1.Si 2.No")))
                        if termino == 1:
                            pass
                        elif termino == 2:
                            self.ordenar_jugada(jugada)
                            break
                nueva_jugada = nueva_jugada + 3 
                
                self.ordenar_jugada(jugada)
                if self.validar_jugada(jugada):
                    break
                else:
                    jugada.clear()
            elif turno == 2:
                self.comer(pozo)
                return
            elif turno == 3:
                ficha_jugada = int(input("Ingrese el indice de la ficha que quiera agrear a otra jugada: "))
                ficha_seleccionada = self.mano.pop(ficha_jugada-1)
                self.agregar_ficha(ficha_seleccionada, jugadores)
                return
            elif turno == 4:
                return
            
    def agregar_ficha(self, ficha_seleccionada, jugadores):
        for i, jugador in enumerate(jugadores):
            if isinstance(jugador, player):
                pass
            else:
                print(f"{i + 1} Jugador {jugador.nombre}")
        sel = int(input("Ingrese el índice del jugador al que quiere agregar una ficha: "))
        if sel >= 1 and sel <= len(jugadores): 
            jugadores[sel - 1].jugadas.append(ficha_seleccionada)
        else:
            print("Índice inválido. Inténtelo de nuevo.")

    def validar_jugada(self, jugada):
        suma = 0
        comodin_presente = False  # Variable para rastrear si hay comodines en la jugada
        conteo_comodin = 0
        # Calcular la suma de los números de las fichas, excluyendo los comodines
        for ficha in jugada:
            if ficha.numero == "*":
                comodin_presente = True
                conteo_comodin += 1
                continue
            suma += ficha.numero

        # Verificar si la suma total es menor a 25
        if suma < 25:
            if comodin_presente and suma >= 12 or conteo_comodin == 2 and suma < 12:
                pass
            else:
                print("Jugada inválida, la suma total de las fichas es menor a 25")
                self.devolver_fichas(jugada)
                return False

        # Verificar si la jugada es una corrida o una tercia/cuarta
        for i, ficha in enumerate(jugada):
            if i < len(jugada) - 1:
                siguiente = jugada[i+1]
                if ficha.numero == '*' or siguiente.numero == '*':
                    self.jugadas.append(ficha)
                    continue
                if ficha.color != siguiente.color:
                    if ficha.numero != siguiente.numero:
                        print("Jugada inválida, no es una corrida")
                        self.devolver_fichas(jugada)
                        return False
                else:
                    if ficha.numero == siguiente.numero:
                        print("Jugada inválida, no es una tercia/cuarta")
                        self.devolver_fichas(jugada)
                        return False
            self.jugadas.append(ficha)
        return True
   
    def devolver_fichas(self, jugada):
        while len(jugada) != 0:
            reg = jugada.pop()
            self.mano.append(reg)    
        
    def ordenar_jugada(self, jugada):
        for i in range(len(jugada) - 1):
            if jugada[i].numero == "*":
                jugada[0] = jugada[i]
            elif jugada[i+1].numero == "*":
                jugada[i+1], jugada[i] = jugada[i], jugada[i+1]
            elif jugada[i].numero > jugada[i+1].numero:
                jugada[i+1], jugada[i] = jugada[i], jugada[i+1]


    def ganar(self):
        if len(self.mano) != 0:
            return False
        elif len(self.mano) == 0:
            print("El jugador ha ganado")
            return True     

class bot():
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.jugada_numero = []
        self.jugada_escaleras = [] #salia error :c
        self.comodin = []
        self.jugadas = []

    def llenarManoBot(self):
        return self.mano
    
    def mostrar_mano(self, fichas):
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
            print('[' + color + f"{ficha.numero}" + COLOR_RESET + ']', end='')
        print()

    def ordenar_mano(self):
        comodines = [ficha for ficha in self.mano if ficha.numero == "*"]
        numeros = [ficha for ficha in self.mano if ficha.numero != "*"]
        
        # Ordenar las fichas numéricas en función de su número
        for i in range(len(numeros)):
            for j in range(len(numeros) - 1):
                if numeros[j].numero > numeros[j + 1].numero:
                    numeros[j], numeros[j + 1] = numeros[j + 1], numeros[j]
        
        # Combinar los comodines y las fichas numéricas ordenadas
        self.mano = comodines + numeros

    def jugada_tercia(self):
        numeros = []
        comodines = []
        jugada = []
        suma = 0
        
        # Iterar sobre la lista de fichas y separar los comodines
        for ficha in self.mano:
            if ficha.numero == "*":
                comodines.append(ficha)
            else:
                numeros.append(ficha)
        
        # Iterar sobre los números para buscar tercias
        for i in range(len(numeros) - 2):  # -2 para evitar el índice fuera de rango
            if len(jugada) < 4:
                if numeros[i].numero == numeros[i+1].numero == numeros[i+2].numero and \
                numeros[i].color != numeros[i+1].color and \
                numeros[i].color != numeros[i+2].color and \
                numeros[i+1].color != numeros[i+2].color:
                    jugada.extend(numeros[i:i+3])  # Agregar la tercia a la jugada
        
        # Calcular la suma de los números en la jugada
        for ficha in jugada:
            suma += ficha.numero
        # Verificar condiciones para agregar las fichas a self.jugadas
        if suma > 25:
            self.jugadas.extend(jugada)     # Agregar las fichas de la tercia
            for ficha in jugada:
                self.mano.remove(ficha)
            return True
        elif len(comodines) == 1 and suma > 12:
            self.jugadas.extend(jugada)     # Agregar las fichas de la tercia
            self.jugadas.append(comodines[0])  # Agregar el comodín restante
            for ficha in jugada:
                self.mano.remove(ficha)
            for ficha in comodines:
                self.mano.remove(ficha)
            return True
        elif len(comodines) == 2 and suma > 9:
            self.jugadas.extend(comodines)  # Agregar ambos comodines
            self.jugadas.extend(jugada)     # Agregar las fichas de la tercia
            for ficha in jugada:
                self.mano.remove(ficha)
            for ficha in comodines:
                self.mano.remove(ficha)
            return True
        
        return False  # No se pudo formar una tercia válida

    def jugada_escalera(self):
        numeros = []
        comodines = []
        jugada = []
        suma = 0
        
        # Iterar sobre la lista de fichas y separar los comodines
        for ficha in self.mano:
            if ficha.numero == "*":
                comodines.append(ficha)
            else:
                numeros.append(ficha)
        # Iterar sobre los números para buscar escaleras
        for i in range(len(numeros) - 2):  # -2 para evitar el índice fuera de rango
            if len(jugada) < 14:
                if (numeros[i].numero + 1 == numeros[i+1].numero) and (numeros[i+1].numero + 1 == numeros[i+2].numero) \
                    and (numeros[i].color == numeros[i+1].color == numeros[i+2].color):
                    jugada.extend(numeros[i:i+3])  # Agregar la escalera a la jugada

        
        # Calcular la suma de los números en la jugada
        for ficha in jugada:
            suma += ficha.numero

        # Verificar condiciones para agregar las fichas a self.jugadas
        if suma > 25:
            self.jugadas.extend(jugada)     # Agregar las fichas de la escalera
            for ficha in jugada:
                self.mano.remove(ficha)
            return True
        elif len(comodines) == 1 and suma > 12:
            self.jugadas.extend(jugada) 
            self.jugadas.append(comodines[0])  # Agregar el comodín restante
            for ficha in jugada:
                self.mano.remove(ficha)
            for ficha in comodines:
                self.mano.remove(ficha)
            return True
        elif len(comodines) == 2 and suma > 9:
            self.jugadas.extend(comodines)  # Agregar ambos comodines
            self.jugadas.extend(jugada)     
            for ficha in jugada:
                self.mano.remove(ficha)
            for ficha in comodines:
                self.mano.remove(ficha)
            return True
        
        return False  # No se pudo formar una escalera válida
    
    def comer(self, pozo):
        if len(pozo) == 0:
            print("No quedan mas fichas en el pozo")
            return
        print(f"El jugador {self.nombre} ha comido\n")
        print(f"Quedan: {len(pozo)-1} fichas en el pozo")
        self.mano.append(pozo.pop())
        time.sleep(1)


    def mostrar_jugadas(self):

        print(f"\nJugadas de {self.nombre}")
        if len(self.jugadas) == 0:
            print("[]")
        else:
            for ficha in self.jugadas:
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

                print('[' + color + f"{ficha.numero}" + COLOR_RESET + ']', end='')
            print()    

    def ganar(self):
        if len(self.mano) != 0:
            return False
        else:
            return True

class mesa():
    def __init__(self, jugadores):
        self.jugadores = jugadores#un arreglo con los jugadores en la mesa
        self.turno_actual = 0

    def ordenar_jugadas(self):
        for jugador in self.jugadores:
            comodines = [ficha for ficha in jugador.jugadas if ficha.numero == "*"]
            numeros = [ficha for ficha in jugador.jugadas if ficha.numero != "*"]
            
            # Ordenar las fichas numéricas en función de su número
            for i in range(len(numeros)):
                for j in range(len(numeros) - 1):
                    if numeros[j].numero > numeros[j + 1].numero:
                        numeros[j], numeros[j + 1] = numeros[j + 1], numeros[j]
            
            # Combinar los comodines y las fichas numéricas ordenadas
            jugador.jugadas = comodines + numeros

    def mostrar_jugadores(self):
        print("Jugadores activos en la mesa:")
        for jugador in self.jugadores:
            print(f"**** {jugador.nombre} ", end='')
        print("****")

    def mostrar_jugadas(self):
        #para mostrar las jugadas que tiene el jugador 
        for jugador in self.jugadores:
           if isinstance(jugador, player):
               pass
           else:
               jugador.mostrar_jugadas()
    def mostrar_manos(self):
        for jugador in self.jugadores:
            if isinstance(jugador, player):
                pass
            else:
                print(f"Mano de {jugador.nombre}")
                jugador.mostrar_mano(jugador.mano)
                print()

    def turnos(self, orden):
        # Reordenar los jugadores para que el primero sea el que tenga el índice 'orden'
        self.jugadores = self.jugadores[orden-1:] + self.jugadores[:orden-1]
        self.turno_actual = 0  # Reseteamos el turno actual al principio del arreglo
        print(f"Inicia el jugador {self.jugadores[self.turno_actual].nombre}")
        return self.jugadores[self.turno_actual]
    
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
                ficha = fichas("*", color)
                arreglo.append(ficha)
        else:
            for i in range(13):
                for j in range(2):
                    ficha = fichas(i + 1, color)
                    arreglo.append(ficha)

def crear_jugadores(Bot, Jugador, incluir_bot=False):
    if incluir_bot:  # Si se incluye un jugador humano
        num_jugadores = 3  # Hay tres bots
        nombre_jugadores = [f"Bot{i+1}" for i in range(num_jugadores)]
        jugadores = [Bot(nombre) for nombre in nombre_jugadores]
        nombre_jugador = input("Ingrese su nombre: ")
        jugador = Jugador(nombre_jugador)
        jugadores.append(jugador)
    else:  # Si son todos bots
        num_jugadores = 4
        nombre_jugadores = [f"Bot{i+1}" for i in range(num_jugadores)]
        jugadores = [Bot(nombre) for nombre in nombre_jugadores]

    return jugadores

def mezclar_fichas(n,jugadores):
    pozo = sum([fichas.amarillo, fichas.azul, fichas.rojo, fichas.verde, fichas.comodin], []) #este es el pozo de las fichas
    random.shuffle(pozo)
    
    #para llenar el arreglo del jugador con sus fichas
    for j in range(n):
        if isinstance(jugadores[j], player):
            mano_jugador = jugadores[j].llenar_mano()
        else:
            mano_jugador = jugadores[j].llenarManoBot()
        for i in range(fichas_jugador):
            ficha = pozo.pop()
            mano_jugador.append(ficha)
    return pozo
       
def main():
    crear_fichas()
    jugadores = crear_jugadores(bot, player, nJugadores)
    # Llenar el deck con la función mezclar_fichas()
    pozo = mezclar_fichas(nJugadores, jugadores)
    
    orden = random.randint(1, nJugadores)
    table= mesa(jugadores)
    print(orden)
    rondas = 0
    #mostrar el contenido hasta que el jugador gane
    while len(jugadores) > 1:
        rondas += 1
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
        print(f"****#### RONDA {rondas} ####****")
        table.mostrar_jugadores()
        if rondas == 1:
            table.turnos(orden)
        table.mostrar_manos()
        for jugador in table.jugadores:
            time.sleep(0.7)
            if isinstance(jugador, player):
                print("\nTu turno")
                table.mostrar_jugadas()
                jugador.armar_jugada(pozo, rondas,table.jugadores)
            else:
                jugador.ordenar_mano()
                if not jugador.jugada_tercia():
                    if not jugador.jugada_escalera():
                        jugador.comer(pozo)
             
            if jugador.ganar():
                if isinstance(jugador, player):
                    print(f"Ha salido el jugador {jugador.nombre}")
                else:
                    print(f"Ha salido el bot {jugador.nombre}")
                jugadores.remove(jugador)


if __name__ == "__main__": 
    main()
