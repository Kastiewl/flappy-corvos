import sys
import pygame
from src.config import (
    COLOR_BACKGROUND, 
    FPS,
    PIPE_SPAWN_INTERVAL,
    PIPE_WIDTH,
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    WINDOW_TITLE,
)
from src.entities.bird import Bird
from src.entities.pipe import Pipe

def main() -> None:
    # 1. Inicializa do Pygame e módulo de fontes
    pygame.init()
    pygame.font.init()

    # 2. Configuração da Janela e relógio
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    running = True

    # 3. Fonte para o placar
    font = pygame.font.SysFont("Arial", 36, bold = True)

    # 4. Estado do jogo e entidades
    bird = Bird()
    pipes: list[Pipe] = []
    spawn_timer: float = 0.0
    score: int = 0

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

            # Verificação de pontuação: pássaro passou ou não do cano
            if not pipe.passed and bird.x > pipe.x + PIPE_WIDTH:
                pipe.passed = True
                score += 1

        # 4. Descarta canos que já saíram da tela (limpeza de memória)
        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        # 5. Verificação de colisão (morte do pássaro)
        if bird.check_collision(pipes):
            # Reínicio rápido do estado
            bird.reset()
            pipes.clear()
            spawn_timer = 0.0
            score = 0

        # --- C. Renderização em camadas ---
        screen.fill(COLOR_BACKGROUND) # Fundo do céu

        # 1. Canos
        for pipe in pipes:            # Canos (verde)
            pipe.draw(screen)

        # 2. Pássaro
        bird.draw(screen)             # Pássaro (corvo)

        # 3. Placar (texto renderizado em branco)
        score_surface = font.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(score_surface, score_rect)
        
        pygame.display.flip()         # 4. Atualiza o display

    # Encerramento limpo dos recursos ao sair do loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()