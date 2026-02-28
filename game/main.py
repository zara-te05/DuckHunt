# main.py – DuckHunt Game (MediaPipe Tasks API compatible)
import os
import sys
import time
import urllib.request

import cv2 as cv
import numpy as np
import pygame
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

# ─── Rutas base ───────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
IMG_DIR    = os.path.join(BASE_DIR, "..", "img")
SOUND_DIR  = os.path.join(BASE_DIR, "..", "sound")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "hand_landmarker.task")
MODEL_URL  = ("https://storage.googleapis.com/mediapipe-models/"
              "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")

# ─── Descargar modelo si no existe ────────────────────────────────────────────
os.makedirs(MODELS_DIR, exist_ok=True)
if not os.path.exists(MODEL_PATH):
    print("Descargando modelo hand_landmarker.task (~23 MB)...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Modelo descargado.")

# ─── Configuración de MediaPipe Tasks API ─────────────────────────────────────
print(f"MediaPipe versión: {mp.__version__}")

BaseOptions    = mp_python.BaseOptions
HandLandmarker = mp_vision.HandLandmarker
HandLandmarkerOptions = mp_vision.HandLandmarkerOptions
VisionRunningMode = mp_vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
detector = HandLandmarker.create_from_options(options)

# ─── Pygame ───────────────────────────────────────────────────────────────────
pygame.init()
SCREEN_W, SCREEN_H = 900, 650
screen  = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("🦆 Duck Hunt")
clock   = pygame.time.Clock()
FPS     = 60

# Fuentes
font_hud   = pygame.font.SysFont("Arial", 24, bold=True)
font_big   = pygame.font.SysFont("Arial", 52, bold=True)
font_small = pygame.font.SysFont("Arial", 20)

# Fondo
background = pygame.image.load(os.path.join(IMG_DIR, "fondo.png"))
background = pygame.transform.scale(background, (SCREEN_W, SCREEN_H))

# Sonido
pygame.mixer.init()
sound_gun = pygame.mixer.Sound(os.path.join(SOUND_DIR, "gun.mp3"))

# Import sprites
from AvesSprites import AvesSprites

# ─── Variables de juego ───────────────────────────────────────────────────────
NUM_AVES  = 10
MAX_LIVES = 3

score     = 0
lives     = MAX_LIVES
game_over = False

array_aves  = [AvesSprites(SCREEN_W, SCREEN_H) for _ in range(NUM_AVES)]
group_aves  = pygame.sprite.Group(*array_aves)

# ─── Cámara ───────────────────────────────────────────────────────────────────
cap           = cv.VideoCapture(0)
frame_counter  = 0
start_time     = time.time()
timestamp_ms   = 0

# ─── Estado del disparador ────────────────────────────────────────────────────
# Pinch: distancia normalizada entre pulgar (lm4) e índice (lm8)
# Cuando la distancia cae bajo PINCH_THRESHOLD → disparo
PINCH_THRESHOLD = 0.07   # ajustar entre 0.05-0.10 según distancia a la cámara
PINCH_COOLDOWN  = 20     # frames mínimos entre disparos

is_pinching      = False
pinch_cooldown   = 0
cursor_x         = SCREEN_W // 2
cursor_y         = SCREEN_H // 2

# ─── Miniatura de cámara en pygame ───────────────────────────────────────────
THUMB_W, THUMB_H = 200, 150   # tamaño de la miniatura

# ─────────────────────────────────────────────────────────────────────────────
def draw_hud():
    """Dibuja puntaje, vidas y FPS en pantalla."""
    # Panel semitransparente
    hud_surf = pygame.Surface((SCREEN_W, 50), pygame.SRCALPHA)
    hud_surf.fill((0, 0, 0, 160))
    screen.blit(hud_surf, (0, 0))

    score_text = font_hud.render(f"🎯 Puntos: {score}", True, (255, 220, 0))
    lives_text = font_hud.render(f"❤ Vidas: {lives}", True, (255, 80, 80))
    fps_real   = clock.get_fps()
    fps_text   = font_small.render(f"FPS: {fps_real:.0f}", True, (180, 255, 180))

    screen.blit(score_text, (20, 12))
    screen.blit(lives_text, (SCREEN_W // 2 - lives_text.get_width() // 2, 12))
    screen.blit(fps_text,   (SCREEN_W - fps_text.get_width() - 15, 30))


def draw_crosshair(x, y):
    """Dibuja la mira en la posición (x, y)."""
    pygame.draw.circle(screen, (255,  50,  50), (int(x), int(y)), 14, 3)
    pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 14, 1)
    pygame.draw.line(screen, (255, 255, 255), (int(x)-22, int(y)), (int(x)+22, int(y)), 1)
    pygame.draw.line(screen, (255, 255, 255), (int(x), int(y)-22), (int(x), int(y)+22), 1)


def draw_game_over():
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    go_text   = font_big.render("GAME OVER", True, (255, 60, 60))
    sc_text   = font_hud.render(f"Puntos finales: {score}", True, (255, 220, 0))
    rst_text  = font_small.render("Presiona R para reiniciar  |  Q para salir", True, (200, 200, 200))
    screen.blit(go_text,  ((SCREEN_W - go_text.get_width())  // 2, SCREEN_H // 2 - 80))
    screen.blit(sc_text,  ((SCREEN_W - sc_text.get_width())  // 2, SCREEN_H // 2))
    screen.blit(rst_text, ((SCREEN_W - rst_text.get_width()) // 2, SCREEN_H // 2 + 60))


def reset_game():
    global score, lives, game_over, array_aves, group_aves
    score     = 0
    lives     = MAX_LIVES
    game_over = False
    array_aves  = [AvesSprites(SCREEN_W, SCREEN_H) for _ in range(NUM_AVES)]
    group_aves  = pygame.sprite.Group(*array_aves)


# ─── Bucle principal ──────────────────────────────────────────────────────────
try:
    while True:
        # ── Eventos ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    raise SystemExit
                if event.key == pygame.K_r and game_over:
                    reset_game()

        # ── Fondo ────────────────────────────────────────────────────────────
        screen.blit(background, (0, 0))

        if game_over:
            # Mostrar aves (congeladas) y pantalla de fin
            group_aves.draw(screen)
            draw_game_over()
            draw_hud()
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # ── Leer cámara ──────────────────────────────────────────────────────
        ret, frame = cap.read()
        if not ret:
            continue

        frame_counter += 1
        timestamp_ms  = int((time.time() - start_time) * 1000)

        # ── Detección de mano ─────────────────────────────────────────────────
        rgb_frame  = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image   = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        results    = detector.detect_for_video(mp_image, timestamp_ms)

        fh, fw = frame.shape[:2]

        if pinch_cooldown > 0:
            pinch_cooldown -= 1

        if results.hand_landmarks:
            for hand_lm in results.hand_landmarks:
                # ── Mover mira con la punta del índice (landmark 8) ──────────
                lm8   = hand_lm[8]
                raw_x = lm8.x * fw
                raw_y = lm8.y * fh

                # Espejo en X (cámara frontal)
                raw_x = fw - raw_x

                # Mapear a pantalla pygame (región central de la cámara)
                cx, cy = fw // 2, fh // 2
                ref_r  = 120
                cursor_x = int(np.interp(raw_x, (cx - ref_r, cx + ref_r), (0, SCREEN_W)))
                cursor_y = int(np.interp(raw_y, (cy - ref_r, cy + ref_r), (0, SCREEN_H)))
                cursor_x = max(0, min(cursor_x, SCREEN_W))
                cursor_y = max(0, min(cursor_y, SCREEN_H))

                # ── Gesto de disparo: PINCH (pulgar lm4 cerca de índice lm8) ──
                # Distancia normalizada (valor entre 0 y 1 aprox)
                lm4 = hand_lm[4]
                dx  = lm4.x - lm8.x
                dy  = lm4.y - lm8.y
                pinch_dist = np.sqrt(dx*dx + dy*dy)

                if pinch_dist < PINCH_THRESHOLD and pinch_cooldown == 0:
                    # ¡Disparo!
                    pinch_cooldown = PINCH_COOLDOWN
                    sound_gun.play()
                    for ave in array_aves:
                        if ave.colision(cursor_x, cursor_y):
                            score += 1

                # Indicador visual de pinch en miniatura
                pinch_pct = max(0.0, 1.0 - pinch_dist / PINCH_THRESHOLD)
                color_ind = (
                    int(255 * pinch_pct),
                    int(255 * (1 - pinch_pct)),
                    0
                )
                # Dibujar círculo en miniatura (se procesa más abajo)
                # Guardamos el color para usarlo en la miniatura
                _pinch_color = color_ind
        else:
            _pinch_color = (100, 100, 100)

        # ── Actualizar y dibujar aves ─────────────────────────────────────────
        group_aves.update()
        group_aves.draw(screen)

        # Detectar aves que escaparon
        for ave in array_aves:
            if ave.just_escaped:
                lives -= 1
                ave.just_escaped = False
                if lives <= 0:
                    game_over = True

        # ── Mira ─────────────────────────────────────────────────────────────
        draw_crosshair(cursor_x, cursor_y)

        # ── HUD ──────────────────────────────────────────────────────────────
        draw_hud()

        # ── Miniatura de cámara en pygame (esquina inferior derecha) ─────────
        try:
            thumb_frame = cv.flip(frame, 1)                          # espejo
            thumb_frame = cv.resize(thumb_frame, (THUMB_W, THUMB_H))
            thumb_rgb   = cv.cvtColor(thumb_frame, cv.COLOR_BGR2RGB)
            # OpenCV es HxWxC, pygame surfarray espera WxHxC
            thumb_surf  = pygame.surfarray.make_surface(
                np.transpose(thumb_rgb, (1, 0, 2))
            )
            # Borde de color según estado de pinch
            thumb_x = SCREEN_W - THUMB_W - 8
            thumb_y = SCREEN_H - THUMB_H - 8
            pygame.draw.rect(screen, _pinch_color,
                             (thumb_x - 2, thumb_y - 2, THUMB_W + 4, THUMB_H + 4), 3)
            screen.blit(thumb_surf, (thumb_x, thumb_y))
            # Etiqueta
            lbl = font_small.render("CAM", True, (200, 200, 200))
            screen.blit(lbl, (thumb_x + 4, thumb_y + 4))
        except Exception:
            pass  # Si la cámara falla, simplemente no muestra la miniatura

        pygame.display.flip()
        clock.tick(FPS)

finally:
    cap.release()
    cv.destroyAllWindows()
    detector.close()
    pygame.quit()