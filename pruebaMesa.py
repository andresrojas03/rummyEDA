import random

COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_WHITE = '\033[97m'
COLOR_RESET = '\033[0m'
fichas_jugador = 14
nJugadores = 2


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

    
class jugador():
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.jugadas = []

    def llenar_mano(self):
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

    def mostrar_jugadas(self, fichas):
        #para mostrar las jugadas que tiene el jugador 
        #usar esta funcion en la clase mesa para mostrar las jugadas de todos los players
        print("Tu(s) jugadas:")
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
        print(f"Has agarrado la ficha {ficha[-1].numero} de color {ficha[-1].color}")
        print(f"Quedan: {len(ficha)} fichas en el pozo")
        self.mano.append(ficha.pop())
    
    def armar_jugada(self, pozo): 
        jugada = []
        print("Tu mano:")
        self.mostrar_mano(self.mano)
        print()
        nueva_jugada = 3
        while len(jugada)< 14:
            turno = int(input("Que desea hacer? 1.Hacer jugada 2.Comer 3. Terminar turno "))
            if turno == 1:
                print(f"Tamanio de la jugada: {len(jugada)}")
                print(f"Tamanio de la nueva jugada: {nueva_jugada}")
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
                            break
                nueva_jugada = nueva_jugada + 3 
                
            elif turno == 2:
                self.comer(pozo)
                return
            elif turno == 3:
                self.validar_jugada(jugada)
                return 
        
    def validar_jugada(self, jugada):
        suma = 0
        valida = True
        for i in range(len(jugada)):
            #determinar el valor del comodin
            if jugada[i].numero == "*":
                if jugada[i+1].numero == 13:
                    suma += (jugada[i+1].numero)
                else:
                    suma += (jugada[i+1].numero + 1)
            else:
                suma += jugada[i].numero


        print(suma)
        # if suma < 25:
        #     print("Jugada invalida, necesitas 25 puntos para poder jugar")
        #     valida = False
        # else:
        #     print(f"Jugada de {suma} puntos")

        # if not valida:
        #     reg = jugada.pop()
        #     self.mano.append(reg)
        #     return False
        # else:
        #     return True


    def ganar(self):
        if len(self.mano) != 0:
            return False
        elif len(self.mano) == 0:
            print("El jugador ha ganado")
            return True     
     
class mesa():
    def __init__(self, jugadores):
        self.jugadores = jugadores#un arreglo con los jugadores en la mesa
        # self.jugadas = jugadas #arreglo con las jugadas de cada jugador
    def mostrar_jugadores(self):
        print("Jugadores activos en la mesa:")
        for jugador in self.jugadores:
            print(f"{jugador.nombre} ", end='')
        print()

    def turnos(self, orden):
        print(f"inicia el jugador {self.jugadores[orden-1].nombre}")
        if orden == 1: #inicia el jugador de consola
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
                ficha = fichas("*", color)
                arreglo.append(ficha)
        else:
            for i in range(13):
                for j in range(2):
                    ficha = fichas(i + 1, color)
                    arreglo.append(ficha)

def crear_jugadores(num_jugadores):
    nombre_jugador = [f"Jugador{i+1}" for i in range(num_jugadores)]
    jugadores = [jugador(nombre) for nombre in nombre_jugador]
    return jugadores

def mezclar_fichas(n,jugadores):
    pozo = sum([fichas.amarillo, fichas.azul, fichas.rojo, fichas.verde, fichas.comodin], []) #este es el pozo de las fichas
    random.shuffle(pozo)
    
    #para llenar el arreglo del jugador con sus fichas
    for j in range(n):
        mano_jugador = jugadores[j].llenar_mano() #llamando el arreglo del jugador
        for i in range(fichas_jugador):
            ficha = pozo.pop()
            mano_jugador.append(ficha) #llenando la mano del jugador


    return pozo
       
def main():
    crear_fichas()
    
    jugadores = crear_jugadores(nJugadores)
    
    # Llenar el deck con la función mezclar_fichas()
    pozo = mezclar_fichas(nJugadores, jugadores)
    
    orden = random.randint(1, nJugadores)

    table= mesa(jugadores)
    inicio = table.turnos(orden)
    

    print(f"En el pozo hay: {len(pozo)} fichas")
    #mostrar el contenido hasta que el jugador gane
    while not jugadores[0].ganar():
        table.mostrar_jugadores()
        
        #pruebas con el jugador 1
        play = jugadores[0].armar_jugada(pozo)
        print(f"Ha terminado el turno del {jugadores[0].nombre}")
        exit(-1)
        
    
    


if __name__ == "__main__": 
    main()
