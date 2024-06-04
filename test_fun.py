class Ficha:
    def __init__(self, color, numero):
        self.color = color
        self.numero = numero

def ordenar_numeros(jugada):
    #ordenar la mano del bot usando cocktail-sort
    n = len(jugada)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if comparar_fichas_numeros(jugada[i], jugada[i + 1]) > 0:
                jugada[i], jugada[i + 1] = jugada[i + 1], jugada[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if comparar_fichas_numeros(jugada[i], jugada[i + 1]) > 0:
                jugada[i], jugada[i + 1] = jugada[i + 1], jugada[i]
                swapped = True

        start += 1

def comparar_fichas_numeros( ficha1, ficha2):
    return ficha1.numero - ficha2.numero

def tercia(jugada):
    ordenar_numeros(jugada)
    tercia = []
    visto = set()
    comodines = []
    # Copiar self.mano para evitar problemas de modificación durante la iteración
    mano_copia = jugada[:]
    
    for ficha in mano_copia:
        if ficha.numero == 0 or ficha.color == 'comodin':
            print('comodin encontrado')
            comodines.append(ficha)

    for ficha in jugada:
        print('[' + f'{ficha.numero} color: {ficha.color}' + ']')


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
            print('Jugada con un comodin')
            coincidencias.extend(comodines)
            tercia.extend(coincidencias)
            visto.add(ficha.numero)
            
        elif len(coincidencias) == 1 and len(comodines) == 2:
            print('Jugada con dos comodines')
            coincidencias.extend(comodines)
            tercia.extend(coincidencias)
            visto.add(ficha.numero)

    
    comprobar_tercia(tercia, comodines)
            
def comprobar_tercia(tercia, comodines):
    arr_tercias = dividir_tercias(tercia)
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
    

    #if not self.jugadas:
    tercias_validas = []
    for arr in tercias:
        suma_tercias = 0
        for ficha in arr:
            suma_tercias += ficha.numero
        if suma_tercias < 25 and len(comodines) == 0:
            break
        if suma_tercias >= 25:
            tercias_validas.append(arr)
            break
        elif suma_tercias > 16 and len(comodines) == 1:
            tercias_validas.append(arr)
            break
        elif suma_tercias >= 9 and len(comodines) == 2:
            tercias_validas.appennd(arr)
            break
        
    
    for arr in tercias_validas:
        for ficha in arr:
            print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
        print()
            


def dividir_tercias(jugada):
    jugadas_validas = []
    arr_tercias = []
    sub_size = 3
    for i in range(0, len(jugada), sub_size):
            sub_arreglo = jugada[i: i + sub_size]
            arr_tercias.append(sub_arreglo)
    for arr in arr_tercias:
        valido = True
        for i, ficha in enumerate(jugada):
            if i == 0:
                continue
            if ficha.numero != jugada[i-1].numero:
                break
            if ficha.color == jugada[i-1].color:
                print("Jugada invalida")
                valido = False
                break
            else:
                continue
        if valido:
            jugadas_validas.append(arr)
    return jugadas_validas

jugada = [
    Ficha('amarillo', 6),
    Ficha('azul', 9),
    Ficha('comodin', 0),
    Ficha('verde', 12),
    Ficha('rojo', 9),
    Ficha('verde', 2),
    Ficha('amarillo', 8),
    Ficha('rojo', 7),
    Ficha('verde', 3),
    Ficha('amarillo', 7),
    Ficha('rojo', 6),
    Ficha('amarillo', 8),
    Ficha('verde', 4),
    Ficha('verde', 5),
    Ficha('rojo', 10),
    Ficha('azul', 12),
    Ficha('amarillo', 12),
]

tercia(jugada)

""" jugadas_validas = jugada_lazy(jugada)

for play in jugadas_validas:
    print()
    for ficha in play:
        print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='') """
    