import os
import random
import pygame
import numpy as np
import imageio

from game.game_engine import GameEngine
from game.bullet import Bullet

def generate_video(output_path="before_gameplay_bug.mp4", duration_seconds=10, fps=30):
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.font.init()

    WIDTH, HEIGHT = 600, 700
    screen = pygame.Surface((WIDTH, HEIGHT))
    engine = GameEngine(WIDTH, HEIGHT)
    engine.enemy_fire_chance = 0.001

    total_frames = duration_seconds * fps
    writer = imageio.get_writer(output_path, fps=fps, macro_block_size=1)

    font_annotate = pygame.font.SysFont("Arial", 18, bold=True)
    font_title = pygame.font.SysFont("Arial", 20, bold=True)

    # Automated script sequence
    # 0s - 2s: Normal movement and 1 successful hit
    # 3s - 5s: Rapid fire, demonstrate bullet skipping collision and passing through
    # 6s - 8s: Repeat demonstration on another column
    # 8s - 10s: Continued play showing enemy march

    simulated_keys = set()
    bug_highlight_timer = 0
    highlight_rect = None

    for frame in range(total_frames):
        current_time = frame / fps

        # AI Player movement control
        target_x = 220
        if current_time < 3.0:
            target_x = 100 + int(current_time * 50)
        elif current_time < 6.0:
            target_x = 260
        else:
            target_x = 350 - int((current_time - 6.0) * 40)

        # Move player towards target_x
        if engine.player.x < target_x - 3:
            engine.player.move(engine.player.speed, WIDTH)
        elif engine.player.x > target_x + 3:
            engine.player.move(-engine.player.speed, WIDTH)

        # Firing logic
        if frame == 15 or frame == 45:
            # Normal shots
            b_x = engine.player.center_x() - 2
            engine.player_bullets.append(Bullet(b_x, engine.player.y, direction=-1))

        elif frame == 85:
            # Trigger Bug 1: Rapid fire 2 bullets aligned so one skips collision
            # Find an alive column
            cols = {}
            for e in engine.enemy_grid.alive_enemies():
                cols.setdefault(round(e.x), []).append(e)
            
            # Pick a column near player
            if cols:
                best_x = min(cols.keys(), key=lambda x: abs(x - engine.player.x))
                col_enemies = sorted(cols[best_x], key=lambda e: e.y)
                if len(col_enemies) >= 2:
                    e_top = col_enemies[0]
                    e_bot = col_enemies[-1]
                    # Align player with this column
                    engine.player.x = best_x + 5
                    # Fire bot bullet hitting bot enemy
                    b1 = Bullet(best_x + 15, e_bot.y + 12, direction=-1)
                    # Fire top bullet overlapping top few px of e_top (so moving 8px skips it entirely!)
                    b2 = Bullet(best_x + 15, e_top.y - 4, direction=-1)
                    engine.player_bullets.extend([b1, b2])
                    bug_highlight_timer = 45
                    highlight_rect = e_top.rect()

        elif frame == 170:
            # Trigger Bug 2: Second occurrence
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

        # Update game state using the buggy collision logic in engine
        screen.fill((0, 0, 0))
        engine.update()
        engine.render(screen)

        # Overlay bug indication banner and callout
        if bug_highlight_timer > 0:
            bug_highlight_timer -= 1
            if highlight_rect:
                pygame.draw.rect(screen, (255, 60, 60), highlight_rect.inflate(10, 10), 2)
            
            # Onscreen caption
            banner_bg = pygame.Rect(10, HEIGHT - 45, WIDTH - 20, 35)
            pygame.draw.rect(screen, (40, 0, 0), banner_bg)
            pygame.draw.rect(screen, (255, 60, 60), banner_bg, 1)
            msg = font_annotate.render("BUG: Bullet skipped collision and passed through enemy!", True, (255, 100, 100))
            screen.blit(msg, (banner_bg.x + 10, banner_bg.y + 8))

        # Title bar banner at top right
        tag = font_title.render("BEFORE FIX - BUGGY GAMEPLAY", True, (255, 180, 0))
        screen.blit(tag, (WIDTH - tag.get_width() - 15, 12))

        # Convert surface to RGB array for video writer
        frame_arr = np.transpose(pygame.surfarray.array3d(screen), (1, 0, 2))
        writer.append_data(frame_arr)

    writer.close()
    pygame.quit()
    print(f"Generated video: {output_path} ({duration_seconds}s @ {fps}fps)")

if __name__ == "__main__":
    generate_video()
