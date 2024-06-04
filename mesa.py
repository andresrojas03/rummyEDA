import random

class juego:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.turno_actual = 0

    def turnos(self, orden):
        self.jugadores = self.jugadores[orden-1:] + self.jugadores[:orden-1]
        self.turno_actual = 0
        print(f'Turno del jugador{self.jugadores[self.turno_actual].nombre}')
        return self.jugadores[self.turno_actual]
    
    def sig_turno(self):
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        print(f'siguiente turno es para el jugador {self.jugadores[self.turno_actual].nombre}')
        return self.jugadores[self.turno_actual]
    
    def mostrar_mesa(self):
        print("mesa de juego:")
        for jugador in self.jugadores:
            print(f"{jugador.nombre} ", end='')
        print()    
            

class jugador:
    def __init__(self, nombre):
        self.nombre = nombre

jugadores = [jugador("bot1"), jugador("bot2"), jugador("bot3"), jugador("bot4")]
game = juego(jugadores)
game.turnos(2)
while len(game.jugadores)>=1:
    if len(game.jugadores) == 1:
        break
    game.mostrar_mesa()
    turno  = game.sig_turno()
    if random.randint(0, 1) == 1:
        print(f"jugador {game.jugadores[game.turno_actual].nombre} ha sido retirado de la mesa")
        print(game.turno_actual)
        game.jugadores.pop(game.turno_actual)
    else:
        pass
print(f"{game.jugadores[game.turno_actual].nombre} ha ganado ")