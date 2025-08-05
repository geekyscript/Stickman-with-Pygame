import pygame
import sys
import math
import time
import colorsys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌈 FUNKY RAVE DANCERS 💃🕺")
clock = pygame.time.Clock()

def hsv2rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

def get_bg_color(t):
    beat = int(t * 4) % 2
    hue = (t * 0.1) % 1.0
    brightness = 0.1 + 0.4 * beat
    return hsv2rgb(hue, 1, brightness)

def get_dancer_color(t, dancer_id):
    hue = ((t * 0.5 + dancer_id * 0.2) % 1.0)
    return hsv2rgb(hue, 1, 1)

def get_pose(dancer_id, t):
    t = t % 10
    p = t / 10
    freq = 2 * math.pi

    waist = math.sin(p * freq * (8 + dancer_id * 2)) * 40
    knee = math.sin(p * freq * (4 + dancer_id)) * 25
    spread = 30 + math.sin(p * freq * (2 + dancer_id)) * 20
    twist = math.sin(p * freq * (1 + dancer_id)) * 25

    return waist, knee, spread, twist

def get_dancer_position(dancer_id, t):
    base_x = 200 + dancer_id * 200
    wave_x = math.sin(t * 1.5 + dancer_id) * 100
    base_y = 200
    wave_y = math.sin(t * 2 + dancer_id * 0.5) * 30
    return base_x + wave_x, base_y + wave_y

def draw_spotlight(x, y, t, dancer_id):
    pulse = (math.sin(t * 6 + dancer_id) + 1) / 2
    radius = 90 + pulse * 50
    hue = (0.6 + 0.2 * dancer_id + 0.2 * math.sin(t + dancer_id)) % 1.0
    color = hsv2rgb(hue, 1, 1)
    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for i in range(int(radius), 0, -6):
        alpha = max(0, int(255 * (i / radius) ** 2 * 0.5))
        pygame.draw.circle(glow_surface, (*color, alpha), (radius, radius), i)
    screen.blit(glow_surface, (x - radius, y - radius))

def draw_dancer(x, y, t, dancer_id):
    waist_bounce, knee_swing, spread_base, twist = get_pose(dancer_id, t)
    color = get_dancer_color(t, dancer_id)

    draw_spotlight(x, y + 40, t, dancer_id)

    neck = (x, y)
    waist = (x, y + 50 + waist_bounce)
    pygame.draw.circle(screen, color, (x, y - 35), 22, 3)
    pygame.draw.line(screen, color, neck, waist, 4)

    arm_angle = math.sin(t * 10 + dancer_id) * 2.5
    arm_len = 50
    arm_left = (x - math.cos(arm_angle) * arm_len, y + math.sin(arm_angle) * arm_len)
    arm_right = (x + math.cos(arm_angle) * arm_len, y + math.sin(arm_angle) * arm_len)
    pygame.draw.line(screen, color, neck, arm_left, 4)
    pygame.draw.line(screen, color, neck, arm_right, 4)

    spread = spread_base + twist

    knee_left = (waist[0] - spread + knee_swing, waist[1] + 35)
    foot_left = (waist[0] - spread + knee_swing * 0.6, waist[1] + 90)
    knee_right = (waist[0] + spread - knee_swing, waist[1] + 35)
    foot_right = (waist[0] + spread - knee_swing * 0.6, waist[1] + 90)

    pygame.draw.line(screen, color, waist, knee_left, 4)
    pygame.draw.line(screen, color, knee_left, foot_left, 3)
    pygame.draw.line(screen, color, waist, knee_right, 4)
    pygame.draw.line(screen, color, knee_right, foot_right, 3)

def draw_lasers(t):
    beat = int(t * 6) % 2 == 0
    if beat:
        for _ in range(8):
            x1 = random.randint(0, WIDTH)
            y1 = 0
            x2 = random.randint(0, WIDTH)
            y2 = HEIGHT
            hue = (t * 0.1 + random.random()) % 1.0
            color = hsv2rgb(hue, 1, 1)
            width = random.randint(2, 5)
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), width)

def draw_disco_sparkles(t):
    sparkle_count = 60
    for _ in range(sparkle_count):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        hue = (t * 0.5 + random.random()) % 1.0
        color = hsv2rgb(hue, 1, 1)
        radius = random.randint(2, 6)
        pygame.draw.circle(screen, color, (x, y), radius)

def draw_moving_lights(t):
    for i in range(4):
        y = int((math.sin(t * 0.4 + i) + 1) / 2 * HEIGHT)
        hue = (0.8 + i * 0.1 + t * 0.2) % 1.0
        color = hsv2rgb(hue, 1, 0.2)
        pygame.draw.rect(screen, color, (0, y, WIDTH, 3))

def main():
    running = True
    while running:
        t = time.time() % 20
        screen.fill(get_bg_color(t))

        draw_moving_lights(t)
        draw_lasers(t)
        draw_disco_sparkles(t)

        for i in range(4):
            dancer_x, dancer_y = get_dancer_position(i, t)
            draw_dancer(dancer_x, dancer_y, t, i)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
