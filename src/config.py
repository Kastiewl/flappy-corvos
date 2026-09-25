from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    DIFFICULTY_SELECT = auto()
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    RANKING = auto()


class Difficulty(Enum):
    FACIL = "Fácil"
    MEDIO = "Médio"
    DIFICIL = "Díficil"


# Dimensões da tela do jogo (em pixels)
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 450

# Taxa de quadros por segundo alvo
FPS: int = 60

# Título da janela do jogo
WINDOW_TITLE: str = "Flappy Raven"

# Paleta de cores RGB (Interface)
COLOR_BACKGROUND: tuple[int, int, int] = (16, 20, 48)
COLOR_WHITE: tuple [int, int, int] = (255, 255, 255)
COLOR_GOLD: tuple [int, int, int] = (255, 215, 0)
COLOR_GRAY: tuple [int, int, int] = (180, 180, 180)
COLOR_RED: tuple [int, int, int] = (255, 75, 75)

# --- Constantes do Pássaro ---
BIRD_WIDTH: int = 36
BIRD_HEIGHT: int = 26
BIRD_START_X: float = 120.0
BIRD_START_Y: float = 180.0
GRAVITY: float = 850.0           # Acelereção vertical
JUMP_VELOCITY: float = -280.0    # Impulso moderado para evitar bater no teto facilmente

# Constantes dos Canos
PIPE_WIDTH: int = 64
PIPE_MIN_HEIGHT: int = 50

# Configurações Calibradas por Dificuldade
DIFFICULTY_SETTINGS: dict[Difficulty, dict[str, float]] = {
    Difficulty.FACIL: {
        "speed": 150.0,
        "gap": 135.0,
        "interval": 2.0,
    },
    Difficulty.MEDIO: {
        "speed": 190.0,
        "gap": 115.0,
        "interval": 1.65,
    },
    Difficulty.DIFICIL: {
        "speed": 235.0,
        "gap": 96.0,
        "interval": 1.35,
    },
}