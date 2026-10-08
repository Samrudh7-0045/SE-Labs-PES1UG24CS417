import os
import math
import wave
import struct
import random
import pygame

SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")

def generate_wav(filepath, duration_s, sample_generator, sample_rate=44100):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    num_samples = int(duration_s * sample_rate)
    with wave.open(filepath, "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            sample = sample_generator(t, duration_s)
            sample = max(-1.0, min(1.0, sample))
            int_sample = int(sample * 32767)
            frames.extend(struct.pack("<h", int_sample))
        wav_file.writeframes(frames)

def generate_default_sounds():
    shoot_path = os.path.join(SOUNDS_DIR, "shoot.wav")
    hit_path = os.path.join(SOUNDS_DIR, "enemy_hit.wav")
    game_over_path = os.path.join(SOUNDS_DIR, "game_over.wav")

    # 1. Player Shoot Sound: high-to-low laser chirp (0.12s)
    if not os.path.exists(shoot_path):
        def shoot_wave(t, duration):
            freq = 950 - 650 * (t / duration)
            decay = 1.0 - (t / duration)
            phase = 2 * math.pi * freq * t
            # Square wave for retro 8-bit feel
            val = 1.0 if math.sin(phase) > 0 else -1.0
            return val * 0.4 * decay

        generate_wav(shoot_path, 0.12, shoot_wave)

    # 2. Enemy Destroyed Sound: crunchy explosion noise (0.22s)
    if not os.path.exists(hit_path):
        def hit_wave(t, duration):
            decay = (1.0 - (t / duration)) ** 2
            low_freq = 90 + 40 * math.sin(2 * math.pi * 30 * t)
            rumble = math.sin(2 * math.pi * low_freq * t)
            noise = random.uniform(-1.0, 1.0)
            return (0.7 * noise + 0.3 * rumble) * 0.5 * decay

        generate_wav(hit_path, 0.22, hit_wave)

    # 3. Game Over Sound: descending retro arpeggio (0.75s)
    if not os.path.exists(game_over_path):
        def game_over_wave(t, duration):
            notes = [360, 300, 240, 180]
            note_idx = min(int(t / (duration / 4)), 3)
            freq = notes[note_idx]
            sub_t = t % (duration / 4)
            decay = 1.0 - (sub_t / (duration / 4))
            val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
            return val * 0.45 * decay

        generate_wav(game_over_path, 0.75, game_over_wave)


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.shoot_sound = None
        self.hit_sound = None
        self.game_over_sound = None

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            generate_default_sounds()

            shoot_path = os.path.join(SOUNDS_DIR, "shoot.wav")
            hit_path = os.path.join(SOUNDS_DIR, "enemy_hit.wav")
            game_over_path = os.path.join(SOUNDS_DIR, "game_over.wav")

            self.shoot_sound = pygame.mixer.Sound(shoot_path)
            self.hit_sound = pygame.mixer.Sound(hit_path)
            self.game_over_sound = pygame.mixer.Sound(game_over_path)

            self.shoot_sound.set_volume(0.4)
            self.hit_sound.set_volume(0.5)
            self.game_over_sound.set_volume(0.6)
            self.enabled = True
        except Exception as e:
            print(f"[SoundManager] Audio disabled or unavailable: {e}")
            self.enabled = False

    def play_shoot(self):
        if self.enabled and self.shoot_sound:
            try:
                self.shoot_sound.play()
            except Exception:
                pass

    def play_enemy_hit(self):
        if self.enabled and self.hit_sound:
            try:
                self.hit_sound.play()
            except Exception:
                pass

    def play_game_over(self):
        if self.enabled and self.game_over_sound:
            try:
                self.game_over_sound.play()
            except Exception:
                pass
