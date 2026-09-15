import pygame
from src.config import (
    BIRD_HEIGHT,
    BIRD_START_X,
    BIRD_START_Y,
    BIRD_WIDTH,
    COLOR_BIRD,
    GRAVITY,
    JUMP_VELOCITY,
    SCREEN_HEIGHT,
)
from src.entities.pipe import Pipe


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

    def check_collision(self, pipes: list[Pipe]) -> bool:
        """Verifica se o pássaro colidiu com canos, chão ou teto"""
        # Colisão com o chão ou com o teto
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            return True

        # Colisão com qualquer um dos canos ativos
        for pipe in pipes:
            if self.rect.colliderect(pipe.top_rect) or self.rect.colliderect(pipe.bottom_rect):
                return True

        return False

    def reset(self) -> None:
        """Restaura o pássaro para as condições iniciais"""
        self.x = BIRD_START_X
        self.y = BIRD_START_Y
        self.velocity_y = 0.0
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface: pygame.Surface) -> None:
        """Desenha o pássaro na superfície fornecida (placeholder geométrico)"""
        pygame.draw.rect(surface, COLOR_BIRD, self.rect)