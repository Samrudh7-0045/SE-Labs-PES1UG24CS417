import os
import pygame
import numpy as np
import imageio

from game.game_engine import GameEngine
from game.bullet import Bullet

def generate_after_video(output_path="after_gameplay_working.mp4", duration_seconds=10, fps=30):
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.font.init()

    WIDTH, HEIGHT = 600, 700
    screen = pygame.Surface((WIDTH, HEIGHT))
    engine = GameEngine(WIDTH, HEIGHT)
    engine.current_difficulty = "Medium"

    total_frames = duration_seconds * fps
    writer = imageio.get_writer(output_path, fps=fps, macro_block_size=1)

    font_banner = pygame.font.SysFont("Arial", 18, bold=True)
    font_title = pygame.font.SysFont("Arial", 20, bold=True)

    # 10s Script:
    # 0s - 4s: Smooth player movement, rapid-firing into enemies, all collisions register cleanly (Task 1 Fixed!)
    # 4s - 6s: HUD displays Score and Difficulty (Task 3 HUD)
    # 6.5s: Enemy bullet collides with player -> Triggers Graphical Game Over Screen (Task 2)
    # 8.5s: Player selects [1] Easy -> Replays with Easy difficulty (Task 3 Replay & Difficulty)
    # 8.5s - 10s: Fresh round running on Easy!

    for frame in range(total_frames):
        current_time = frame / fps

        # Phase 1: 0s - 6s (Active gameplay with clean collision)
        if current_time < 6.0:
            target_x = 120 + int(current_time * 65)
            if engine.player.x < target_x - 3:
                engine.player.move(engine.player.speed, WIDTH)
            elif engine.player.x > target_x + 3:
                engine.player.move(-engine.player.speed, WIDTH)

            # Rapid fire every 15 frames
            if frame % 15 == 0 and frame < 160:
                b_x = engine.player.center_x() - 2
                engine.player_bullets.append(Bullet(b_x, engine.player.y, direction=-1))

        # Phase 2: At frame 185 (~6.2s), intentionally spawn an enemy bullet that hits player to show Game Over
        elif frame == 185:
            # Spawn bullet right above player
            engine.enemy_bullets.append(Bullet(engine.player.center_x(), engine.player.y - 10, direction=1))

        # Phase 3: At frame 250 (~8.3s), trigger Replay on Easy
        elif frame == 250:
            engine.reset_game("Easy")

        # Phase 4: 8.3s - 10s (New game running on Easy)
        elif current_time >= 8.4:
            target_x = 200 + int((current_time - 8.4) * 80)
            if engine.player.x < target_x - 3:
                engine.player.move(engine.player.speed, WIDTH)
            if frame % 20 == 0:
                engine.player_bullets.append(Bullet(engine.player.center_x() - 2, engine.player.y, direction=-1))

        screen.fill((0, 0, 0))
        engine.update()
        engine.render(screen)

        # Title badge
        tag = font_title.render("AFTER FIX - FULL FUNCTIONALITY", True, (0, 220, 100))
        screen.blit(tag, (WIDTH - tag.get_width() - 15, HEIGHT - 30))

        # Annotations based on current phase
        if current_time < 5.8:
            banner_bg = pygame.Rect(10, HEIGHT - 40, 360, 30)
            pygame.draw.rect(screen, (0, 40, 20), banner_bg)
            pygame.draw.rect(screen, (0, 200, 100), banner_bg, 1)
            msg = font_banner.render("All collisions register accurately!", True, (150, 255, 180))
            screen.blit(msg, (banner_bg.x + 8, banner_bg.y + 5))
        elif 6.0 <= current_time < 8.3:
            banner_bg = pygame.Rect(10, 10, 320, 30)
            pygame.draw.rect(screen, (40, 10, 10), banner_bg)
            pygame.draw.rect(screen, (255, 80, 80), banner_bg, 1)
            msg = font_banner.render("Graphical Game Over + Difficulty Menu", True, (255, 180, 180))
            screen.blit(msg, (banner_bg.x + 8, banner_bg.y + 5))
        elif current_time >= 8.4:
            banner_bg = pygame.Rect(10, HEIGHT - 40, 360, 30)
            pygame.draw.rect(screen, (0, 40, 20), banner_bg)
            pygame.draw.rect(screen, (0, 200, 100), banner_bg, 1)
            msg = font_banner.render("Replay: New match started on Easy!", True, (150, 255, 180))
            screen.blit(msg, (banner_bg.x + 8, banner_bg.y + 5))

        frame_arr = np.transpose(pygame.surfarray.array3d(screen), (1, 0, 2))
        writer.append_data(frame_arr)

    writer.close()
    pygame.quit()
    print(f"Generated after video: {output_path} ({duration_seconds}s @ {fps}fps)")

if __name__ == "__main__":
    generate_after_video()
