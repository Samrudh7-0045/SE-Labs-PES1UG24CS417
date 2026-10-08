import pygame
from game.game_engine import GameEngine
from game.bullet import Bullet

def run_interactive_simulation():
    pygame.init()
    pygame.font.init()

    WIDTH, HEIGHT = 600, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Invaders - Bug Demonstration (10s)")

    clock = pygame.time.Clock()
    FPS = 30
    total_frames = 10 * FPS

    engine = GameEngine(WIDTH, HEIGHT)
    engine.enemy_fire_chance = 0.001

    font_annotate = pygame.font.SysFont("Arial", 18, bold=True)
    font_title = pygame.font.SysFont("Arial", 20, bold=True)

    bug_highlight_timer = 0
    highlight_rect = None

    running = True
    frame = 0

    while running and frame < total_frames:
        clock.tick(FPS)
        current_time = frame / FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Autonomous movement
        target_x = 220
        if current_time < 3.0:
            target_x = 100 + int(current_time * 50)
        elif current_time < 6.0:
            target_x = 260
        else:
            target_x = 350 - int((current_time - 6.0) * 40)

        if engine.player.x < target_x - 3:
            engine.player.move(engine.player.speed, WIDTH)
        elif engine.player.x > target_x + 3:
            engine.player.move(-engine.player.speed, WIDTH)

        # Firing logic
        if frame == 15 or frame == 45:
            b_x = engine.player.center_x() - 2
            engine.player_bullets.append(Bullet(b_x, engine.player.y, direction=-1))

        elif frame == 85 or frame == 170:
            cols = {}
            for e in engine.enemy_grid.alive_enemies():
                cols.setdefault(round(e.x), []).append(e)
            if cols:
                best_x = min(cols.keys(), key=lambda x: abs(x - engine.player.x))
                col_enemies = sorted(cols[best_x], key=lambda e: e.y)
                if len(col_enemies) >= 2:
                    e_top = col_enemies[0]
                    e_bot = col_enemies[-1]
                    engine.player.x = best_x + 5
                    b1 = Bullet(best_x + 15, e_bot.y + 12, direction=-1)
                    b2 = Bullet(best_x + 15, e_top.y - 4, direction=-1)
                    engine.player_bullets.extend([b1, b2])
                    bug_highlight_timer = 45
                    highlight_rect = e_top.rect()

        screen.fill((0, 0, 0))
        engine.update()
        engine.render(screen)

        if bug_highlight_timer > 0:
            bug_highlight_timer -= 1
            if highlight_rect:
                pygame.draw.rect(screen, (255, 60, 60), highlight_rect.inflate(10, 10), 2)
            banner_bg = pygame.Rect(10, HEIGHT - 45, WIDTH - 20, 35)
            pygame.draw.rect(screen, (40, 0, 0), banner_bg)
            pygame.draw.rect(screen, (255, 60, 60), banner_bg, 1)
            msg = font_annotate.render("BUG: Bullet skipped collision and passed through enemy!", True, (255, 100, 100))
            screen.blit(msg, (banner_bg.x + 10, banner_bg.y + 8))

        tag = font_title.render("BEFORE FIX - BUGGY GAMEPLAY", True, (255, 180, 0))
        screen.blit(tag, (WIDTH - tag.get_width() - 15, 12))

        pygame.display.flip()
        frame += 1

    pygame.quit()

if __name__ == "__main__":
    run_interactive_simulation()
