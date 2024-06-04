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

    def modalidad(self):
            modalidad = 1
            if modalidad == 1:
                self.crear_jugadores(jugador = False)
            elif modalidad == 2:
                self.crear_jugadores(jugador = True)    
    
    def crear_jugadores(self, jugador):
        if jugador:
            for i in range(3):
                self.jugadores.append(bot(f'bot{i+1}'))
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
        pozo = sum([fichas.amarillo, fichas.azul, fichas.verde, fichas.rojo, fichas.comodin], [])
        random.shuffle(pozo)
        for i in range(n):
            if isinstance(self.jugadores[i], bot):
                mano_jugador = self.jugadores[i].llenar_mano_bot()
            for j in range(14):
                ficha = pozo.pop()
                mano_jugador.append(ficha)
        return pozo     

    def mostrar_jugadas(self):
        for jugador in self.jugadores:
            if len(jugador.jugadas) == 0:
                print('[]')
            else:
                print(f'Jugadas de {jugador.nombre}: ')
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

    def ordenar_numeros(self):
        #ordenar la mano del bot usando cocktail-sort
        n = len(self.mano)
        swapped = True
        start = 0
        end = n - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if self.comparar_fichas_numeros(self.mano[i], self.mano[i + 1]) > 0:
                    self.mano[i], self.mano[i + 1] = self.mano[i + 1], self.mano[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                if self.comparar_fichas_numeros(self.mano[i], self.mano[i + 1]) > 0:
                    self.mano[i], self.mano[i + 1] = self.mano[i + 1], self.mano[i]
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
    
    #agregar la opcion de comprobar las jugadas de los demas jugadores
    def planear_jugadas(self, rondas, pozo, jugadores):
        self.ordenar_mano_bot()
        cont_jugadas = 0
        for jugador in jugadores:
            for jugadas in jugador.jugadas:
                if not jugadas:
                    continue
                else:
                    cont_jugadas += 1

        if len(self.jugadas) < 2:
            if self.jugada_greedy():
                self.mostrar_jugadas()
                self.mostrar_mano()
            else:
                self.comer_bot(pozo)
        else:
            if self.jugada_lazy():
                self.mostrar_jugadas()
                self.mostrar_mano()
            else:
                self.comer_bot(pozo)
    
    def jugada_lazy(self):
        if self.tercia():
            return True
        else:
            if self.escalera():
                return True
            else:
                return False
            
    def jugada_greedy(self):
        self.ordenar_numeros()
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
    
    #modificar para que solamente detecte una tercia, no varias porque seria como el greedy
    def tercia(self):
        tercia = []
        visto = set()
        suma = 0
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

        if not self.jugadas:
            if suma >= 25:
                if self.comprobar_tercia(tercia, comodines):
                    tercia.clear()
                    comodines.clear()
                    return True
                else:
                    comodines.clear()
                    tercia.clear()
                    return False
            elif suma < 25 and len(comodines) >= 1:
                print("intentando jugada con comodines")
                if self.comprobar_tercia(tercia,comodines):
                    comodines.clear()
                    tercia.clear()
                    return True
                else:
                    comodines.clear()
                    tercia.clear()
                    return False
        else:
            if self.comprobar_tercia(tercia, comodines):
                comodines.clear()
                tercia.clear()
                return True
            else:
                comodines.clear()
                tercia.clear()
                return False
            
    def comprobar_tercia(self, tercia, comodines):
        
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
crear_fichas()
table.modalidad()
pozo = table.mezclar_fichas()
i = 0
orden = random.randint(0,4)
rondas = 0
table.mostrar_jugadores()
table.mostrar_manos()
while i <= 9:
    #os.system('cls' if os.name == 'nt' else 'clear') 
    rondas += 1
    print(f"####----> RONDA {rondas} <----#####")
    if rondas == 1:
        table.turno(orden)
    
    if len(table.jugadores) == 1:
        break
    
    for j in range(len(table.jugadores)):
        table.jugadores[table.turno_actual].planear_jugadas(rondas, pozo, table.jugadores)
        print()
        table.sig_turno()
        time.sleep(1)
    
    i += 1


table.mostrar_manos()
table.mostrar_jugadas()
