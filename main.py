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
    pygame.init()
    pygame.font.init()
    init_db()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    running = True

    font_score = pygame.font.SysFont("Arial", 42, bold=True)
    font_title = pygame.font.SysFont("Arial", 36, bold=True)
    font_subtitle = pygame.font.SysFont("Arial", 20)

    state = GameState.START
    bird = Bird()
    pipes: list[Pipe] = []
    spawn_timer: float = 0.0
    score: int = 0
    high_score: int = get_high_score()

    #chamando as layers do paralax 
    layer_files = [
        "Sky.png", "Shade 3.png", "Shade 2.png",
        "Buildings 4.png", "Buildings 3.png", 
        "Buildings 2.png", "Buildings 1.png"
    ]
    bg_layers = []
    for file_name in layer_files:
        img = pygame.image.load(f"sprites/Pixel Art - City Landscape V2/{file_name}").convert_alpha()
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_layers.append(img)
    
    # Definindo a velocidade do fundo e dos predios das frente
    bg_scroll = [0.0] * len(bg_layers)
    bg_speeds = [5.0, 15.0, 25.0, 35.0, 45.0, 60.0, 80.0] 

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if state == GameState.START:
                        state = GameState.PLAYING
                        bird.jump()
                    elif state == GameState.PLAYING:
                        bird.jump()
                    elif state == GameState.GAME_OVER:
                        bird.reset()
                        pipes.clear()
                        spawn_timer = 0.0
                        score = 0
                        state = GameState.PLAYING
                        bird.jump()

        if state == GameState.PLAYING:
            bird.update(dt)
            
            # Atualiza o parallax
            for i in range(len(bg_scroll)):
                bg_scroll[i] -= bg_speeds[i] * dt
                if bg_scroll[i] <= -SCREEN_WIDTH:
                    bg_scroll[i] = 0.0

            spawn_timer += dt
            if spawn_timer >= PIPE_SPAWN_INTERVAL:
                pipes.append(Pipe())
                spawn_timer = 0.0

            for pipe in pipes:
                pipe.update(dt)
                if not pipe.passed and bird.x > pipe.x + PIPE_WIDTH:
                    pipe.passed = True
                    score += 1

            pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

            if bird.check_collision(pipes):
                save_score(score)
                high_score = get_high_score()
                state = GameState.GAME_OVER

        # --- Renderização ---
        screen.fill(COLOR_BACKGROUND) 

        # Desenha as camadas do background duas vezes para criar o loop contínuo da imagem
        for i, img in enumerate(bg_layers):
            screen.blit(img, (int(bg_scroll[i]), 0))
            screen.blit(img, (int(bg_scroll[i]) + SCREEN_WIDTH, 0))

        for pipe in pipes:
            pipe.draw(screen)
            
        bird.draw(screen)

        if state == GameState.START:
            title_surf = font_title.render("FLAPPY RAVEN", True, (255, 215 ,0))
            sub_surf = font_subtitle.render("Pressione ESPAÇO para Iniciar", True, (255,255, 255))
            screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 140)))
            screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH // 2, 190)))
            
        elif state == GameState.PLAYING:
            score_surf = font_score.render(str(score), True, (255, 255, 255))
            screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, 45)))
            
        elif state == GameState.GAME_OVER:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            over_surf = font_title.render("FIM DE JOGO", True, (255, 75, 75))
            final_score_surf = font_subtitle.render(f"Pontos: {score} | Recorde: {high_score}", True, (255, 255, 255))
            restart_surf = font_subtitle.render("Pressione ESPAÇO para Tentar Novamente", True, (200, 200, 200))
            screen.blit(over_surf, over_surf.get_rect(center=(SCREEN_WIDTH //  2, 130)))
            screen.blit(final_score_surf, final_score_surf.get_rect(center=(SCREEN_WIDTH // 2, 180)))
            screen.blit(restart_surf, restart_surf.get_rect(center=(SCREEN_WIDTH // 2, 220)))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()