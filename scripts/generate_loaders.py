import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio

os.makedirs('scripts', exist_ok=True)
os.makedirs('frontend/public', exist_ok=True)
os.makedirs('mobile/assets', exist_ok=True)

WIDTH, HEIGHT = 600, 400
FPS = 12
DURATION_SEC = 8
TOTAL_FRAMES = FPS * DURATION_SEC  # 96 frames = 8 seconds

# Create target mask for LM Monogram to sample target points
def create_lm_target_mask():
    img = Image.new('L', (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(img)

    # Draw L
    # Vertical line of L
    draw.rectangle([210, 100, 235, 230], fill=255)
    # Horizontal line of L
    draw.rectangle([210, 210, 290, 230], fill=255)
    # Serif bottom left
    draw.polygon([(195, 230), (235, 230), (210, 222)], fill=255)

    # Draw M overlapping/interlocking
    # Left leg of M
    draw.polygon([(250, 130), (270, 130), (250, 230), (235, 230)], fill=255)
    # V part of M
    draw.polygon([(250, 130), (300, 200), (315, 200), (270, 130)], fill=255)
    draw.polygon([(300, 200), (350, 130), (365, 130), (315, 200)], fill=255)
    # Right leg of M
    draw.rectangle([345, 130, 365, 230], fill=255)
    # Serif right
    draw.polygon([(335, 230), (375, 230), (355, 222)], fill=255)

    return np.array(img)

mask = create_lm_target_mask()
y_indices, x_indices = np.where(mask > 128)

NUM_PARTICLES = 400
np.random.seed(42)
sample_indices = np.random.choice(len(x_indices), NUM_PARTICLES, replace=True)

target_x = x_indices[sample_indices].astype(float)
target_y = y_indices[sample_indices].astype(float)

# Initial random positions for particles coming from afar
start_x = np.random.uniform(20, WIDTH - 20, NUM_PARTICLES)
start_y = np.random.uniform(10, HEIGHT - 10, NUM_PARTICLES)

# Particle types: 0=circle, 1=square, 2=triangle, 3=dot
particle_types = np.random.choice([0, 1, 2, 3], NUM_PARTICLES)
particle_sizes = np.random.uniform(3.0, 6.0, NUM_PARTICLES)
particle_speeds = np.random.uniform(0.7, 1.3, NUM_PARTICLES)

# Gold color palette RGB tuples
GOLD_DARK = (180, 135, 45)
GOLD_MID = (218, 165, 32)
GOLD_LIGHT = (245, 215, 110)
GOLD_BRIGHT = (255, 235, 170)

def draw_particle(draw, p_type, x, y, size, color):
    r = size / 2.0
    if p_type == 0:  # Circle
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)
    elif p_type == 1:  # Square
        draw.rectangle([x - r, y - r, x + r, y + r], fill=color)
    elif p_type == 2:  # Triangle
        draw.polygon([(x, y - r * 1.2), (x - r, y + r), (x + r, y + r)], fill=color)
    else:  # Dot
        draw.ellipse([x - r * 0.7, y - r * 0.7, x + r * 0.7, y + r * 0.7], fill=color)

def generate_frames(is_dark=False):
    frames = []
    bg_color = (11, 15, 25) if is_dark else (255, 255, 255)

    # Try loading a clean serif / sans font or fallback
    try:
        font_luka = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)
        font_mossala = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_luka = font_mossala = ImageFont.load_default()

    for f in range(TOTAL_FRAMES):
        img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
        draw = ImageDraw.Draw(img)

        t = f / float(TOTAL_FRAMES)  # 0.0 to 1.0

        # Phase 1: Particles gather from 0 to frame 45 (t = 0 to 0.47)
        gather_progress = min(1.0, (f / 45.0))
        # Ease out cubic function for smooth, meticulous gathering
        eased_gather = 1 - math.pow(1 - gather_progress, 3)

        for i in range(NUM_PARTICLES):
            # Individual speed factor
            p_t = min(1.0, eased_gather * particle_speeds[i])
            curr_x = start_x[i] + (target_x[i] - start_x[i]) * p_t
            curr_y = start_y[i] + (target_y[i] - start_y[i]) * p_t

            # Color transition based on progress
            if p_t < 0.5:
                col = GOLD_DARK if is_dark else (160, 120, 30)
            elif p_t < 0.9:
                col = GOLD_MID
            else:
                col = GOLD_LIGHT

            p_size = particle_sizes[i] * (1.2 - 0.4 * p_t)
            draw_particle(draw, particle_types[i], curr_x, curr_y, p_size, col)

        # Draw clean solid LM Monogram overlay when particles reach target (> frame 35)
        if f >= 35:
            alpha = min(1.0, (f - 35) / 15.0)
            gold_color = (235, 185, 60) if is_dark else (190, 145, 30)

            # Blend solid lines for LM
            lm_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
            lm_draw = ImageDraw.Draw(lm_img)

            # L
            lm_draw.rectangle([210, 100, 235, 230], fill=gold_color + (int(255 * alpha),))
            lm_draw.rectangle([210, 210, 290, 230], fill=gold_color + (int(255 * alpha),))
            lm_draw.polygon([(195, 230), (235, 230), (210, 222)], fill=gold_color + (int(255 * alpha),))

            # M
            lm_draw.polygon([(250, 130), (270, 130), (250, 230), (235, 230)], fill=gold_color + (int(255 * alpha),))
            lm_draw.polygon([(250, 130), (300, 200), (315, 200), (270, 130)], fill=gold_color + (int(255 * alpha),))
            lm_draw.polygon([(300, 200), (350, 130), (365, 130), (315, 200)], fill=gold_color + (int(255 * alpha),))
            lm_draw.rectangle([345, 130, 365, 230], fill=gold_color + (int(255 * alpha),))
            lm_draw.polygon([(335, 230), (375, 230), (355, 222)], fill=gold_color + (int(255 * alpha),))

            img.paste(lm_img, (0, 0), lm_img)

        # Phase 2: Animated writing of "LUKA" and "MOSSALA" (Frames 40 to 80)
        if f >= 40:
            text_progress = min(1.0, (f - 40) / 35.0)

            # LUKA text
            full_luka = "L U K A"
            visible_chars_luka = int(len(full_luka) * min(1.0, text_progress * 1.5))
            luka_str = full_luka[:visible_chars_luka]

            # MOSSALA text
            full_mossala = "M O S S A L A"
            visible_chars_mossala = int(len(full_mossala) * max(0.0, (text_progress - 0.3) * 1.5))
            mossala_str = full_mossala[:visible_chars_mossala]

            text_color = (220, 170, 50) if is_dark else (170, 125, 20)

            # Draw LUKA
            draw.text((WIDTH / 2, 270), luka_str, fill=text_color, font=font_luka, anchor="mm")

            # Divider Line & Diamond
            if text_progress > 0.4:
                line_len = min(180, int((text_progress - 0.4) * 300))
                draw.line([(WIDTH/2 - line_len/2, 295), (WIDTH/2 + line_len/2, 295)], fill=text_color, width=1)
                # Diamond center
                draw.polygon([(WIDTH/2, 291), (WIDTH/2 + 4, 295), (WIDTH/2, 299), (WIDTH/2 - 4, 295)], fill=text_color)

            # Draw MOSSALA
            if visible_chars_mossala > 0:
                draw.text((WIDTH / 2, 318), mossala_str, fill=text_color, font=font_mossala, anchor="mm")

        # Phase 3: Golden shimmer effect across the logo (Frames 70 to 96)
        if f >= 70:
            shimmer_pos = int((f - 70) / 26.0 * (WIDTH + 200)) - 100
            shimmer_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shimmer_img)
            s_draw.polygon([
                (shimmer_pos, 0),
                (shimmer_pos + 60, 0),
                (shimmer_pos + 20, HEIGHT),
                (shimmer_pos - 40, HEIGHT)
            ], fill=(255, 255, 255, 40))
            img.paste(shimmer_img, (0, 0), shimmer_img)

        frames.append(np.array(img))

    return frames

print("Generating loader_white.gif...")
frames_white = generate_frames(is_dark=False)
imageio.mimsave('frontend/public/loader_white.gif', frames_white, fps=FPS)
imageio.mimsave('mobile/assets/loader_white.gif', frames_white, fps=FPS)

print("Generating loader_black.gif...")
frames_black = generate_frames(is_dark=True)
imageio.mimsave('frontend/public/loader_black.gif', frames_black, fps=FPS)
imageio.mimsave('mobile/assets/loader_black.gif', frames_black, fps=FPS)

print("Done generating loader GIFs successfully!")
