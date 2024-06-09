import random
import time
import os

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

class mesa():
    def __init__(self):
        self.jugadores = []
        self.turno_actual = 0
        self.modo = False

    def modalidad(self, modalidad):
            if modalidad == 1:
                self.crear_jugadores(jugador = False)
            elif modalidad == 2:
                self.crear_jugadores(jugador = True)    
    
    def crear_jugadores(self, jugador):
        if jugador:
            for i in range(3):
                self.jugadores.append(bot(f'bot{i+1}'))
            nombre = input('Ingrese su nombre ')
            self.jugadores.append(player(f'{nombre}'))
        else:
            print('Se va a jugar solamente con bots')
            for i in range(4):
                self.jugadores.append(bot(f'bot{i+1}')) 
    
    def mostrar_jugadores(self):
        for jugador in self.jugadores:
            print('[' + f'{self.jugadores[self.turno_actual].nombre}' + ']', end='')
        print()

    def mezclar_fichas(self):
        n = len(self.jugadores)
        if n == 0:
            print('No hay jugadores en la mesa')
            exit(1)
        pozo = sum([fichas.amarillo, fichas.azul, fichas.verde, fichas.rojo, fichas.comodin], [])
        random.shuffle(pozo)
        
        for i in range(n):
            if isinstance(self.jugadores[i], player):
                mano_jugador = self.jugadores[i].llenar_mano()
            else:
                mano_jugador = self.jugadores[i].llenar_mano_bot()
            for j in range(14):
                ficha = pozo.pop()
                mano_jugador.append(ficha)

        print(f'Despues de repartir fichas el pozo se quedo con {len(pozo)} fichas')
        return pozo     

    def mostrar_jugadas(self):
        
        for jugador in self.jugadores:
            print(f'Jugadas de {jugador.nombre}: ')
            if len(jugador.jugadas) == 0:
                print('[]')
            else:
                for jugada in jugador.jugadas:
                    for ficha in jugada:
                        color = COLOR_RESET
                        if ficha.color == 'amarillo':
                            color = COLOR_YELLOW
                        if ficha.color == 'azul':
                            color = COLOR_BLUE
                        if ficha.color == 'rojo':
                            color = COLOR_RED
                        if ficha.color == 'verde':
                            color = COLOR_GREEN
                        if ficha.color == 'comodin':
                            color = COLOR_WHITE
                        print('[' + color + f'{ficha.numero}' + COLOR_RESET + ']', end='')
                    print()
                print()

    def mostrar_manos(self):
        for jugador in self.jugadores:
            if len(jugador.mano) == 0:
                print('[]')
            else:
                print(f'La mano de {jugador.nombre} contiene {len(jugador.mano)} fichas')
                for ficha in jugador.mano:
                    color = COLOR_RESET
                    if ficha.color == 'amarillo':
                        color = COLOR_YELLOW
                    if ficha.color == 'azul':
                        color = COLOR_BLUE
                    if ficha.color == 'rojo':
                        color = COLOR_RED
                    if ficha.color == 'verde':
                        color = COLOR_GREEN
                    if ficha.color == 'comodin':
                        color = COLOR_WHITE
                    print('[' + color + f'{ficha.numero}' + COLOR_RESET + ']', end='')
            print()

    def turno (self, orden):
        self.jugadores = self.jugadores[orden-1:] + self.jugadores[:orden-1]
        self.turno_actual = 0
        print(f'Inicia {self.jugadores[self.turno_actual].nombre}')
        return self.jugadores[self.turno_actual]

    def sig_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        print(f"Turno de {self.jugadores[self.turno_actual].nombre}")
        return self.jugadores[self.turno_actual]
    
    def eliminar_jugador(self, indice):
        print(f"{self.jugadores[self.turno_actual].nombre} eliminado")
        self.jugadores.pop(indice)
        if self.turno_actual >= len(self.jugadores):
            self.turno_actual = 0

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
            print(f'Jugadas: ')
            cont_jugadas = 0
            for jugada in jugadas:
                cont_jugadas += 1
                print(f'Jugada {cont_jugadas}: ')
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
                    print('[' + color + f"{ficha.numero}" + COLOR_RESET + ']', end='')
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

    def ordenar_numeros(self, jugada):
        #ordenar la mano del bot usando cocktail-sort
        n = len(jugada)
        swapped = True
        start = 0
        end = n - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if self.comparar_fichas_numeros(jugada[i], jugada[i + 1]) > 0:
                    jugada[i], jugada[i + 1] = jugada[i + 1], jugada[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                if self.comparar_fichas_numeros(jugada[i], jugada[i + 1]) > 0:
                    jugada[i], jugada[i + 1] = jugada[i + 1], self.mano[i]
                    swapped = True

            start += 1

    def comparar_fichas_numeros(self, ficha1, ficha2):
        return ficha1.numero - ficha2.numero


    def armar_jugada(self, pozo, jugadores):
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
            elif opcion == 3:
                if len(self.jugadas) == 0:
                    print('No se pueden agregar fichas a otras jugadas si no has hecho una jugada')
                    continue
                else:
                    if self.agregar_a_jugada(jugadores):
                        break
                    else:
                        continue

            elif opcion == 4:
                if cont_jugadas != len(self.jugadas):
                    break
                else:
                    print("Para terminar el turno debes de haber realizado una jugada antes")

    def agregar_a_jugada(self, jugadores):
        while True:
            for i, jugador in enumerate(jugadores):
                print(f'{i+1}: {jugador.nombre}')
            
            jugador_sel = input('Ingrese el índice del jugador (presione q para cancelar): ')
            if jugador_sel.lower() == 'q':
                return False

            try:
                jugador_sel = int(jugador_sel)
                if jugador_sel < 1 or jugador_sel > len(jugadores):
                    print("Índice inválido")
                    continue
            except ValueError:
                print("Por favor ingrese un número válido")
                continue

            jugador = jugadores[jugador_sel - 1]
            if len(jugador.jugadas) == 0:
                print('El jugador no tiene jugadas')
                continue
            
            while True:
                self.mostrar_jugadas(jugador.jugadas)
                try:
                    jugada_sel = int(input('Ingrese el índice de la jugada: '))
                    if jugada_sel < 1 or jugada_sel > len(jugador.jugadas):
                        print("Índice inválido")
                        continue
                except ValueError:
                    print("Por favor ingrese un número válido")
                    continue

                self.mostrar_mano(self.mano)
                try:
                    ficha_sel = int(input('Ingrese el índice de la ficha que desea agregar a esa jugada: '))
                    if ficha_sel < 1 or ficha_sel > len(self.mano):
                        print("Índice inválido")
                        continue
                except ValueError:
                    print("Por favor ingrese un número válido")
                    continue

                ficha = self.mano.pop(ficha_sel - 1)
                jugadores[jugador_sel - 1].jugadas[jugada_sel - 1].extend([ficha])
                if self.validar_agregar_ficha(jugadores[jugador_sel - 1].jugadas[jugada_sel - 1]):
                    return True
                else:
                    jugadores[jugador_sel - 1].jugadas[jugada_sel - 1].pop()
                    self.mano.append(ficha)
                    print("La ficha no es válida en esta jugada, se ha devuelto a la mano")
                    break

                
    def validar_agregar_ficha(self, jugada):
        self.ordenar_numeros(jugada)
        print('Jugada con la ficha agregada')
        for ficha in jugada:
            print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')

        if self.detectar_tercia(jugada):
            return True
        else:
            if self.detectar_escalera(jugada):
                return True
            else:
                return False
        
    def detectar_tercia(self, jugada):
        for i, ficha in enumerate(jugada):
            if ficha.numero == 0 or ficha.color == 'comodin':
                continue
            if i == 0:
                continue
            if ficha.numero != jugada[0].numero:
                return False
            elif ficha.color == jugada[i-1].color or ficha.color == jugada[0].color:
                return False
            
        return len(jugada) == 3

    def detectar_escalera(self, jugada):
        for i, ficha in enumerate(jugada):
            if i == 0:
                continue
            if abs(ficha.numero - jugada[i-1].numero) != 1:
                return False
            if ficha.color != jugada[i-1].color:
                return False
        return True

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
            if abs(ficha.numero - jugada[i-1].numero) != 1 and not comodin:
                return False
            
            if abs(ficha.numero - jugada[i-1].numero) == 1 and ficha.color == jugada[0].color:
                continue
            else:
                return False
        return True
    
    def ganar(self):
        if len(self.mano) == 0:
            return True
        else:
            return False


class bot():
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.jugadas = []
    
    def llenar_mano_bot(self):
        return self.mano
    
    def mostrar_mano(self):
        if len(self.mano) == 0:
            print('Mano vacia')
        else:
            print(f'Mano de {self.nombre}')
            for ficha in self.mano:
                color = COLOR_RESET
                if ficha.color == 'amarillo':
                    color = COLOR_YELLOW
                if ficha.color == 'azul':
                    color = COLOR_BLUE
                if ficha.color == 'rojo':
                    color = COLOR_RED
                if ficha.color == 'verde':
                    color = COLOR_GREEN
                if ficha.color == 'comodin':
                    color = COLOR_WHITE
                print('[' + color + f'{ficha.numero}' + COLOR_RESET + ']', end='')
        print()

    def mostrar_jugadas(self):
        if len(self.jugadas) == 0:
            print('[]')
        else:
            print(f'Jugadas de {self.nombre}')
            for jugada in self.jugadas:
                for ficha in jugada:
                    color = COLOR_RESET
                    if ficha.color == 'amarillo':
                        color = COLOR_YELLOW
                    if ficha.color == 'azul':
                        color = COLOR_BLUE
                    if ficha.color == 'rojo':
                        color = COLOR_RED
                    if ficha.color == 'verde':
                        color = COLOR_GREEN
                    if ficha.color == 'comodin':
                        color = COLOR_WHITE
                    print('[' + color + f'{ficha.numero}' + COLOR_RESET + ']', end='')
                print()
        print()

    def ver_jugadas(self, jugadas):
        if len(jugadas) == 0:
            print('[]')
        else:
            for i, jugada in enumerate(jugadas, start=1):
                print(f"jugada {i}:")
                for ficha in jugada:
                    color = COLOR_RESET
                    if ficha.color == 'amarillo':
                        color = COLOR_YELLOW
                    if ficha.color == 'azul':
                        color = COLOR_BLUE
                    if ficha.color == 'rojo':
                        color = COLOR_RED
                    if ficha.color == 'verde':
                        color = COLOR_GREEN
                    if ficha.color == 'comodin':
                        color = COLOR_WHITE
                    print('[' + color + f'{ficha.numero}' + COLOR_RESET + ']', end='')
                print()
        print()

    def ordenar_mano_bot(self):
        #ordenar la mano del bot usando cocktail-sort
        n = len(self.mano)
        swapped = True
        start = 0
        end = n - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if self.comparar_fichas(self.mano[i], self.mano[i + 1]) > 0:
                    self.mano[i], self.mano[i + 1] = self.mano[i + 1], self.mano[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                if self.comparar_fichas(self.mano[i], self.mano[i + 1]) > 0:
                    self.mano[i], self.mano[i + 1] = self.mano[i + 1], self.mano[i]
                    swapped = True

            start += 1

    def comparar_fichas(self, ficha1, ficha2):
        color_order = ["amarillo", "azul", "rojo", "verde", "comodin"]
        # Compara los colores de las fichas
        if ficha1.color != ficha2.color:
            return color_order.index(ficha1.color) - color_order.index(ficha2.color)
        else:
            return ficha1.numero - ficha2.numero

    def ordenar_numeros(self, jugada):
        #ordenar la mano del bot usando cocktail-sort
        n = len(jugada)
        swapped = True
        start = 0
        end = n - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if self.comparar_fichas_numeros(jugada[i], jugada[i + 1]) > 0:
                    jugada[i], jugada[i + 1] = jugada[i + 1], jugada[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                if self.comparar_fichas_numeros(jugada[i], jugada[i + 1]) > 0:
                    jugada[i], jugada[i + 1] = jugada[i + 1], self.mano[i]
                    swapped = True

            start += 1

    def comparar_fichas_numeros(self, ficha1, ficha2):
        return ficha1.numero - ficha2.numero

    def comer_bot(self, pozo):
        if len(pozo) == 0:
            return
        ficha = pozo.pop()
        print(f"El {self.nombre} ha comido la ficha {ficha.numero} {ficha.color}")
        self.mano.append(ficha) 
    
    def planear_jugadas(self, rondas, pozo, jugadores):
        self.ordenar_mano_bot()
        cont_jugadas = 0
        if self.jugada_libre(rondas):
            return True
        
        for jugador in jugadores:
            for jugadas in jugador.jugadas:
                if not jugadas:
                    continue
                else:
                    cont_jugadas += 1

        if len(self.jugadas) < 2 or rondas < 10:
            if self.jugada_greedy():
                self.agregar_a_jugadas(jugadores, rondas)
                for jugador in jugadores:
                    for jugada in jugador.jugadas:
                        self.ordenar_numeros(jugada)
                self.mostrar_jugadas()
            else:
                self.comer_bot(pozo)
        else:
            if self.jugada_lazy():
                self.mostrar_jugadas()
            else:
                self.comer_bot(pozo)
    
    def jugada_lazy(self):
        if self.escalera():
            return True
        else:
            if self.tercia():
                return True
            else:
                return False

    def jugada_greedy(self):
        self.ordenar_numeros(self.mano)
        jugadas_greedy = []
        jugada_copy = self.mano[:]
        jugadas_validas = []
        visto = set()

        #para separar todas las tercias posibles
        for ficha in jugada_copy:
                if ficha.numero in visto:
                    continue
                coincidencias = [ficha]
                for comprobar in jugada_copy:
                    if ficha.numero == comprobar.numero and ficha != comprobar:
                        coincidencias.append(comprobar)
                    if len(coincidencias) == 3:
                        break
                if len(coincidencias) == 3:
                    jugadas_greedy.extend(coincidencias)
                    visto.add(ficha.numero)

        jugadas_validas = self.dividir_tercias(jugadas_greedy) #se agregan las tercias a las jugadas validas
        
        #separar todas las escaleras posibles
        visto.clear()
        self.ordenar_mano_bot()

        escalera = [self.mano[0]]  # Inicializamos la escalera con la primera ficha de la mano
        escalera_valida = []
        for i in range(1, len(self.mano)):
            ficha_actual = self.mano[i]
            ficha_anterior = self.mano[i - 1]

            # Verificar si las fichas tienen el mismo color y son consecutivas
            if (ficha_actual.color == ficha_anterior.color) and (ficha_actual.numero == ficha_anterior.numero + 1):
                escalera.append(ficha_actual)
            elif ficha_actual.numero != ficha_anterior.numero:  # Si no son consecutivas y no tienen el mismo número
                escalera = [ficha_actual]  # Iniciar una nueva escalera

            if len(escalera) >= 3:
                escalera_valida.append(escalera)
                escalera = [ficha_actual] #resetear la escalera cuando se agreguen
        
        jugadas_validas += escalera_valida

        suma_jugada = 0
        if not self.jugadas:
            if not jugadas_validas:
                return False
            else:
                for jugada in jugadas_validas:
                    for ficha in jugada:
                        suma_jugada += ficha.numero
                if suma_jugada < 25:
                    return False
                else:
                    for jugada in jugadas_validas:
                        self.jugadas.append(jugada)
                        for ficha in jugada:
                            if ficha in self.mano:
                                self.mano.remove(ficha)
                    return True       
        
        if not jugadas_validas:
            return False
        else:
            for jugada in jugadas_validas:
                self.jugadas.append(jugada)
                for ficha in jugada:
                    if ficha in self.mano:
                        self.mano.remove(ficha)
            return True
    
    def jugada_libre(self, rondas):
        if rondas > 10 and not self.jugadas:
            return True
        else:
            return True

    def agregar_a_jugadas(self, jugadores, rondas):
        if rondas ==1 or not self.jugadas:
            return
        
        jugadas = []
        for jugador in jugadores:
            for jugada in jugador.jugadas:
                jugadas.append(jugada)


        jugadas_tercia = []
        jugadas_escalera = []
        for jugada in jugadas:
            if self.detectar_tercia(jugada):
                jugadas_tercia.append(jugada)
            else:
                if self.detectar_escalera(jugada):
                    jugadas_escalera.append(jugada)
        
        for jugada in jugadas_tercia:
            colores = set()
            for ficha in jugada:
                colores.add(ficha.color)
            for ficha in self.mano:
                if (ficha.numero == jugada[0].numero and ficha.color not in colores) and len(jugada) == 3:
                    print(f'{self.nombre} agrego {ficha.numero} color: {ficha.color} a una jugada tercia')
                    jugada.append(ficha)
                    print('Jugada con la ficha agregada:')
                    for ficha in jugada:
                        print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
                    break
                else:
                    continue
            break

        for jugada in jugadas_tercia:
            for ficha in jugada:
                if ficha in self.mano:
                    self.mano.remove(ficha)

        for jugada in jugadas_escalera:
            primera_ficha = jugada[0]
            ultima_ficha = jugada[-1]
            numeros = set()
            for ficha in jugada:
                numeros.add(ficha.numero)
            for ficha in self.mano: 
                if (abs(ficha.numero - primera_ficha.numero) == 1 or abs(ficha.numero - ultima_ficha.numero) == 1) and ficha.color == primera_ficha.color:
                    if ficha.numero not in numeros:
                        print(f'{self.nombre} agrego {ficha.numero} color: {ficha.color} a una jugada escalera')
                        jugada.append(ficha)
                        print('Jugada con la ficha agregada:')
                        for ficha in jugada:
                            print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
                        break
                    else:
                        continue
                else:
                    continue
            break

        for jugada in jugadas_escalera:
            for ficha in jugada:
                if ficha in self.mano:
                    self.mano.remove(ficha)


        self.mostrar_mano()
        return 
        """print('\nmano actualizada')
        for ficha in mano_bot:
            print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
        
        for jugada in jugadas:
            ordenar_mano_bot(jugada)
        
        print('\njugadas actualizadas:')
        for jugada in jugadas:
            for ficha in jugada:
                print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
            print() """

    def detectar_tercia(self, jugada):
        for i, ficha in enumerate(jugada):
            if ficha.numero == 0 or ficha.color == 'comodin':
                continue
            if i == 0:
                continue
            if ficha.numero != jugada[0].numero:
                return False
            elif ficha.color == jugada[i-1].color or ficha.color == jugada[0].color:
                return False
            
        return len(jugada) == 3

    def detectar_escalera(self, jugada):
        for i, ficha in enumerate(jugada):
            if i == 0:
                continue
            if abs(ficha.numero - jugada[i-1].numero) != 1:
                return False
            if ficha.color != jugada[i-1].color:
                return False
        return True
        
    def cuarta(self):
        cuarta = []
        visto = set()
        comodines = []
        mano_copia = self.mano[:]

        for ficha in mano_copia:
            if ficha.numero == 0 or ficha.color == 'comodin':
                comodines.append(ficha)

        for ficha in mano_copia:
            if ficha.numero in visto:
                continue
            coincidencias = [ficha]
            for comprobar in mano_copia:
                if ficha.numero == comprobar.numero and ficha != comprobar:
                    coincidencias.append(comprobar)
                if len(coincidencias) == 4:
                    break
                elif len(coincidencias) == 3 and len(comodines) == 1:
                    break
            if len(coincidencias) == 4:
                cuarta.extend(coincidencias)
                visto.add(ficha.numero)
            elif len(coincidencias) == 3 and len(comodines) == 1:
                coincidencias.extend(comodines)
                cuarta.extend(coincidencias)
                visto.add(ficha.numero)
        
        if self.comprobar_cuarta(cuarta):
            comodines.clear()
            cuarta.clear()
            return True
        else:
            comodines.clear()
            cuarta.clear()
            return False

    def comprobar_cuarta(self, jugada):
        cuarta_valida = []
        for arr in jugada:
            valido = True
            for i, ficha in enumerate(arr):
                if ficha.numero == 0 or ficha.color == 'comodin':
                    continue
                if i == 0:
                    continue
                if ficha.numero != arr[0]:
                    break
                if ficha.color == arr[i-1].color or ficha.color == arr[0].color:
                    valido = False
                    break
            if valido:
                cuarta_valida.append(arr)
        
        for arr in cuarta_valida:
            self.jugadas.append(arr)
            for ficha in arr:
                if ficha in self.mano:
                    self.mano.remove(ficha)
            return True

    def tercia(self):
        tercia = []
        visto = set()
        comodines = []
        # Copiar self.mano para evitar problemas de modificación durante la iteración
        mano_copia = self.mano[:]
        
        for ficha in mano_copia:
            if ficha.numero == 0 or ficha.color == 'comodin':
                comodines.append(ficha)

        for ficha in mano_copia:
            if ficha.numero in visto:
                continue
            coincidencias = [ficha]
            for comprobar in mano_copia:
                if ficha.numero == comprobar.numero and ficha != comprobar:
                    coincidencias.append(comprobar)
                if len(coincidencias) == 3:
                    break
                elif len(coincidencias) == 2 and len(comodines) == 1:
                    break
                elif len(coincidencias) == 1 and len(comodines) == 2:
                    break
            if len(coincidencias) == 3:
                tercia.extend(coincidencias)
                visto.add(ficha.numero)
            elif len(coincidencias) == 2 and len(comodines) == 1:
                coincidencias.extend(comodines)
                tercia.extend(coincidencias)
                visto.add(ficha.numero)
            elif len(coincidencias) == 1 and len(comodines) == 2:
                coincidencias.extend(comodines)
                tercia.extend(coincidencias)
                visto.add(ficha.numero)


        if self.comprobar_tercia(tercia):
            tercia.clear()
            comodines.clear()
            return True
        else:
            comodines.clear()
            tercia.clear()
            return False
            
    def comprobar_tercia(self, tercia):
        
        arr_tercias = self.dividir_tercias(tercia)

        tercias = []
        for arr in arr_tercias:
            es_valida = True
            for i, ficha in enumerate(arr):
                if ficha.numero == 0 or ficha.color == 'comodin':
                    continue
                if i == 0:
                    continue  # Saltar la primera ficha
                if ficha.numero != arr[0].numero:
                    break  # Salir si el número no es el mismo que el de la primera ficha
                elif ficha.color == arr[i - 1].color:
                    es_valida = False
                    break
            if es_valida:
                tercias.append(arr)

        if len(arr_tercias) == 0:
            return False

        for arr in tercias:
            self.jugadas.append(arr)
            for ficha in arr:
                if ficha in self.mano:
                    self.mano.remove(ficha)
            return True

    def dividir_tercias(self, jugada):
        #esta funcion la ocupa comprobar_tercia y jugada greedy
        jugadas_validas = []
        arr_tercias = []
        sub_size = 3
        for i in range(0, len(jugada), sub_size):
                sub_arreglo = jugada[i: i + sub_size]
                arr_tercias.append(sub_arreglo)
        for arr in arr_tercias:
            valido = True
            for i, ficha in enumerate(arr):
                if i == 0:
                    continue
                if ficha.numero != arr[0].numero:
                    break
                elif ficha.color == arr[i-1].color:
                    valido = False
                    break
                else:
                    continue
            if valido:
                jugadas_validas.append(arr)
        return jugadas_validas
    
    def escalera(self):
        escalera = [self.mano[0]]  # Inicializamos la escalera con la primera ficha de la mano

        for i in range(1, len(self.mano)):
            ficha_actual = self.mano[i]
            ficha_anterior = self.mano[i - 1]

            # Verificar si las fichas tienen el mismo color y son consecutivas
            if (ficha_actual.color == ficha_anterior.color) and (ficha_actual.numero == ficha_anterior.numero + 1):
                escalera.append(ficha_actual)
            elif ficha_actual.numero != ficha_anterior.numero:  # Si no son consecutivas y no tienen el mismo número
                escalera = [ficha_actual]  # Iniciar una nueva escalera

            if len(escalera) >= 3:
                if self.comprobar_escalera(escalera):
                    self.mostrar_mano()
                    escalera.clear()
                    return True
                else:
                    escalera.clear()
                    return False
                
        print(f'{self.nombre} no pudo realizar una escalera')
        escalera.clear()
        return False  # No se encontró una escalera
    
    def comprobar_escalera(self, escalera):
        suma_escalera = 0
        for ficha in escalera:
            suma_escalera += ficha.numero
   
        if suma_escalera < 25 and not self.jugadas:
            print("La primer escalera debe de ser mayor a 25 puntos")
            return False
        else:
            print('Se realizo una escalera')
            self.jugadas.append(list(escalera))
            for ficha in escalera:
                if ficha in self.mano:
                    self.mano.remove(ficha)
            return True

    def ganar(self):
        if len(self.mano) == 0:
            return True
        else:
            return False



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



table = mesa()
modalidad = int(input("Ingrese el modo de juego 1.CPU only 2.Jugador vs CPU "))
table.modalidad(modalidad)
crear_fichas()


pozo = table.mezclar_fichas()
i = 0
orden = random.randint(0,4)
rondas = 0




table.mostrar_manos()

for jugador in table.jugadores:
    if len(jugador.mano) == 0:
        print("Hubo un error, el jugador no tiene fichas")
        exit(1)



while len(table.jugadores) > 1:
    #os.system('cls' if os.name == 'nt' else 'clear') 
    rondas += 1
    print(f"####----> RONDA {rondas} <----#####")
    if rondas == 1:
        table.turno(orden)
    table.mostrar_manos()
    table.mostrar_jugadas()
    if len(table.jugadores) == 1:
        break
    if len(pozo) == 0:
        print('El pozo se quedo sin fichas')
        break
    for j in range(len(table.jugadores)):
        if table.jugadores[table.turno_actual].ganar():
            table.eliminar_jugador(table.turno_actual)

        if isinstance(table.jugadores[table.turno_actual], player):
            table.jugadores[table.turno_actual].armar_jugada(pozo, table.jugadores)
            print()
            table.sig_turno()
            time.sleep(1)
        else:
            if table.jugadores[table.turno_actual].planear_jugadas(rondas, pozo, table.jugadores):
                table.eliminar_jugador(table.turno_actual)
            print()
            table.sig_turno()
            time.sleep(1)
    
    
















