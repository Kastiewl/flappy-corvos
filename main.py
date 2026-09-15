import sys
import pygame
from src.config import (
    COLOR_BACKGROUND, 
    FPS,
    GameState,
    PIPE_SPAWN_INTERVAL,
    PIPE_WIDTH,
    SCREEN_HEIGHT, 
    SCREEN_WIDTH, 
    WINDOW_TITLE,
)
from src.database import get_high_score, init_db, save_score
from src.entities.bird import Bird
from src.entities.pipe import Pipe

def main() -> None:
    # 1. Inicializa do Pygame e módulo de fontes
    pygame.init()
    pygame.font.init()
    init_db()

    # 2. Configuração da Janela e relógio
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    running = True

    # 3. Fontes tipógraficas
    font_score = pygame.font.SysFont("Arial", 42, bold = True)
    font_title = pygame.font.SysFont("Arial", 36, bold = True)
    font_subtitle = pygame.font.SysFont("Arial", 20)


    # 4. Estado do jogo e entidades
    state = GameState.START
    bird = Bird()
    pipes: list[Pipe] = []
    spawn_timer: float = 0.0
    score: int = 0
    high_score: int = get_high_score()

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
                    if state == GameState.START:
                        state = GameState.PLAYING
                        bird.jump()

                    elif state == GameState.PLAYING:
                        bird.jump()

                    elif state == GameState.GAME_OVER:
                        # Reseta as variáveis e inicia uma nova partida
                        bird.reset()
                        pipes.clear()
                        spawn_timer = 0.0
                        score = 0
                        state = GameState.PLAYING
                        bird.jump()

        # --- B. Atualização da Lógica e Física por estado ---
        # 1. Atualiza o pássaro
        if state == GameState.PLAYING:
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
                save_score(score)
                high_score = get_high_score()
                state = GameState.GAME_OVER

        # --- C. Renderização em camadas ---
        screen.fill(COLOR_BACKGROUND) # Fundo do céu

        # 1. Canos
        for pipe in pipes:            # Canos (verde)
            pipe.draw(screen)

        # 2. Pássaro
        bird.draw(screen)             # Pássaro (corvo)

        # Camada de Interface do Usuário (UI) conforme o Estado
        if state == GameState.START:
            title_surf = font_title.render("FLAPPY RAVEN", True, (255, 215 ,0))
            sub_surf = font_subtitle.render("Pressione ESPAÇO para Iniciar", True, (255,255, 255))
            screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 140)))
            screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 190)))

        elif state == GameState.PLAYING:
            score_surf = font_score.render(str(score), True, (255, 255, 255))
            screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, 45)))

        elif state == GameState.GAME_OVER:
            # Sobreposição translúcida escura sobre a cena congelada
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            over_surf = font_title.render("FIM DE JOGO", True, (255, 75, 75))
            final_score_surf = font_subtitle.render(f"Pontos: {score} | Recorde: {high_score}", True, (255, 255, 255))
            restart_surf = font_subtitle.render("Pressione ESPAÇO para Tentar Novamente", True, (200, 200, 200))

            screen.blit(over_surf, over_surf.get_rect(center=(SCREEN_WIDTH //  2, 130)))
            screen.blit(final_score_surf, final_score_surf.get_rect(center=(SCREEN_WIDTH // 2, 180)))
            screen.blit(restart_surf, restart_surf.get_rect(center=(SCREEN_WIDTH // 2, 220)))
        
        pygame.display.flip()         # 4. Atualiza o display

    # Encerramento limpo dos recursos ao sair do loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()