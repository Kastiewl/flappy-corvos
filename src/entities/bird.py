import pygame
from src.config import (
    BIRD_HEIGHT,
    BIRD_START_X,
    BIRD_START_Y,
    BIRD_WIDTH,
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
        self.rect: pygame.Rect = pygame.Rect(
            int(self.x), int(self.y), BIRD_WIDTH, BIRD_HEIGHT
        )
        
        # Carregamento e animação dos sprites
        self.frames = []
        for i in range(8):
            # Carrega os sprites
            img = pygame.image.load(f"sprites/Pixel Art Bird 16x16/voo{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (BIRD_WIDTH, BIRD_HEIGHT))
            # Flipando
            img = pygame.transform.flip(img, True, False)
            self.frames.append(img)
            
        self.current_frame: float = 0.0
        # Velocidade da animação
        self.animation_speed: float = 20.0

    def jump(self) -> None:
        """Aplica um impulso vertical instantâneo para cima"""
        self.velocity_y = JUMP_VELOCITY

    def update(self, dt: float) -> None:
        """Atualiza a velocidade e posição vertical com base no delta time"""
        # 1. Aplica a gravidade a velocidade vertical (v = v0 + a * dt
        self.velocity_y += GRAVITY * dt

        # 2. Atualiza a posição com base na velocidade (y = y0 + v * dt)
        self.y += self.velocity_y * dt

        # 3. Sincroniza o retângulo de renderização/colisão com a nova posição
        self.rect.y = int(self.y)
        
        # Animação condicional: apenas bate as asas se estiver subindo (velocidade negativa)
        if self.velocity_y < 0:
            self.current_frame += self.animation_speed * dt
            if self.current_frame >= len(self.frames):
                self.current_frame = 0.0
        else:
            # Trava no primeiro frame (ou um frame de planeio) quando estiver caindo
            self.current_frame = 0.0

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
        self.current_frame = 0.0

    def draw(self, surface: pygame.Surface) -> None:
        # Desenha o frame atual da animação e rotaciona levemente com base na velocidade
        frame_idx = int(self.current_frame)
        image = self.frames[frame_idx]
        
        # Inclinação suave do pássaro baseada na velocidade vertical
        angle = -max(-45, min(45, self.velocity_y * 0.1))
        rotated_image = pygame.transform.rotate(image, angle)
        
        # Centraliza a rotação no retângulo
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect.topleft)