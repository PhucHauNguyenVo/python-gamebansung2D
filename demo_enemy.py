import pygame, sys, time
from ke_thu import Enemy
from nguoi_choi import NguoiChoi

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# dummy groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# create dummy player at center
player = NguoiChoi((WIDTH//2, HEIGHT//2), all_sprites, bullets)
all_sprites.add(player)

# create an enemy
enemy = Enemy((WIDTH//2 - 150, HEIGHT//2), player, all_sprites, bullets)
all_sprites.add(enemy)

states = ['idle', 'run', 'shoot', 'dead']
state_idx = 0
state_time = 0.0
state_duration = 2.5

running = True
start = time.time()
while running:
    dt = clock.tick(60) / 1000.0
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    state_time += dt
    if state_time >= state_duration:
        state_time = 0.0
        state_idx = (state_idx + 1) % len(states)
        enemy.set_state(states[state_idx])

    # NguoiChoi.cap_nhat expects (dt, phim) so handle separately
    phim = pygame.key.get_pressed()
    for spr in list(all_sprites):
        if hasattr(spr, 'cap_nhat'):
            try:
                spr.cap_nhat(dt, phim)
            except TypeError:
                try:
                    spr.update(dt)
                except Exception:
                    pass
        else:
            try:
                spr.update(dt)
            except Exception:
                pass

    screen.fill((30,30,30))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
