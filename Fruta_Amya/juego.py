import pygame
from jugador import Jugador
from fruta import Fruta
from obstaculo import Obstaculo

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("FrutaManía 🍎")
        self.reloj = pygame.time.Clock()
        self.jugador = Jugador(400, 300)
        self.fruta = Fruta()
        self.obstaculos = [Obstaculo()]  
        self.velocidad_jugador = 5  
        self.puntaje = 0
        self.ejecutando = True

    def checar_colisiones(self):
    jugador_rect = pygame.Rect(self.jugador.x, self.jugador.y, 60, 60)
    fruta_rect = pygame.Rect(self.fruta.x, self.fruta.y, 40, 40)
    
    if jugador_rect.colliderect(fruta_rect):
        self.puntaje += 1
        self.fruta = Fruta()  
        
        # Cada 5 frutas: acelerar todos los obstáculos
        if self.puntaje % 5 == 0:
            for obstaculo in self.obstaculos:
                obstaculo.velocidad += 0.5
            print(f"¡Nivel subió! Velocidad obstáculos: {self.obstaculos[0].velocidad}")
        
        # Cada 10 frutas: agregar un nuevo obstáculo
        if self.puntaje % 10 == 0 and self.puntaje > 0:
            nuevo_obstaculo = Obstaculo()
            self.obstaculos.append(nuevo_obstaculo)
            print(f"¡Nuevo obstáculo! Total: {len(self.obstaculos)}")
        
        # Cada 20 frutas: el jugador se vuelve más lento (cansancio)
        if self.puntaje % 20 == 0 and self.puntaje > 0:
            self.velocidad_jugador = max(2, self.velocidad_jugador - 0.5)
            print(f"¡Cansancio! Velocidad jugador: {self.velocidad_jugador}")
    
    # Verificar colisión con todos los obstáculos
    for obstaculo in self.obstaculos:
        obstaculo_rect = pygame.Rect(obstaculo.x, obstaculo.y, 70, 70)
        if jugador_rect.colliderect(obstaculo_rect):
            self.ejecutando = False
            break

    def iniciar(self):
        fuente = pygame.font.Font(None, 36)

        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            teclas = pygame.key.get_pressed()
            self.jugador.mover(teclas)
            self.checar_colisiones()
            for obstaculo in self.obstaculos:
                obstaculo.seguir_jugador(self.jugador.x, self.jugador.y)



            # Fondo verde claro
            self.pantalla.fill((200, 255, 200))

            self.fruta.dibujar(self.pantalla)
            for obstaculo in self.obstaculos:
                obstaculo.dibujar(self.pantalla)
            self.jugador.dibujar(self.pantalla)

            texto = fuente.render(f"Puntaje: {self.puntaje}", True, (0, 0, 0))
            self.pantalla.blit(texto, (10, 10))

            pygame.display.update()
            self.reloj.tick(30)

        pygame.quit()



