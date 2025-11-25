import pygame

class Jugador:
    def __init__(self, x, y):
        self.x = x
       	self.y = y
        self.velocidad = 5

        try:
            imagen_original = pygame.image.load("assets/jugador/jugador.png")
            self.imagen = pygame.transform.scale(imagen_original, (60, 60))
        except:
            self.imagen = pygame.Surface((60, 60))
            self.imagen.fill((0, 0, 255))

    def mover(self, teclas, velocidad=5):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += velocidad

        self.x = max(0, min(self.x, 740))
        self.y = max(0, min(self.y, 540))

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

 
    def obtener_pos(self):
        return self.x, self.y
