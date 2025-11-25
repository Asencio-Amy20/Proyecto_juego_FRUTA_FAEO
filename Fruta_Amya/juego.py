import pygame
from jugador import Jugador
from fruta import Fruta
from obstaculo import Obstaculo
from powerup import PowerUp
import random

class Juego:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pygame.time.Clock()

        # Objetos del juego
        self.jugador = Jugador(400, 300)
        self.fruta = Fruta()
        self.obstaculos = [Obstaculo()]
        
        # Variables del juego
        self.velocidad_jugador = 5
        self.powerups = []
        self.tiempo_spawn_powerup = 0
        self.powerup_activo = None
        self.tiempo_powerup = 0
        self.velocidad_obstaculos_original = 2
        self.tiene_escudo = False
        self.puntaje = 0
        self.ejecutando = True


    def checar_colisiones(self):
        jugador_rect = pygame.Rect(self.jugador.x, self.jugador.y, 60, 60)
        fruta_rect = pygame.Rect(self.fruta.x, self.fruta.y, 40, 40)

        # Colisión con fruta
        if jugador_rect.colliderect(fruta_rect):
            self.puntaje += 1
            self.fruta = Fruta()

            if self.puntaje % 5 == 0:
                for obst in self.obstaculos:
                    obst.velocidad += 0.5

            if self.puntaje % 10 == 0:
                self.obstaculos.append(Obstaculo())

            if self.puntaje % 20 == 0:
                self.velocidad_jugador = max(2, self.velocidad_jugador - 0.5)

        # Colisión con obstáculos
        for obst in self.obstaculos:
            obst_rect = pygame.Rect(obst.x, obst.y, 70, 70)
            if jugador_rect.colliderect(obst_rect):
                if self.tiene_escudo:
                    self.tiene_escudo = False
                    self.powerup_activo = None
                    self.tiempo_powerup = 0
                    obst.x = random.randint(100, 700)
                    obst.y = random.randint(100, 500)
                else:
                    self.ejecutando = False
                break

    def spawn_powerup(self):
        self.tiempo_spawn_powerup += 1

        if self.tiempo_spawn_powerup >= 300:
            if random.randint(1, 100) <= 40:
                self.powerups.append(PowerUp())
            self.tiempo_spawn_powerup = 0

    def activar_powerup(self, tipo):
        self.powerup_activo = tipo

        if tipo == "velocidad":
            self.velocidad_jugador = 10
            self.tiempo_powerup = 150

        elif tipo == "escudo":
            self.tiene_escudo = True
            self.tiempo_powerup = 90

        elif tipo == "tiempo_lento":
            for ob in self.obstaculos:
                self.velocidad_obstaculos_original = ob.velocidad
                ob.velocidad *= 0.3
            self.tiempo_powerup = 150

        elif tipo == "fruta_dorada":
            self.puntaje += 5
            self.powerup_activo = None

        elif tipo == "bomba":
            if len(self.obstaculos) > 1:
                self.obstaculos = [self.obstaculos[0]]
            self.obstaculos[0] = Obstaculo()
            self.powerup_activo = None

    def actualizar_powerups(self):
        self.powerups = [p for p in self.powerups if p.esta_vivo()]

        jugador_rect = pygame.Rect(self.jugador.x, self.jugador.y, 60, 60)

        for power in self.powerups[:]:
            rect_p = pygame.Rect(power.x - power.tamano, power.y - power.tamano,
                                 power.tamano * 2, power.tamano * 2)

            if jugador_rect.colliderect(rect_p):
                self.activar_powerup(power.tipo)
                self.powerups.remove(power)

        # Reducir duración del powerup
        if self.powerup_activo and self.tiempo_powerup > 0:
            self.tiempo_powerup -= 1

            if self.tiempo_powerup <= 0:

                if self.powerup_activo == "velocidad":
                    self.velocidad_jugador = 5

                elif self.powerup_activo == "escudo":
                    self.tiene_escudo = False

                elif self.powerup_activo == "tiempo_lento":
                    for ob in self.obstaculos:
                        ob.velocidad = ob.velocidad / 0.3

                self.powerup_activo = None

 
    def guardar_record(self):
        try:
            try:
                with open("records.txt", "r") as archivo:
                    records = []
                    for linea in archivo:
                        if linea.strip():
                            punt = int(linea.split(" - ")[0])
                            records.append(punt)
            except:
                records = []

            records.append(self.puntaje)
            records.sort(reverse=True)
            records = records[:5]

            with open("records.txt", "w") as archivo:
                for i, punt in enumerate(records):
                    archivo.write(f"{punt} - Jugador{i+1}\n")
            return True

        except:
            return False


    def pantalla_game_over(self):
        fuente_grande = pygame.font.Font(None, 80)
        fuente_mediana = pygame.font.Font(None, 50)
        fuente_pequeña = pygame.font.Font(None, 36)

        self.pantalla.fill((0, 0, 0))

        texto = fuente_grande.render("GAME OVER", True, (255, 0, 0))
        rect = texto.get_rect(center=(400, 150))
        self.pantalla.blit(texto, rect)

        texto_puntaje = fuente_mediana.render(f"Puntaje Final: {self.puntaje}", True, (255, 255, 100))
        rect_puntaje = texto_puntaje.get_rect(center=(400, 250))
        self.pantalla.blit(texto_puntaje, rect_puntaje)

        pygame.display.update()

        esperando = True
        while esperando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return "salir"

                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    esperando = False

        return "menu"

  
    def iniciar(self):
        fuente = pygame.font.Font(None, 36)
        self.ejecutando = True

        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "salir"

            teclas = pygame.key.get_pressed()
            self.jugador.mover(teclas, self.velocidad_jugador)

            self.checar_colisiones()
            self.spawn_powerup()
            self.actualizar_powerups()

            for obst in self.obstaculos:
                obst.seguir_jugador(self.jugador.x, self.jugador.y)

            self.pantalla.fill((200, 255, 200))
            self.fruta.dibujar(self.pantalla)

            for p in self.powerups:
                p.dibujar(self.pantalla)

            for obst in self.obstaculos:
                obst.dibujar(self.pantalla)

            self.jugador.dibujar(self.pantalla)

            texto = fuente.render(f"Puntaje: {self.puntaje}", True, (0, 0, 0))
            self.pantalla.blit(texto, (10, 10))

            pygame.display.update()
            self.reloj.tick(30)

        self.guardar_record()
        return self.pantalla_game_over()

