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
        
        # Ordenar las fichas numéricas en función de su número y color
        numeros.sort(key=lambda x: (x.color, x.numero))
        
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
        size_jugadas= len(self.jugadas)
        jugada = []
        print("Tu mano: ")
        self.mostrar_mano(self.mano)
        print()
        self.mostrar_jugadas(self.jugadas)
        while True:
            sel = int(input("Que deseas hacer? 1.Armar jugada 2.Comer 3.Agregar a jugada "))
            if sel == 1:
                while len(self.jugadas) < 14:
                    self.mostrar_mano(self.mano)
                    cond = int(input("Agregar ficha? 1.Si 2.No  "))
                    if cond == 1:
                        indice = int(input("Seleccione el indice de su ficha: "))-1
                        ficha= self.mano.pop(indice)
                        jugada.append(ficha)
                    elif cond == 2: 
                        break
                    else:
                        break
                print(f"size de tus jugadas{len(jugada)}")
                
                if self.validar_jugada(jugada):
                    while jugada:
                        agregar = jugada.pop()
                        self.jugadas.append(agregar)
                    break
                else:
                    while jugada:
                        reg = jugada.pop()
                        self.mano.append(reg)
                        continue
            if sel == 2:
                self.comer(pozo)
                break
            if sel == 3:
                ind = int(input("Seleccione el indice de la ficha que quiere agregar: "))-1
                ficha_seleccionada = self.mano.pop(ind)
                if self.agregar_ficha(ficha_seleccionada, jugadores):
                    break
                else:
                    continue
     #verificar si es valida la jugada       
    def agregar_ficha(self, ficha_seleccionada, jugadores):
        suma_jugada = 0
        for _, jugador in enumerate(jugadores):
            for ficha in jugador.jugadas:
                suma_jugada += ficha.numero
        if suma_jugada == 0:
            print("No se puede agregar una ficha a jugadas vacias")
            return 
        for i, jugador in enumerate(jugadores):
            print(f"{i + 1} Jugador {jugador.nombre}")
        sel = int(input("Ingrese el índice del jugador al que quiere agregar una ficha: "))
        if sel >= 1 and sel <= len(jugadores): 
            jugadores[sel - 1].jugadas.append(ficha_seleccionada)
        else:
            print("Índice inválido. Inténtelo de nuevo.")

    def validar_jugada(self, jugada):
        for ficha in jugada:
            print(f"ficha numero {ficha.numero} de color {ficha.color}")
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
        #revisar esto jasjaj
        # Verificar si la jugada es una corrida o una tercia/cuarta
        for i, ficha in enumerate(jugada):
            if i < len(jugada) - 1:
                siguiente = jugada[i+1]
                if ficha.numero == '*' or siguiente.numero == '*':
                    self.jugadas.append(ficha)
                    continue
                #pao revisa esto
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
      
    # def ordenar_jugada(self, jugada):
    #     for i in range(len(jugada) - 1):
    #         if jugada[i].numero == "*":
    #             jugada[0] = jugada[i]
    #         elif jugada[i+1].numero == "*":
    #             jugada[i+1], jugada[i] = jugada[i], jugada[i+1]
    #         elif jugada[i].numero > jugada[i+1].numero:
    #             jugada[i+1], jugada[i] = jugada[i], jugada[i+1]


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
        
        # Ordenar las fichas numéricas en función de su número y color
        numeros.sort(key=lambda x: (x.color, x.numero))
        
        # Combinar los comodines y las fichas numéricas ordenadas
        self.mano = comodines + numeros

    def armar_jugada(self, pozo, jugadores):
        jugadas_en_mesa = []
        for jugador in jugadores:
            jugadas_en_mesa.extend(jugador.jugadas)

        if self.jugada_tercia():
            if self.jugada_escalera():
                if self.es_jugada_valida(self.contar_comodines()):
                    return True
                else:
                    self.comer(pozo)
                    return False
            elif self.es_jugada_valida(self.contar_comodines()):
                return True
            else:
                self.comer(pozo)
                return False
        elif self.jugada_escalera():
            if self.es_jugada_valida(self.contar_comodines()):
                return True
            else:
                self.comer(pozo)
                return False
        elif self.agregar_ficha(jugadores):
            return True
        else:
            self.comer(pozo) 


    def agregar_ficha(self, jugadores):
        print(f"{self.nombre} intentando agregar una ficha a las jugadas en la mesa")
        for jugador in jugadores:
            for ficha in self.mano:
                if self.validar_ficha(ficha, jugador.jugadas):
                    jugador.jugadas.append(ficha)
                    self.mano.remove(ficha)
                    print(f"{self.nombre} agregó una ficha a las jugadas de {jugador.nombre}")
                    return True
        print("No se pudo agregar ninguna ficha a las jugadas de los otros jugadores")
        return False
    #verificar logica de validar
    def validar_ficha(self, ficha, jugada):
        jugadas_tercia = []
        jugadas_escalera = []
        #separar las jugadas por escaleras y tercias/cuartas
        for i in range(len(jugada) - 1):
            pieza = jugada[i]
            siguiente_pieza = jugada[i + 1]
            if pieza.numero == siguiente_pieza.numero and pieza.color != siguiente_pieza.color:
                jugadas_tercia.append(pieza)
            elif pieza.numero != siguiente_pieza.numero + 1 and pieza.color == siguiente_pieza.color:
                jugadas_escalera.append(pieza)
        #comprobar si se puede agregar en tercias/cuartas
        for i in range(len(jugadas_tercia)):
            pieza = jugadas_tercia[i]
            if ficha.numero == pieza.numero and ficha.color != pieza.color:
                return True
            else:
                break
        #comprobar si se puede agregar en escaleras
        for i in range(len(jugadas_escalera)):
            pieza = jugadas_escalera[i]
            #verificar condicion
            if ficha.numero == pieza.numero + 1 and ficha.color == pieza.color:
                return True
            else:
                break
        return False


    def es_jugada_valida(self, num_comodines):
        amarillo = []
        azul = []
        rojo = []
        verde = []

        # Separar las jugadas por color
        for i, ficha in enumerate(self.jugadas):
            if ficha.color == "amarillo":
                amarillo.append(ficha)
            elif ficha.color == "azul":
                azul.append(ficha)
            elif ficha.color == "verde":
                verde.append(ficha)
            elif ficha.color == "rojo":
                rojo.append(ficha)

        # Calcular sumas de cada color
        suma_amarillo = sum(ficha.numero for ficha in amarillo)
        suma_azul = sum(ficha.numero for ficha in azul)
        suma_verde = sum(ficha.numero for ficha in verde)
        suma_rojo = sum(ficha.numero for ficha in rojo)

        # Verificar si alguna suma de color es mayor o igual a 25, o si la suma total es mayor o igual a 25
        if suma_amarillo >= 25 or suma_azul >= 25 or suma_verde >= 25 or suma_rojo >= 25:
            return True
        elif suma_amarillo >= 12 and num_comodines == 1 or suma_azul >= 12 and num_comodines == 1 or suma_verde >= 12 and num_comodines == 1 or suma_rojo >= 12 and num_comodines == 1:
            return True
        elif suma_amarillo >= 9 and num_comodines == 2 or suma_azul >= 9 and num_comodines == 2 or suma_verde >= 9 and num_comodines == 2 or suma_rojo >= 9 and num_comodines == 2:
            return True
        else:
            sum_total = suma_amarillo + suma_azul + suma_rojo + suma_verde
            if sum_total >= 25:
                return True
            elif sum_total >= 12 and num_comodines == 1:
                return True
            elif sum_total >= 9 and num_comodines == 2:
                return True
            else:
                while self.jugadas:
                    reg = self.jugadas.pop()
                    self.mano.append(reg)
  
    def contar_comodines(self):
        cont_comodin = 0
        for ficha in self.mano:
            if ficha.numero == "*":
                cont_comodin += 1
                continue
        return cont_comodin

    def jugada_tercia(self):
        print(f"{self.nombre} intentando hacer una jugada tercia")
        numeros = [f for f in self.mano if f.numero != "*"]
        comodines = [f for f in self.mano if f.numero == "*"]
        jugada = []
        #ordena el arreglo numeros en orden ascendente
        numeros.sort(key=lambda x: x.numero)

        for i in range(len(numeros) - 2):  
            if numeros[i].numero == numeros[i+1].numero == numeros[i+2].numero \
                    and numeros[i].color != numeros[i+1].color != numeros[i+2].color:
                jugada = [numeros[i], numeros[i+1], numeros[i+2]]  # Agregar la tercia
                if len(jugada) >= 3:
                    jugada.extend(comodines[:3 - len(jugada)])  # Agregar comodines si es necesario
                    self.jugadas.extend(jugada) 
                    for ficha in jugada:
                        self.mano.remove(ficha) 
                    return True
        print("No se pudo formar una tercia")
        return False

    #verificar lo de los comodines
    def jugada_escalera(self):
            print(f"{self.nombre} intentando hacer una jugada escalera")
            numeros = [f for f in self.mano if f.numero != "*"]
            jugada = []
            numeros.sort(key=lambda x: x.numero)
            for i in range(len(numeros) - 2):
                jugada = [numeros[i]]
                for j in range(i + 1, len(numeros)):
                    if numeros[j].numero == "*":
                        if self.contar_comodines() > 0 and numeros[j].color == jugada[-1].color:
                            jugada.append(self.usar_comodin())  # Usar un comodín si es posible
                        else:
                            break
                    # Si la próxima ficha no es un comodín, verificar si forma parte de la escalera
                    elif numeros[j].numero - jugada[-1].numero == 1 and numeros[j].color == jugada[-1].color:
                        jugada.append(numeros[j])
                    else:
                        break
                if len(jugada) >= 3:
                    self.jugadas.extend(jugada)
                    for ficha in jugada:
                        self.mano.remove(ficha)
                    return True

            print("No se pudo formar una escalera")
            return False

    def usar_comodin(self):
        comodines = [ficha for ficha in self.mano if ficha.numero == "*"]
        if comodines:
            comodin = comodines[0]  # Tomar el primer comodín disponible
            self.mano.remove(comodin)  # Quitar el comodín de la mano
            return comodin
        else:
            return None  # Retorna None si no hay comodines disponibles

    def comer(self, pozo):
        if len(pozo) == 0:
            print("No quedan mas fichas en el pozo")
            return
        print(f"El jugador {self.nombre} ha comido\n")
        print(f"Quedan: {len(pozo)-1} fichas en el pozo")
        ficha_comida = pozo.pop()
        self.mano.append(ficha_comida)
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

    def ordenar_manos(self):
        for jugador in self.jugadores:
            comodines = [ficha for ficha in jugador.mano if ficha.numero == "*"]
            numeros = [ficha for ficha in jugador.mano if ficha.numero != "*"]
            
            # Ordenar las fichas numéricas en función de su número y color
            numeros.sort(key=lambda x: (x.color, x.numero))
            
            # Combinar los comodines y las fichas numéricas ordenadas
            jugador.mano = comodines + numeros

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
                print(f"Mano de {jugador.nombre} tiene {len(jugador.mano)} fichas")
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
    table = mesa(jugadores)
    rondas = 0

    while len(jugadores) > 1:
        rondas += 1
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar la pantalla
        print(f"****#### RONDA {rondas} ####****")
        table.mostrar_jugadores()
        if rondas == 1:
            table.turnos(orden)
        table.ordenar_manos()
        table.mostrar_manos()
        for jugador in table.jugadores:
            time.sleep(0.7)
            if isinstance(jugador, player):
                print("\nTu turno")
                table.mostrar_jugadas()
                jugador.armar_jugada(pozo, rondas, table.jugadores)
            else:
                jugador.ordenar_mano()
                jugador.armar_jugada(pozo, table.jugadores) 

            if jugador.ganar():
                if isinstance(jugador, player):
                    print(f"Ha salido el jugador {jugador.nombre}")
                else:
                    print(f"Ha salido el bot {jugador.nombre}")
                jugadores.remove(jugador)


if __name__ == "__main__": 
    main()
