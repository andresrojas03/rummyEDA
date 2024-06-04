class Ficha:
    def __init__(self, color, numero):
        self.color = color
        self.numero = numero

def jugada_lazy(jugada, jugadas_hechas):
    tercia = []
    visto = set()
    suma = 0
    for ficha in jugada:
        if ficha.numero in visto:
            continue
        coincidencias = [ficha]
        for comprobar in jugada:
            if ficha.numero == comprobar.numero and ficha != comprobar:
                coincidencias.append(comprobar)
            if len(coincidencias) == 3:
                break

        if len(coincidencias) == 3:
            tercia.extend(coincidencias)
            visto.add(ficha.numero)
    for ficha in tercia:
        suma += ficha.numero
    
    if jugadas_hechas == 0:
        if suma <= 25:
            print('Tu primer jugada debe de ser mayor a 25 puntos')
            return tercia, suma
        else:
            print("Jugada valida")
            return tercia, suma

    else:
        print("jugada valida")
        return tercia, suma
    
    


jugada = [
    Ficha('amarillo', 2),
    Ficha('azul', 5),
    Ficha('rojo', 2),
    Ficha('verde', 12),
    Ficha('rojo', 5),
    Ficha('verde', 2),
    Ficha('amarillo', 5)
]

tercia, suma = jugada_lazy(jugada, 1)

for ficha in tercia:
    print(f'Ficha {ficha.color} de color {ficha.numero}.')
print(f'Suma total es de {suma} puntos')
