# dan.py - Đạn
import pygame
from cau_hinh import BULLET_SPEED, ENEMY_BULLET_SPEED

class VienDan(pygame.sprite.Sprite):
    """
    Viên đạn có chủ sở hữu: 'player' hoặc 'enemy'
    direction: pygame.Vector2 đã chuẩn hóa
    speed: px/giây
    """
    def __init__(self, pos, direction, owner='player'):
        super().__init__()
        # Kích thước khác nhau cho trực quan
        if owner == 'player':
            self.image = pygame.Surface((8, 4))
            self.image.fill((255, 230, 0))
            speed = BULLET_SPEED
        else:
            self.image = pygame.Surface((6, 6))
            self.image.fill((255, 80, 80))
            speed = ENEMY_BULLET_SPEED

        self.rect = self.image.get_rect(center=pos)
        self.direction = direction.normalize() if direction.length() != 0 else pygame.Vector2(1, 0)
        self.owner = owner
        self.speed = speed

        # Alias tiếng Việt cho thuộc tính
        self.huong = self.direction
        self.chu_so_huu = self.owner
        self.toc_do = self.speed

    def cap_nhat(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

        # Xóa nếu ra ngoài màn hình
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.colliderect(self.rect):
            self.kill()

    # Alias tiếng Anh để tương thích với pygame.Group.update
    update = cap_nhat

# Alias tên lớp để tương thích với import cũ
Bullet = VienDan
