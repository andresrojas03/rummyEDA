class Ficha:
    def __init__(self, numero, color):
        self.numero = numero
        self.color = color

def agregar_a_jugadas():
    jugadas = [[Ficha(5, 'amarillo'), Ficha(5, 'azul'), Ficha(5, 'verde')], [Ficha(7, 'rojo'), Ficha(7, 'azul'), Ficha(7, 'verde')], [Ficha(8, 'amarillo'), Ficha(9, 'amarillo'), Ficha(10, 'amarillo')]]
    mano_bot = [Ficha(5, 'rojo'), Ficha(5, 'verde'), Ficha(7, 'amarillo'), Ficha(7, 'amarillo'), Ficha(5, 'azul'), Ficha(11, 'verde')]
    jugadas_tercia = []
    jugadas_escalera = []
    for jugada in jugadas:
        if detectar_tercia(jugada):
            jugadas_tercia.append(jugada)
        else:
            if detectar_escalera(jugada):
                jugadas_escalera.append(jugada) 
    #comprobar las fichas de la mano con las jugadas
    print('Mano del bot: ')
    for ficha in mano_bot:
        print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
    

    for jugada in jugadas_tercia:
        colores = set()
        for ficha in jugada:
            colores.add(ficha.color)
        for ficha in mano_bot:
            if (ficha.numero == jugada[0].numero and ficha.color not in colores) and len(jugada) == 3:
                jugada.append(ficha)
            else:
                continue

    for jugada in jugadas_tercia:
        for ficha in jugada:
            if ficha in mano_bot:
                mano_bot.remove(ficha)

    for jugada in jugadas_escalera:
        primera_ficha = jugada[0]
        ultima_ficha = jugada[-1]
        for ficha in mano_bot: 
            if (abs(ficha.numero - primera_ficha.numero) == 1 or abs(ficha.numero - ultima_ficha.numero) == 1) and ficha.color == primera_ficha.color:
                jugada.append(ficha)
            else:
                continue
        
    for jugada in jugadas_escalera:
        for ficha in jugada:
            if ficha in mano_bot:
                mano_bot.remove(ficha)
    
    print('\nmano actualizada')
    for ficha in mano_bot:
        print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
    
    for jugada in jugadas:
        ordenar_mano_bot(jugada)
    
    print('\njugadas actualizadas:')
    for jugada in jugadas:
        for ficha in jugada:
            print('[' + f'{ficha.numero} color: {ficha.color}' + ']', end='')
        print()
    
    
def ordenar_mano_bot(jugada):
    #ordenar la mano del bot usando cocktail-sort
    n = len(jugada)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if comparar_fichas(jugada[i], jugada[i + 1]) > 0:
                jugada[i], jugada[i + 1] = jugada[i + 1], jugada[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if comparar_fichas(jugada[i], jugada[i + 1]) > 0:
                jugada[i], jugada[i + 1] = jugada[i + 1], jugada[i]
                swapped = True

        start += 1

def comparar_fichas(ficha1, ficha2):
    color_order = ["amarillo", "azul", "rojo", "verde", "comodin"]
    # Compara los colores de las fichas
    if ficha1.color != ficha2.color:
        return color_order.index(ficha1.color) - color_order.index(ficha2.color)
    else:
        return ficha1.numero - ficha2.numero
    


def detectar_tercia(jugada):
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


def detectar_escalera(jugada):
    for i, ficha in enumerate(jugada):
        if i == 0:
            continue
        if abs(ficha.numero - jugada[i-1].numero) != 1:
            return False
        if ficha.color != jugada[i-1].color:
            return False
    return True

agregar_a_jugadas()
