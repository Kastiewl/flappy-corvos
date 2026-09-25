from pathlib import Path
import sys
import urllib.request
import pygame
from src.audio import SoundManager
from src.config import (
    COLOR_BACKGROUND,
    COLOR_GOLD,
    COLOR_GRAY,
    COLOR_RED,
    COLOR_WHITE,
    DIFFICULTY_SETTINGS,
    FPS,
    Difficulty,
    GameState,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WINDOW_TITLE,
)
from src.database import get_high_score, get_top_scores, init_db, save_score
from src.entities.bird import Bird
from src.entities.pipe import Pipe

# Gestão de caminhos e ficheiros
base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)
ROOT_DIR = Path(base_path)

FONTS_DIR = ROOT_DIR / "fonts"
FONT_PATH = FONTS_DIR / "PressStart2P-Regular.ttf"

# Caminho absoluto para a diretoria dos cenários
PARALLAX_DIR = (
    Path(__file__).resolve().parent
    / "sprites"
    / "background city"
)


def ensure_font_exists() -> Path | None:
    """Garante que a fonte Press Start 2P existe localmente ou descarrega-a"""
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    alt_font_path = FONTS_DIR / "press_start_2p.ttf"

    if FONT_PATH.exists():
        return FONT_PATH
    if alt_font_path.exists():
        return alt_font_path

    # Tenta baixar automaticamente da fonte oficial
    url = "https://github.com/google/fonts/raw/main/ofl/pressstart2p/PressStart2P-Regular.ttf"
    try:
        urllib.request.urlretrieve(url, FONT_PATH)
        return FONT_PATH
    except Exception:
        return None
    

def load_fonts(font_file: Path | None) -> tuple[dict[str, pygame.font.Font], bool]:
    """Carrega as instâncias de fontes em tamanhos pixel art calibrados."""
    if font_file and font_file.exists():
        return {
            "title": pygame.font.Font(str(font_file), 24),
            "subtitle": pygame.font.Font(str(font_file), 10),
            "menu": pygame.font.Font(str(font_file), 13),
            "score": pygame.font.Font(str(font_file), 30),
            "footer": pygame.font.Font(str(font_file), 9),
        }, True

    # Fallback de segurança utilizando tipografia de sistema
    return {
        "title": pygame.font.SysFont("Arial", 36, bold=True),
        "subtitle": pygame.font.SysFont("Arial", 18, bold=True),
        "menu": pygame.font.SysFont("Arial", 22, bold=True),
        "score": pygame.font.SysFont("Arial", 42, bold=True),
        "footer": pygame.font.SysFont("Arial", 16),
    }, False


def draw_text_with_outline(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    center_pos: tuple[int, int],
    is_pixel: bool = True,
    outline_color: tuple[int, int, int] = (0, 0, 0),
    thickness: int = 2,
) -> None:
    """Desenha texto com contorno preto nítido para realce em pixel art."""
    x, y = center_pos
    antialias = not is_pixel

    # Desenha as bordas periféricas em redor do centro
    offsets = [
        (-thickness, 0), (thickness, 0), (0, -thickness), (0, thickness),
        (-thickness, -thickness), (thickness, thickness),
        (-thickness, thickness), (thickness, -thickness)
    ]
    for dx, dy in offsets:
        outline_surf = font.render(text, antialias, outline_color)
        surface.blit(outline_surf, outline_surf.get_rect(center=(x + dx, y + dy)))

    # Desenha o texto principal por cima
    main_surf = font.render(text, antialias, color)
    surface.blit(main_surf, main_surf.get_rect(center=(x, y)))


def load_parallax_layers() -> list[pygame.Surface]:
    """Carrega e escala todas as camadas de parallax em memória."""
    layer_files = [
        "sky.png", "shade2.png", "shade1.png",
        "buildings4.png", "buildings3.png",
        "buildings2.png", "buildings1.png"
    ]
    layers: list[pygame.Surface] = []
    for file_name in layer_files:
        file_path = PARALLAX_DIR / file_name
        if file_path.exists():
            img = pygame.image.load(str(file_path)).convert_alpha()
            img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            layers.append(img)
        else:
            # Fallback seguro caso algum ficheiro não seja localizado
            fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            layers.append(fallback)
    return layers


def main() -> None:
    # Inicialização do jogo
    pygame.init()
    pygame.font.init()
    init_db()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    running = True

    audio = SoundManager()

    # Fontes tipógraficas
    font_file = ensure_font_exists()
    fonts, is_pixel = load_fonts(font_file)

    # Estado do jogo e Navegação de Menus
    state = GameState.MENU
    current_difficulty = Difficulty.MEDIO

    menu_options = ["Jogar", "Dificuldade", "Ranking", "Sair"]
    menu_selected_index = 0

    difficulty_options = [Difficulty.FACIL, Difficulty.MEDIO, Difficulty.DIFICIL]
    diff_selected_index = 1

    # Entidades e Variáveis da Partida
    bird = Bird()
    pipes: list[Pipe] = []
    spawn_timer: float = 0.0
    score: int = 0
    high_score: int = get_high_score()
    
    # Configuração do Parallax
    bg_layers = load_parallax_layers()
    bg_scroll = [0.0] * len(bg_layers)
    bg_speeds = [6.0, 10.0, 16.0, 22.0, 30.0, 40.0, 52.0]

    # Game Loop Principal
    while running:
        dt = clock.tick(FPS) / 1000.0

        # Tratamento de eventos por estado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            
            elif event.type == pygame.KEYDOWN:
                # Menu Principal
                if state == GameState.MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        menu_selected_index = (menu_selected_index - 1) % len(menu_options)
                        audio.play("swoosh")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selected_index = (menu_selected_index + 1) % len(menu_options)
                        audio.play("swoosh")
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        action = menu_options[menu_selected_index]
                        if action == "Jogar":
                            bird.reset()
                            pipes.clear()
                            spawn_timer = 0.0
                            score = 0
                            state = GameState.PLAYING
                            bird.jump()
                            audio.play("wing")
                        elif action == "Dificuldade":
                            audio.play("swoosh")
                            state = GameState.DIFFICULTY_SELECT
                        elif action == "Ranking":
                            audio.play("swoosh")
                            state = GameState.RANKING
                        elif action == "Sair":
                            running = False

                # Menu de Dificuldade
                elif state == GameState.DIFFICULTY_SELECT:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        diff_selected_index = (diff_selected_index - 1) % len(difficulty_options)
                        audio.play("swoosh")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        diff_selected_index = (diff_selected_index + 1) % len(difficulty_options)
                        audio.play("swoosh")
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        current_difficulty = difficulty_options[diff_selected_index]
                        audio.play("swoosh")
                        state = GameState.MENU
                    elif event.key == pygame.K_ESCAPE:
                        audio.play("swoosh")
                        state = GameState.MENU

                # Ecrã de Ranking
                elif state == GameState.RANKING:
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                        audio.play("swoosh")
                        state = GameState.MENU

                # Partida Ativa
                elif state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                        audio.play("wing")
                    elif event.key == pygame.K_ESCAPE:
                        state = GameState.MENU

                # Fim de Jogo
                elif state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        bird.reset()
                        pipes.clear()
                        spawn_timer = 0.0
                        score = 0
                        state = GameState.PLAYING
                        bird.jump()
                        audio.play("wing")
                    elif event.key == pygame.K_ESCAPE:
                        state = GameState.MENU

        # Atualização da Física e Movimento
        # O parallax move-se durante a partida e com velocidade reduzida pelo menu
        is_playing = (state == GameState.PLAYING)
        parallax_speed_mult = 1.0 if is_playing else 0.35

        for i in range(len(bg_scroll)):
            bg_scroll[i] -= bg_speeds[i] * parallax_speed_mult * dt
            if bg_scroll[i] <= -SCREEN_WIDTH:
                bg_scroll[i] += SCREEN_WIDTH

        if is_playing:
            bird.update(dt)

            # Obtenção dos parâmetros da dificuldade selecionada
            settings = DIFFICULTY_SETTINGS[current_difficulty]
            speed = settings["speed"]
            gap = settings["gap"]
            interval = settings["interval"]

            # Criação de canos respeitando a dificuldade ativa
            spawn_timer += dt
            if spawn_timer >= interval:
                pipes.append(Pipe(gap=gap, speed=speed))
                spawn_timer = 0.0

            for pipe in pipes:
                pipe.update(dt)
                if not pipe.passed and bird.x > pipe.x + PIPE_WIDTH:
                    pipe.passed = True
                    score += 1
                    audio.play("point")

            pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

            if bird.check_collision(pipes):
                audio.play("hit")
                audio.play("die")
                save_score(score)
                high_score = get_high_score()
                state = GameState.GAME_OVER

        # Renderização em camadas
        screen.fill(COLOR_BACKGROUND)

        # Camadas do Parallax (desenhadas duas vezes para o loop horizontal contínuo)
        for i, img in enumerate(bg_layers):
            x_pos = int(bg_scroll[i])
            screen.blit(img, (x_pos, 0))
            screen.blit(img, (x_pos + SCREEN_WIDTH, 0))
            screen.blit(img, (x_pos + SCREEN_WIDTH * 2, 0))

        # Renderização por Estado
        if state == GameState.MENU:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            draw_text_with_outline(screen, "FLAPPY RAVEN", fonts["title"], COLOR_GOLD, (SCREEN_WIDTH // 2, 75), is_pixel=is_pixel)
            draw_text_with_outline(screen, f"Dificuldade Atual: {current_difficulty.value}", fonts["subtitle"], COLOR_GRAY, (SCREEN_WIDTH // 2, 120), is_pixel= is_pixel, thickness=1)

            for i, opt in enumerate(menu_options):
                is_selected = (i == menu_selected_index)
                color = COLOR_GOLD if is_selected else COLOR_WHITE
                prefix = "> " if is_selected else "  "
                draw_text_with_outline(screen, f"{prefix}{opt}", fonts["menu"], color, (SCREEN_WIDTH // 2, 175 + i * 42), is_pixel=is_pixel)

            draw_text_with_outline(screen, "      SETAS para navegar  |  ENTER para selecionar", fonts["footer"], COLOR_GRAY, (SCREEN_WIDTH // 2, 400), is_pixel=is_pixel, thickness=1)

        elif state == GameState.DIFFICULTY_SELECT:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            draw_text_with_outline(screen, "SELECIONE A DIFICULDADE", fonts["title"], COLOR_GOLD, (SCREEN_WIDTH // 2, 80), is_pixel=is_pixel)

            for i, diff in enumerate(difficulty_options):
                is_selected = (i == diff_selected_index)
                color = COLOR_GOLD if is_selected else COLOR_WHITE
                prefix = "> " if is_selected else "  "
                draw_text_with_outline(screen, f"{prefix}{diff.value}", fonts["menu"], color, (SCREEN_WIDTH // 2, 180 + i * 50), is_pixel=is_pixel)

            draw_text_with_outline(screen, "      Enter para confirmar  |  ESC para voltar ao menu", fonts["footer"], COLOR_GRAY, (SCREEN_WIDTH // 2, 400), is_pixel=is_pixel, thickness=1)

        elif state == GameState.RANKING:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0,0))

            draw_text_with_outline(screen, "TOP 5 RECORDES", fonts["title"], COLOR_GOLD, (SCREEN_WIDTH // 2, 75), is_pixel=is_pixel)

            top_scores = get_top_scores(5)
            if not top_scores:
                draw_text_with_outline(screen, "Nenhuma pontuação registrada.", fonts["subtitle"], COLOR_GRAY, (SCREEN_WIDTH // 2, 220), is_pixel=is_pixel)
            else:
                for i, s in enumerate(top_scores):
                    pos_text = f"#{i + 1}"
                    score_text = f"{pos_text:>4} ........................ {s:>3} pts"
                    color = COLOR_GOLD if i == 0 else COLOR_WHITE
                    draw_text_with_outline(screen, score_text, fonts["menu"], color, (SCREEN_WIDTH // 2, 160 + i * 38), is_pixel=is_pixel)

            draw_text_with_outline(screen, "Pressione ESC ou ESPAÇO para voltar", fonts["footer"], COLOR_GRAY, (SCREEN_WIDTH // 2, 400), is_pixel=is_pixel, thickness=1)
            
        elif state == GameState.PLAYING:
            for pipe in pipes:
               pipe.draw(screen)
            bird.draw(screen)

            draw_text_with_outline(screen, str(score), fonts["score"], COLOR_WHITE, (SCREEN_WIDTH // 2, 45), is_pixel=is_pixel, thickness=3)
            
        elif state == GameState.GAME_OVER:
            for pipe in pipes:
                pipe.draw(screen)
            bird.draw(screen)

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))

            draw_text_with_outline(screen, "FIM DE JOGO", fonts["title"], COLOR_RED, (SCREEN_WIDTH // 2, 130), is_pixel=is_pixel, thickness=3)
            draw_text_with_outline(screen, f"Pontos: {score}  |  Recorde: {high_score}", fonts["subtitle"], COLOR_WHITE, (SCREEN_WIDTH // 2, 190), is_pixel=is_pixel)
            draw_text_with_outline(screen, "ESPAÇO: Tentar Novamente  |  ESC: Menu Principal", fonts["footer"], COLOR_GRAY, (SCREEN_WIDTH // 2, 240), is_pixel=is_pixel, thickness=1)

        pygame.display.flip()  

    # Encerramento limpo dos recursos ao sair do loop
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()