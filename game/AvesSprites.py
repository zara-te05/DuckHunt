import os.path
import random

import pygame


class AvesSprites(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        super().__init__()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        AVE_DIR  = os.path.join(BASE_DIR, "..", "img", "ave")

        # Cargar y escalar sprites
        self.aves = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(AVE_DIR, f"ave{i}.png")),
                (80, 80)
            )
            for i in range(1, 11)
        ]

        self.screen_width  = screen_width
        self.screen_height = screen_height

        self.ancho_ave = 80
        self.alto_ave  = 80
        self.mov_ave   = 5

        self.index       = 0
        self.image       = self.aves[self.index]
        self.rect        = self.image.get_rect()
        self.last_update = pygame.time.get_ticks()

        # Posición objetivo aleatoria
        self._set_random_target()

        # Estados
        self.is_dead            = False   # El ave fue disparada
        self.dead_anim_playing  = False   # Animación de muerte en curso
        self.dead_anim_counter  = 0
        self.just_escaped       = False   # Se disparó esta señal un frame para el juego principal

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _set_random_target(self):
        """Elige un destino aleatorio dentro de los 2/3 superiores de la pantalla."""
        self.target_x = random.randint(0, (self.screen_width  - self.ancho_ave) // 5) * 5
        self.target_y = random.randint(0, int((self.screen_height * 0.65) - self.alto_ave) // 5) * 5

    def _cycle_fly_x(self):
        self.index = (self.index + 1) % 2          # frames 0-1 (vuelo horizontal)

    def _cycle_fly_y(self):
        self.index = 5 + (self.index - 5 + 1) % 3  # frames 5-7 (vuelo vertical)

    # ── Actualización ─────────────────────────────────────────────────────────
    def update(self):
        now = pygame.time.get_ticks()
        self.just_escaped = False  # reset cada frame

        if not self.is_dead:
            # Animación viva: mover hacia el destino
            if now - self.last_update > 33:
                self.last_update = now

                if self.rect.x < self.target_x:
                    self.rect.x += self.mov_ave
                    self.image = self.aves[self.index]
                    self._cycle_fly_x()

                elif self.rect.x > self.target_x:
                    self.rect.x -= self.mov_ave
                    raw = self.aves[self.index]
                    self.image = pygame.transform.flip(raw, True, False)
                    self._cycle_fly_x()

                elif self.rect.y < self.target_y:
                    self.rect.y += self.mov_ave
                    self.image = pygame.transform.rotate(self.aves[self.index], 180)
                    self._cycle_fly_y()

                elif self.rect.y > self.target_y:
                    self.rect.y -= self.mov_ave
                    self.image = self.aves[self.index]
                    self._cycle_fly_y()

                else:
                    # Llegó al destino: nuevo destino
                    self.index = 0
                    self._set_random_target()

        else:
            # ── Animación de muerte ───────────────────────────────────────
            if self.dead_anim_playing:
                self.image = self.aves[8]  # frame especial "herido"
                self.dead_anim_counter += 1
                if self.dead_anim_counter >= 12:
                    self.dead_anim_playing  = False
                    self.dead_anim_counter  = 0

            else:
                # Ave cayendo
                self.image = self.aves[9]  # frame cayendo
                fall_limit = int(self.screen_height * 0.65)

                if self.rect.y < fall_limit:
                    self.rect.y += self.mov_ave * 2  # cae más rápido
                else:
                    # El ave escapó / cayó: una señal al juego y reaparece
                    self.just_escaped = True
                    self._respawn()

    def _respawn(self):
        """Reinicia el ave en posición inicial."""
        self.rect.x         = 0
        self.rect.y         = 0
        self.index          = 0
        self.is_dead        = False
        self.dead_anim_playing  = False
        self.dead_anim_counter  = 0
        self._set_random_target()

    # ── Colisión ──────────────────────────────────────────────────────────────
    def colision(self, x, y) -> bool:
        """Devuelve True y marca el ave como muerta si (x, y) la golpea."""
        if not self.is_dead and self.rect.collidepoint(x, y):
            self.is_dead           = True
            self.dead_anim_playing = True
            self.dead_anim_counter = 0
            self.image             = self.aves[8]
            return True
        return False
