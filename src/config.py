from enum import Enum, auto

class GameState(Enum):
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()

# Dimensões da tela do jogo (em pixels)
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 450

# Taxa de quadros por segundo alvo
FPS: int = 60

# Título da janela do jogo
WINDOW_TITLE: str = "Flappy Raven"

# Cores padrão RGB (RGB: Red, Green, Blue de 0 a 255)
# Tom noturno de azul escuro (placeholder para a paleta da arte)
COLOR_BACKGROUND: tuple[int, int, int] = (16, 20, 48)
COLOR_BIRD: tuple[int, int, int] = (45, 45, 55)          # Corvo (chumbo escuro)
COLOR_PIPE: tuple[int, int, int] = (50, 160, 65)         # Verde clássico

# --- Constantes do Pássaro ---
BIRD_WIDTH: int = 36
BIRD_HEIGHT: int = 26
BIRD_START_X: float = 120.0
BIRD_START_Y: float = 180.0

# Física (valores calibrados em pixels por segundo)
GRAVITY: float = 850.0        # Acelereção vertical
JUMP_VELOCITY: float = -280.0 # Impulso moderado para evitar bater no teto facilmente

# Constantes dos Canos
PIPE_WIDTH: int = 64 
PIPE_GAP: int = 125 # Espaço vertical livre para o pássaro passar 
PIPE_SPEED: float = 170.0 # Velocidade de deslocamento para a esquerda (px/s)
PIPE_SPAWN_INTERVAL: float = 1.9 # Intervalo de spawn em segundos
PIPE_MIN_HEIGHT: int = 50 # Altura mínima para o cano superior/inferior