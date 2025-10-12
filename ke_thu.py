# ke_thu.py - Đối tượng kẻ thù
import pygame, random
from dan import Bullet
from cau_hinh import ENEMY_SPEED, ENEMY_SHOOT_INTERVAL_MIN, ENEMY_SHOOT_INTERVAL_MAX

class Enemy(pygame.sprite.Sprite):
    def __init__(self, vi_tri, muc_tieu_nguoi_choi, nhom_tat_ca_sprite, nhom_dan):
        """
        Kẻ thù di chuyển ngẫu nhiên và thỉnh thoảng bắn về phía người chơi.
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((200, 60, 60))
        self.rect = self.image.get_rect(center=vi_tri)

        # Tham chiếu
        self.muc_tieu = muc_tieu_nguoi_choi
        self.nhom_tat_ca = nhom_tat_ca_sprite
        self.nhom_dan = nhom_dan

        # Thuộc tính chuyển động
        self.toc_do = ENEMY_SPEED
        self.huong = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.huong.length() == 0:
            self.huong = pygame.Vector2(1, 0)
        else:
            self.huong = self.huong.normalize()

        # Thời gian đổi hướng
        self.thoi_gian_doi_huong = random.uniform(1.0, 2.5)
        self.dem_doi_huong = 0.0

        # Bắn
        self.khoang_thoi_gian_ban = random.uniform(ENEMY_SHOOT_INTERVAL_MIN, ENEMY_SHOOT_INTERVAL_MAX)
        self.dem_ban = 0.0

    def update(self, dt):
        # Di chuyển
        self.rect.x += self.huong.x * self.toc_do * dt
        self.rect.y += self.huong.y * self.toc_do * dt

        # Chạm biên -> phản xạ
        man_hinh = pygame.display.get_surface()
        vung = man_hinh.get_rect()
        if self.rect.left < vung.left or self.rect.right > vung.right:
            self.huong.x *= -1
            self.rect.clamp_ip(vung)
        if self.rect.top < vung.top or self.rect.bottom > vung.bottom:
            self.huong.y *= -1
            self.rect.clamp_ip(vung)

        # Đổi hướng theo bộ đếm
        self.dem_doi_huong += dt
        if self.dem_doi_huong >= self.thoi_gian_doi_huong:
            self.dem_doi_huong = 0.0
            self.thoi_gian_doi_huong = random.uniform(1.0, 2.5)
            self.huong = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if self.huong.length() == 0:
                self.huong = pygame.Vector2(1, 0)
            else:
                self.huong = self.huong.normalize()

        # Bắn về phía người chơi theo bộ đếm
        self.dem_ban += dt
        if self.dem_ban >= self.khoang_thoi_gian_ban:
            self.dem_ban = 0.0
            self.khoang_thoi_gian_ban = random.uniform(ENEMY_SHOOT_INTERVAL_MIN, ENEMY_SHOOT_INTERVAL_MAX)
            self.ban_ve_phia_nguoi_choi()

    def ban_ve_phia_nguoi_choi(self):
        if not self.muc_tieu:
            return
        dx = self.muc_tieu.rect.centerx - self.rect.centerx
        dy = self.muc_tieu.rect.centery - self.rect.centery
        vec = pygame.Vector2(dx, dy)
        if vec.length() == 0:
            vec = pygame.Vector2(1, 0)
        vien_dan = Bullet(self.rect.center, vec, owner='enemy')
        self.nhom_tat_ca.add(vien_dan)
        self.nhom_dan.add(vien_dan)
