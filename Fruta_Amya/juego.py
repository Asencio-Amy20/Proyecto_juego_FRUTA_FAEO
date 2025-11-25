import pygame
from jugador import Jugador
from fruta import Fruta
from obstaculo import Obstaculo
from powerup import PowerUp
import random

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
        
        
        if self.puntaje % 20 == 0 and self.puntaje > 0:
            self.velocidad_jugador = max(2, self.velocidad_jugador - 0.5)
            print(f"¡Cansancio! Velocidad jugador: {self.velocidad_jugador}")
    
       
for obstaculo in self.obstaculos:
    obstaculo_rect = pygame.Rect(obstaculo.x, obstaculo.y, 70, 70)
    if jugador_rect.colliderect(obstaculo_rect):
        if self.tiene_escudo:
            
            self.tiene_escudo = False
            self.powerup_activo = None
            self.tiempo_powerup = 0
            print("🛡️ ¡Escudo bloqueó el ataque!")
            obstaculo.x = random.randint(100, 700)
            obstaculo.y = random.randint(100, 500)
        else:
            self.ejecutando = False
        break

    def spawn_powerup(self):
    """Genera power-ups aleatoriamente"""
    self.tiempo_spawn_powerup += 1
    
    
    if self.tiempo_spawn_powerup >= 300:
        if random.randint(1, 100) <= 40:
            self.powerups.append(PowerUp())
            print(f"¡Power-up apareció! Tipo: {self.powerups[-1].tipo}")
        self.tiempo_spawn_powerup = 0

    def activar_powerup(self, tipo):
    """Activa el efecto del power-up recolectado"""
    self.powerup_activo = tipo
    
    if tipo == "velocidad":
        self.velocidad_jugador = 10  
        self.tiempo_powerup = 150  
        print("⚡ ¡VELOCIDAD ACTIVADA!")
    
    elif tipo == "escudo":
        self.tiene_escudo = True
        self.tiempo_powerup = 90  
        print("🛡️ ¡ESCUDO ACTIVADO!")
    
    elif tipo == "tiempo_lento":
        for obstaculo in self.obstaculos:
            self.velocidad_obstaculos_original = obstaculo.velocidad
            obstaculo.velocidad = obstaculo.velocidad * 0.3 
        self.tiempo_powerup = 150 
        print("⏰ ¡TIEMPO LENTO ACTIVADO!")
    
    elif tipo == "fruta_dorada":
        self.puntaje += 5  
        print("¡+5 PUNTOS!")
        self.powerup_activo = None 
    
    elif tipo == "bomba":
        
        if len(self.obstaculos) > 1:
            self.obstaculos = [self.obstaculos[0]]
        
        self.obstaculos[0] = Obstaculo()
        print("¡BOMBA! Obstáculos destruidos")
        self.powerup_activo = None  

    def actualizar_powerups(self):
    """Actualiza el estado de los power-ups activos"""
   
    self.powerups = [p for p in self.powerups if p.esta_vivo()]
    
    # Verificar colisiones con power-ups
    jugador_rect = pygame.Rect(self.jugador.x, self.jugador.y, 60, 60)
    for powerup in self.powerups[:]:
        powerup_rect = pygame.Rect(powerup.x - powerup.tamano, powerup.y - powerup.tamano, 
                                   powerup.tamano * 2, powerup.tamano * 2)
        if jugador_rect.colliderect(powerup_rect):
            self.activar_powerup(powerup.tipo)
            self.powerups.remove(powerup)
    
   
    if self.powerup_activo and self.tiempo_powerup > 0:
        self.tiempo_powerup -= 1
        
        if self.tiempo_powerup <= 0:
            if self.powerup_activo == "velocidad":
                self.velocidad_jugador = 5
                print("⚡ Velocidad terminó")
            
            elif self.powerup_activo == "escudo":
                self.tiene_escudo = False
                print("🛡️ Escudo terminó")
            
            elif self.powerup_activo == "tiempo_lento":
                for obstaculo in self.obstaculos:
                    obstaculo.velocidad = obstaculo.velocidad / 0.3  
                print("⏰ Tiempo lento terminó")
            
            self.powerup_activo = None

    def iniciar(self):
        fuente = pygame.font.Font(None, 36)

        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            teclas = pygame.key.get_pressed()
            self.jugador.mover(teclas, self.velocidad_jugador)
            self.checar_colisiones()
            self.spawn_powerup()
            self.actualizar_powerups()
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
            
            texto_obstaculos = fuente.render(f"Obstaculos: {len(self.obstaculos)}", True, (255, 0, 0))
            self.pantalla.blit(texto_obstaculos, (10, 50))
            
            texto_velocidad = fuente.render(f"Velocidad: {self.velocidad_jugador:.1f}", True, (0, 0, 255))
            self.pantalla.blit(texto_velocidad, (650, 10))

            pygame.display.update()
            self.reloj.tick(30)

        pygame.quit()








