from pathlib import Path
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

# Raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Caminho absoluto para a pasta dos sprites do pássaro
SPRITES_DIR = ROOT_DIR / "sprites" / "bird"
if not SPRITES_DIR.exists():
    SPRITES_DIR = ROOT_DIR / "bird"

def recolor_to_raven(surface: pygame.Surface) -> pygame.Surface:
    """Substitui tons azuis por tons de preto/grafite do corvo,
    
    mantendo o bico amarelo, o olho e o relevo/sombra das penas"""
    recolored = surface.copy()
    width, height = recolored.get_size()

    for x in range(width):
        for y in range(height):
            r, g, b, a = recolored.get_at((x, y))

            # Ignora pixels 100% transparentes
            if a == 0:
                continue

            # Detecta se o pixel é azul (predomínio de azul sobre vermelho e verde)
            if b > r and b > g:
                # Calcula a luminosidade relativa para preservas as sombras originais
                luminance = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0

                # Converte para tons de grafite escuro (entre 22 e 70)
                gray = int(22 + luminance * 48)

                # Mantém um leve tom azul-noite metálico típico de plumagem de corvo
                recolored.set_at((x, y), (gray, gray, int(gray * 1.18), a))

    return recolored

class Bird:
    # Cache estático de frames para carregar e processar apenas uma vez na execução
    _frames_cache: list[pygame.Surface] | None = None

    def __init__(self) -> None:
        # Posições fracionárias para física precisa com delta time
        self.x: float = BIRD_START_X
        self.y: float = BIRD_START_Y
        self.velocity_y: float = 0.0

        self.rect: pygame.Rect = pygame.Rect(
            int(self.x), int(self.y), BIRD_WIDTH, BIRD_HEIGHT
        )
        
        # Carregamento e processamento dos sprites
        if Bird._frames_cache is None:
            Bird._frames_cache = self._load_frames()

        self.frames = Bird._frames_cache
        self.current_frame: float = 0.0
        self.animation_speed: float = 16.0 # Frequência fluída de bater de asas

    def _load_frames(self) -> list[pygame.Surface]:
        """Carrega, recolore, redimensiona e espelha os 8 frames de voo."""
        loaded_frames: list[pygame.Surface] = []

        for i in range (8):
            frame_path = SPRITES_DIR / f"voo{i}.png"

            if frame_path.exists():
                img = pygame.image.load(str(frame_path)).convert_alpha()

                # Troca a paleta de cor no tamanho nativo 16x16 (alta perfomance)
                img = recolor_to_raven(img)

                # Escala para as dimensões configuradas do jogo
                img = pygame.transform.scale(img, (BIRD_WIDTH, BIRD_HEIGHT))

                # Espelha horizontalmente para voar virado para a direita
                img = pygame.transform.flip(img, True, False)

                loaded_frames.append(img)
            else:
                # Fallback de segurança se algum arquivo não for encontrado
                fallback = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
                fallback.fill((35, 35, 40))
                loaded_frames.append(fallback)

        return loaded_frames
    
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
        angle = -max(-45, min(35.0, self.velocity_y * 0.12))
        rotated_image = pygame.transform.rotate(image, angle)
        
        # Centraliza a rotação no retângulo
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect.topleft)