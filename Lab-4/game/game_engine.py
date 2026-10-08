import pygame
import random
from .player import Player
from .enemy import EnemyGrid
from .bullet import Bullet

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.player = Player(width // 2 - 20, height - 50, 40, 20)
        self.enemy_grid = EnemyGrid(width)

        self.player_bullets = []
        self.enemy_bullets = []

        self._shoot_cooldown = 0
        self.enemy_fire_chance = 0.003

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self._shoot_cooldown <= 0:
                bullet_x = self.player.center_x() - 2
                self.player_bullets.append(
                    Bullet(bullet_x, self.player.y, direction=-1)
                )
                self._shoot_cooldown = 15

    def handle_input(self):
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

                    break

        # Enemy bullet hits player
        for bullet in self.enemy_bullets:
            if bullet.rect().colliderect(self.player.rect()):
                self.game_over = True
                break

        # Enemies reached the player
        if self.enemy_grid.reached_bottom(self.player.y):
            self.game_over = True

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

        # Temporary game-over message
        if self.game_over and not getattr(
            self,
            "_game_over_logged",
            False
        ):
            print(
                "Game over! Final score:",
                self.score
            )

            self._game_over_logged = True
