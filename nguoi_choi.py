# nguoi_choi.py
import pygame, math
from dan import Bullet
from cau_hinh import PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_MAGAZINE, PLAYER_RESERVE_MAX, RELOAD_TIME

class NguoiChoi(pygame.sprite.Sprite):
    def __init__(self, vi_tri, nhom_tat_ca, nhom_dan):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 180, 200))
        self.rect = self.image.get_rect(center=vi_tri)

        # Nhóm để thêm đạn / sprite
        self.all_sprites = nhom_tat_ca
        self.bullets_group = nhom_dan
        # Alias tiếng Việt
        self.nhom_tat_ca = nhom_tat_ca
        self.nhom_dan = nhom_dan

        # Chỉ số
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp

        self.magazine = PLAYER_MAGAZINE      # đạn đang có trong băng
        self.magazine_size = PLAYER_MAGAZINE
        self.reserve = PLAYER_RESERVE_MAX    # đạn dự trữ tổng

        # Nạp đạn
        self.reloading = False
        self.reload_time = RELOAD_TIME
        self._reload_timer = 0.0

        # Di chuyển
        self.speed = PLAYER_SPEED

    def cap_nhat(self, dt, phim):
        # Di chuyển mượt theo dt
        van_toc = pygame.Vector2(0, 0)
        if phim[pygame.K_w] or phim[pygame.K_UP]:
            van_toc.y = -1
        if phim[pygame.K_s] or phim[pygame.K_DOWN]:
            van_toc.y = 1
        if phim[pygame.K_a] or phim[pygame.K_LEFT]:
            van_toc.x = -1
        if phim[pygame.K_d] or phim[pygame.K_RIGHT]:
            van_toc.x = 1
        if van_toc.length() > 0:
            van_toc = van_toc.normalize()
        self.rect.x += van_toc.x * self.speed * dt
        self.rect.y += van_toc.y * self.speed * dt

        # Giữ trong màn hình
        man_hinh = pygame.display.get_surface()
        self.rect.clamp_ip(man_hinh.get_rect())

        # Xử lý nạp đạn nếu đang nạp
        if self.reloading:
            self._reload_timer += dt
            if self._reload_timer >= self.reload_time:
                self._hoan_tat_nap()

    def co_the_ban(self):
        return (not self.reloading) and self.magazine > 0

    def ban_vao_chuot(self):
        """Bắn về hướng con trỏ chuột nếu còn đạn trong băng"""
        if not self.co_the_ban():
            return None
        mx, my = pygame.mouse.get_pos()
        dx = mx - self.rect.centerx
        dy = my - self.rect.centery
        vec = pygame.Vector2(dx, dy)
        if vec.length() == 0:
            vec = pygame.Vector2(1, 0)
        vien_dan = Bullet(self.rect.center, vec, owner='player')
        self.all_sprites.add(vien_dan)
        self.bullets_group.add(vien_dan)
        self.magazine -= 1
        return vien_dan

    def bat_dau_nap(self):
        """Bắt đầu nạp đạn: chỉ khi còn đạn dự trữ và băng chưa đầy"""
        if self.reloading:
            return False
        if self.magazine >= self.magazine_size:
            return False
        if self.reserve <= 0:
            return False
        self.reloading = True
        self._reload_timer = 0.0
        return True

    def _hoan_tat_nap(self):
        """Hoàn tất nạp: chuyển đạn từ dự trữ -> băng"""
        can_them = self.magazine_size - self.magazine
        lay = min(can_them, self.reserve)
        self.magazine += lay
        self.reserve -= lay
        self.reloading = False
        self._reload_timer = 0.0

    def nhan_sat_thuong(self, so_luong=1):
        self.hp -= so_luong
        if self.hp < 0:
            self.hp = 0

    # Alias tiếng Anh để tương thích với mã hiện có
    update = cap_nhat
    can_shoot = co_the_ban
    shoot_at_mouse = ban_vao_chuot
    start_reload = bat_dau_nap
    _finish_reload = _hoan_tat_nap
    take_damage = nhan_sat_thuong

# Alias tên lớp để tương thích với import cũ
Player = NguoiChoi
