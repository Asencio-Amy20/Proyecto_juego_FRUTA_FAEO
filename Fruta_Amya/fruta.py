import pygame
import random

class Fruta:
    def __init__(self):
        self.x = random.randint(50, 750)
        self.y = random.randint(50, 550)

        try:
            imagen_original = pygame.image.load("assets/fruta/fruta.png")
            self.imagen = pygame.transform.scale(imagen_original, (40, 40))
        except:
            # Si no hay imagen: circulo rojo
            self.imagen = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.imagen, (255, 0, 0), (20, 20), 20)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def obtener_pos(self):
        return self.x, self.y
