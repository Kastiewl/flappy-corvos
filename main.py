import sys
import pygame
from src.config import (
    COLOR_BACKGROUND, 
    FPS,
    PIPE_SPAWN_INTERVAL,
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    WINDOW_TITLE,
)
from src.entities.bird import Bird
from src.entities.pipe import Pipe

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
    pipes: list[Pipe] = []
    spawn_timer: float = 0.0

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

        # --- B. Atualização da Lógica e Física ---
        # 1. Atualiza o pássaro
        bird.update(dt)

        # 2. Temporizador de spawn dos canos
        spawn_timer += dt
        if spawn_timer >= PIPE_SPAWN_INTERVAL:
            pipes.append(Pipe())
            spawn_timer = 0.0

        # 3. Atualiza os canos existentes
        for pipe in pipes:
            pipe.update(dt)

        # 4. Descarta canos que já saíram da tela (limpeza de memória)
        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        # --- C. Renderização em camadas ---
        screen.fill(COLOR_BACKGROUND) # 1. Fundo do céu
        for pipe in pipes:            # 2. Canos (verde)
            pipe.draw(screen)

        bird.draw(screen)             # 3. Pássaro (corvo)
        pygame.display.flip()         # 4. Atualiza o display

    # Encerramento limpo dos recursos ao sair do loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()