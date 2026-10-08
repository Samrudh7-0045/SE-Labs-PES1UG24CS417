import pygame
import random
from .player import Player
from .enemy import EnemyGrid
from .bullet import Bullet
from .sound import SoundManager

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)


class GameEngine:
    DIFFICULTIES = {
        "Easy": {
            "enemy_speed": 1.0,
            "fire_chance": 0.001,
            "color": (100, 220, 100),
        },
        "Medium": {
            "enemy_speed": 1.6,
            "fire_chance": 0.003,
            "color": (240, 200, 60),
        },
        "Hard": {
            "enemy_speed": 2.5,
            "fire_chance": 0.007,
            "color": (255, 80, 80),
        },
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.current_difficulty = "Medium"
        diff_cfg = self.DIFFICULTIES[self.current_difficulty]

        self.player = Player(width // 2 - 20, height - 50, 40, 20)
        self.enemy_grid = EnemyGrid(width, speed=diff_cfg["enemy_speed"])

        self.player_bullets = []
        self.enemy_bullets = []

        self._shoot_cooldown = 0
        self.enemy_fire_chance = diff_cfg["fire_chance"]

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.sub_font = pygame.font.SysFont("Arial", 22)
        self.game_over = False
        self.victory = False
        self.sound_manager = SoundManager()

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key in (pygame.K_1, pygame.K_e):
                    self.reset_game("Easy")
                elif event.key in (pygame.K_2, pygame.K_m):
                    self.reset_game("Medium")
                elif event.key in (pygame.K_3, pygame.K_h):
                    self.reset_game("Hard")
                elif event.key == pygame.K_r:
                    self.reset_game(self.current_difficulty)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self._shoot_cooldown <= 0:
                bullet_x = self.player.center_x() - 2
                self.player_bullets.append(
                    Bullet(bullet_x, self.player.y, direction=-1)
                )
                self.sound_manager.play_shoot()
                self._shoot_cooldown = 15

    def handle_input(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-self.player.speed, self.width)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(self.player.speed, self.width)

    def update(self):
        if self.game_over:
            return

        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

        # Move enemies
        self.enemy_grid.move()

        # Enemies randomly fire bullets
        for enemy in self.enemy_grid.alive_enemies():
            if random.random() < self.enemy_fire_chance:
                bullet_x = enemy.x + enemy.width // 2

                self.enemy_bullets.append(
                    Bullet(
                        bullet_x,
                        enemy.y + enemy.height,
                        direction=1
                    )
                )

        # Move player bullets
        for bullet in self.player_bullets:
            bullet.move()

        # Move enemy bullets
        for bullet in self.enemy_bullets:
            bullet.move()

        # Remove bullets that leave the screen
        self.player_bullets = [
            b for b in self.player_bullets
            if not b.off_screen(self.height)
        ]

        self.enemy_bullets = [
            b for b in self.enemy_bullets
            if not b.off_screen(self.height)
        ]

        # ---------------------------------------------------------
        # TASK 1: FIX BULLET COLLISION
        # ---------------------------------------------------------
        # Iterate over a copy of the bullet list so that removing
        # a bullet does not cause the next bullet to be skipped.
        for bullet in self.player_bullets[:]:
            for enemy in self.enemy_grid.alive_enemies():

                if bullet.rect().colliderect(enemy.rect()):
                    enemy.alive = False
                    self.player_bullets.remove(bullet)
                    self.score += 1
                    self.sound_manager.play_enemy_hit()
                    break

        # Enemy bullet hits player
        for bullet in self.enemy_bullets:
            if bullet.rect().colliderect(self.player.rect()):
                self.trigger_game_over(victory=False)
                break

        # Enemies reached the player
        if self.enemy_grid.reached_bottom(self.player.y):
            self.trigger_game_over(victory=False)

        # All enemies defeated
        if not self.enemy_grid.alive_enemies():
            self.trigger_game_over(victory=True)

    def trigger_game_over(self, victory=False):
        if not self.game_over:
            self.game_over = True
            self.victory = victory
            self.sound_manager.play_game_over()

    def reset_game(self, difficulty=None):
        if difficulty and difficulty in self.DIFFICULTIES:
            self.current_difficulty = difficulty
        diff_cfg = self.DIFFICULTIES[self.current_difficulty]

        self.player = Player(self.width // 2 - 20, self.height - 50, 40, 20)
        self.enemy_grid = EnemyGrid(self.width, speed=diff_cfg["enemy_speed"])
        self.enemy_fire_chance = diff_cfg["fire_chance"]
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self._shoot_cooldown = 0
        self.score = 0
        self.game_over = False
        self.victory = False

    def render(self, screen):
        # Player
        pygame.draw.rect(
            screen,
            GREEN,
            self.player.rect()
        )

        # Enemies
        for enemy in self.enemy_grid.alive_enemies():
            pygame.draw.rect(
                screen,
                WHITE,
                enemy.rect()
            )

        # Player bullets
        for bullet in self.player_bullets:
            pygame.draw.rect(
                screen,
                WHITE,
                bullet.rect()
            )

        # Enemy bullets
        for bullet in self.enemy_bullets:
            pygame.draw.rect(
                screen,
                RED,
                bullet.rect()
            )

        # Score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )
        screen.blit(score_text, (10, 10))

        # Current Difficulty badge in HUD
        diff_cfg = self.DIFFICULTIES[self.current_difficulty]
        diff_text = self.sub_font.render(
            f"Difficulty: {self.current_difficulty.upper()}",
            True,
            diff_cfg["color"]
        )
        screen.blit(diff_text, (self.width - diff_text.get_width() - 12, 14))

        # ---------------------------------------------------------
        # TASK 2 & TASK 3: GAME OVER & REPLAY / DIFFICULTY MENU
        # ---------------------------------------------------------
        if self.game_over:
            # 1. Dark semi-transparent overlay over the gameplay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            # 2. Centered dialog box
            box_width, box_height = 460, 310
            box_x = (self.width - box_width) // 2
            box_y = (self.height - box_height) // 2
            card_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, (24, 24, 34), card_rect, border_radius=14)

            accent_color = (80, 220, 100) if self.victory else RED
            pygame.draw.rect(screen, accent_color, card_rect, width=3, border_radius=14)

            # 3. Title text
            title_text = "VICTORY!" if self.victory else "GAME OVER"
            title_surf = self.title_font.render(title_text, True, accent_color)
            screen.blit(title_surf, title_surf.get_rect(center=(self.width // 2, box_y + 45)))

            # 4. Final score
            score_surf = self.font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(score_surf, score_surf.get_rect(center=(self.width // 2, box_y + 95)))

            # 5. Replay with Difficulty prompt
            replay_label = self.sub_font.render("Select Difficulty to Replay:", True, (210, 210, 240))
            screen.blit(replay_label, replay_label.get_rect(center=(self.width // 2, box_y + 145)))

            # 6. Difficulty options: Easy, Medium, Hard
            options = [
                ("[1] Easy", (100, 220, 100), self.width // 2 - 130),
                ("[2] Med", (240, 200, 60), self.width // 2),
                ("[3] Hard", (255, 90, 90), self.width // 2 + 130),
            ]
            for label, col, x_pos in options:
                btn_surf = self.sub_font.render(label, True, col)
                screen.blit(btn_surf, btn_surf.get_rect(center=(x_pos, box_y + 195)))

            # 7. Bottom controls prompt
            sub_surf = self.sub_font.render("Press [1 / 2 / 3] to Play Again  |  [Q] to Exit", True, (170, 170, 180))
            screen.blit(sub_surf, sub_surf.get_rect(center=(self.width // 2, box_y + 260)))