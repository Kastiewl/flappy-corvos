# Dimensões da tela do jogo (em pixels)
SCREEN_WIDTH: int = 400
SCREEN_HEIGHT: int = 600

# Taxa de quadros por segundo alvo
FPS: int = 60

# Título da janela do jogo
WINDOW_TITLE: str = "Flappy Corvos"

# Cor de fundo padrão (RGB: Red, Green, Blue de 0 a 255)
# (135, 206, 235) gera um to de azul celeste (placeholder do céu)
COLOR_BACKGROUND: tuple[int, int, int] = (135, 206, 235) # Azul celetes
COLOR_BIRD: tuple[int, int, int] = (30, 30, 30)          # Preto chumbo

# --- Constantes do Pássaro ---
BIRD_WIDTH: int = 34
BIRD_HEIGHT: int = 24
BIRD_START_X: float = 80.0
BIRD_START_Y: float = 200.0

# Física (valores calibrados em pixels por segundo)
GRAVITY: float = 900.0 # Aceleração para baixo
JUMP_VELOCITY: float = -320.0 # Impulso para cima (negativo sobe na tela)