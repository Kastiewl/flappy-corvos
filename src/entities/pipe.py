import random
import pygame
from src.config import (
    PIPE_GAP,
    PIPE_MIN_HEIGHT,
    PIPE_SPEED,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

class Pipe:
    def __init__(self) -> None:
        # Posição horizontal fracionária para física com delta time
        self.x: float = float(SCREEN_WIDTH)

        # Determina a altura aleatória do cano superior respeitando os limites
        max_top_height = SCREEN_HEIGHT - PIPE_GAP - PIPE_MIN_HEIGHT
        self.top_height: int = random.randint(PIPE_MIN_HEIGHT, max_top_height)

        # Retângulo do cano superior (começa no topo da tela y=0)
        self.top_rect: pygame.Rect = pygame.Rect(
            int(self.x), 0, PIPE_WIDTH, self.top_height
        )

        # Retângulo do cano inferior (começa logo abaixo do gap)
        bottom_y = self.top_height + PIPE_GAP
        bottom_height = SCREEN_HEIGHT - bottom_y
        self.bottom_rect: pygame.Rect = pygame.Rect(
            int(self.x), bottom_y, PIPE_WIDTH, bottom_height
        )

        #Flag de pontuação
        self.passed: bool = False
        
        # Carregamento do sprite do cano
        original_pipe_img = pygame.image.load("sprites/Pixel Art - Pipes - FREE/Pipes.png").convert_alpha()
        
        # Escala os canos para preencher os retângulos dinâmicos
        self.bottom_img = pygame.transform.scale(original_pipe_img, (PIPE_WIDTH, bottom_height))
        
        # flipando o cano de cima
        top_scaled = pygame.transform.scale(original_pipe_img, (PIPE_WIDTH, self.top_height))
        self.top_img = pygame.transform.flip(top_scaled, False, True)


    
    def is_off_screen(self) -> bool:
        """Verifica se o par de canos já saiu completamente pelo lado esquerdo"""
        return self.x + PIPE_WIDTH < 0


    def update(self, dt: float) -> None:
        """Move os canos para a esquerda com base no delta time"""
        self.x -= PIPE_SPEED * dt
        # Sincroniza a posição horizontal dos dois retângulos
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, surface: pygame.Surface) -> None:
        """Desenha os retângulos dos canos superior e inferior na tela."""
        surface.blit(self.top_img, self.top_rect.topleft)
        surface.blit(self.bottom_img, self.bottom_rect.topleft)