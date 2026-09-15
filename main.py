import sys
import pygame
from src.config import COLOR_BACKGROUND, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE

def main() -> None:
    # 1. Inicializa todos os módulos do Pygame
    pygame.init()

    # 2. Cria a superfície da janela e define o título
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # 3. Cria o relógio para controle de FPS e cálculo de delta time
    clock = pygame.time.Clock()
    running = True

    # --- Ciclo de vida do Jogo (Game Loop) ---
    while running:
        # Limita o loop a 60 FPS e calcula o tempo do frame em segundos
        dt = clock.tick(FPS) / 1000.0

        # --- A. Processamento de Eventos ---
        for event in pygame.event.get():
            # Se o usuário clicar no 'X' na janela
            if event.type == pygame.QUIT:
                running = False

        # --- B. Atualização da Lógica ---
        # (Aqui entrará a física do pássaro e dos canos nos próximos passos)

        # --- C. Renderização ---
        screen.fill(COLOR_BACKGROUND)
        pygame.display.flip()

    # Encerramento limpo dos recursos ao sair do loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()