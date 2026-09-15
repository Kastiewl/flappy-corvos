import pygame
from src.config import (
    BIRD_HEIGHT,
    BIRD_START_X,
    BIRD_START_Y,
    BIRD_WIDTH,
    COLOR_BIRD,
    GRAVITY,
    JUMP_VELOCITY,
)


class Bird:
    def __init__(self) -> None:
        # Posições fracionárias para física precisa com delta time
        self.x: float = BIRD_START_X
        self.y: float = BIRD_START_Y
        self.velocity_y: float = 0.0

        # Retângulo para renderização e detecção de colisões
        self.rect: pygame.Rect = pygame.Rect(
            int(self.x), int(self.y), BIRD_WIDTH, BIRD_HEIGHT
        )

    def jump(self) -> None:
        """Aplica um impulso vertical instantâneo para cima"""
        self.velocity_y = JUMP_VELOCITY

    def update(self, dt: float) -> None:
        """Atualiza a velocidade e posição vertical com base no delta time"""
        # 1. Aplica a gravidade a velocidade vertical (v = v0 + a * dt)
        self.velocity_y += GRAVITY * dt

        # 2. Atualiza a posição com base na velocidade (y = y0 + v * dt)
        self.y += self.velocity_y * dt

        # 3. Sincroniza o retângulo de renderização/colisão com a nova posição
        self.rect.y = int(self.y)

    def draw(self, surface: pygame.Surface) -> None:
        """Desenha o pássaro na superfície fornecida (placeholder geométrico)"""
        pygame.draw.rect(surface, COLOR_BIRD, self.rect)