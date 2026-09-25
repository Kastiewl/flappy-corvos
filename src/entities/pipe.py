import random
from pathlib import Path
import pygame
from src.config import (
    PIPE_MIN_HEIGHT,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

# Caminho absoluto para a textura do cano a partir da raiz do projeto
PIPE_SPRITE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "sprites"
    / "pipes"
    / "pipes.png"
)


class Pipe:
    # Cache estático: carrega a imagem da textura apenas UMA vez na memória
    _base_image: pygame.Surface | None = None

    def __init__(self, gap: float, speed: float) -> None:
        self.x: float = float(SCREEN_WIDTH)
        self.passed: bool = False
        self.gap: float = gap
        self.speed: float = speed

        # 1. Carregamento sob demanda (apenas na criação do primeiro cano)
        if Pipe._base_image is None:
            if PIPE_SPRITE_PATH.exists():
                Pipe._base_image = pygame.image.load(str(PIPE_SPRITE_PATH)).convert_alpha()
            else:
                # Fallback de segurança caso o caminho do ficheiro mude
                Pipe._base_image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
                Pipe._base_image.fill((50, 160, 65))

        # Definição procedural de alturas respeitando o vão da dificuldade
        max_top_height = int (SCREEN_HEIGHT - self.gap - PIPE_MIN_HEIGHT)
        self.top_height: int = random.randint(PIPE_MIN_HEIGHT, max_top_height)
        self.bottom_y: int = int(self.top_height + self.gap)
        self.bottom_height: int = SCREEN_HEIGHT - self.bottom_y

        # Retângulos de colisão (AABB)
        self.top_rect: pygame.Rect = pygame.Rect(
            int(self.x), 0, PIPE_WIDTH, self.top_height
        )
        self.bottom_rect: pygame.Rect = pygame.Rect(
            int(self.x), self.bottom_y, PIPE_WIDTH, self.bottom_height
        )

        # Redimensionamento e espelhamento das texturas
        self.bottom_img = pygame.transform.scale(
            Pipe._base_image, (PIPE_WIDTH, self.bottom_height)
        )
        top_scaled = pygame.transform.scale(
            Pipe._base_image, (PIPE_WIDTH, self.top_height)
        )
        self.top_img = pygame.transform.flip(top_scaled, False, True)
        
    def is_off_screen(self) -> bool:
        """Verifica se o par de canos já saiu completamente pelo lado esquerdo"""
        return self.x + PIPE_WIDTH < 0


    def update(self, dt: float) -> None:
        """Desloca os canos com base na velocidade dinâmica da dificuldade"""
        self.x -= self.speed * dt
        # Sincroniza a posição horizontal dos dois retângulos
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, surface: pygame.Surface) -> None:
        """Desenha os retângulos dos canos superior e inferior na tela."""
        surface.blit(self.top_img, self.top_rect.topleft)
        surface.blit(self.bottom_img, self.bottom_rect.topleft)