import sys
import pygame
from src.config import COLOR_BACKGROUND, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE
from src.entities.bird import Bird

def main() -> None:
    # 1. Inicializa do Pygame
    pygame.init()

    # 2. Configuração da Janela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # 3. Relógio e controle de execução
    clock = pygame.time.Clock()
    running = True

    # Inicia a entidade do pássaro antes de rodar o jogo
    bird = Bird()

    # --- Ciclo de vida do Jogo (Game Loop) ---
    while running:
        # Limita o loop a 60 FPS e calcula o tempo do frame em segundos
        dt = clock.tick(FPS) / 1000.0

        # --- A. Processamento de Eventos ---
        for event in pygame.event.get():
            # Se o usuário clicar no 'X' na janela
            if event.type == pygame.QUIT:
                running = False

            # Captura o clique da barra de espaço para pular
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # --- B. Atualização da Lógica ---
        bird.update(dt)

        # --- C. Renderização ---
        screen.fill(COLOR_BACKGROUND)
        bird.draw(screen)
        pygame.display.flip()

    # Encerramento limpo dos recursos ao sair do loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()