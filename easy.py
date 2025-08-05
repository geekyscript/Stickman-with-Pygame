import pygame
pygame.init()

# Screen setup
win = pygame.display.set_mode((200, 300))
clock = pygame.time.Clock()

y = 150  # vertical position
dir = 1  # direction

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()

    win.fill((0, 0, 0))  # Black background

    # Bounce
    y += dir
    if y > 160 or y < 140:
        dir *= -1

    # Draw stick figure
    pygame.draw.circle(win, (255, 255, 255), (100, y - 40), 10, 1)        # Head
    pygame.draw.line(win, (255, 255, 255), (100, y - 30), (100, y), 1)    # Body
    pygame.draw.line(win, (255, 255, 255), (85, y - 20), (115, y - 20), 1) # Arms
    pygame.draw.line(win, (255, 255, 255), (100, y), (85, y + 30), 1)     # Left leg
    pygame.draw.line(win, (255, 255, 255), (100, y), (115, y + 30), 1)    # Right leg

    pygame.display.update()
    clock.tick(30)
