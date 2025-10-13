import pygame, random
from dan import Bullet
from cau_hinh import ENEMY_BULLET_SPEED


class Boss(pygame.sprite.Sprite):
    """
    Boss mạnh hơn kẻ thù thường: nhiều HP, bắn liên tục và không tự chết khi va chạm với người chơi.
    Constructor: (pos, muc_tieu_nguoi_choi, nhom_tat_ca_sprite, nhom_dan)
    """
    def __init__(self, vi_tri, muc_tieu_nguoi_choi, nhom_tat_ca_sprite, nhom_dan):
        super().__init__()
        # Lớp hình lớn để dễ phân biệt
        self.image = pygame.Surface((120, 120))
        self.image.fill((120, 20, 140))
        # Thêm một viền để trông giống boss
        pygame.draw.rect(self.image, (200, 80, 200), self.image.get_rect(), 6)
        self.rect = self.image.get_rect(center=vi_tri)

        # Tham chiếu giống Enemy
        self.muc_tieu = muc_tieu_nguoi_choi
        self.nhom_tat_ca = nhom_tat_ca_sprite
        self.nhom_dan = nhom_dan

        # Thuộc tính chiến đấu
        self.hp = 30
        self.max_hp = self.hp
        self.toc_do = 40
        # Di chuyển chậm, đổi hướng theo timer
        self.huong = pygame.Vector2(0, 1)
        self.thoi_gian_doi_huong = 2.5
        self.dem_doi_huong = 0.0

        # Bắn một cách liên tục, nhưng nhanh hơn
        self.khoang_thoi_gian_ban = 0.6
        self.dem_ban = 0.0

        # Khi va chạm với player, boss sẽ không chết ngay
        self.dies_on_collide = False

    def update(self, dt):
        # Di chuyển chậm lên xuống hoặc sang ngang một cách đơn giản
        self.rect.x += self.huong.x * self.toc_do * dt
        self.rect.y += self.huong.y * self.toc_do * dt

        man_hinh = pygame.display.get_surface()
        vung = man_hinh.get_rect()
        # Giữ boss luôn trong vùng màn hình
        if not vung.contains(self.rect):
            # Đẩy vào trong và đổi hướng
            self.rect.clamp_ip(vung)
            self.huong *= -1

        # Đổi hướng theo timer để di chuyển "có nhịp"
        self.dem_doi_huong += dt
        if self.dem_doi_huong >= self.thoi_gian_doi_huong:
            self.dem_doi_huong = 0.0
            # Chọn hướng ngẫu nhiên nhưng ưu tiên hướng về giữa
            dx = (vung.centerx - self.rect.centerx) + random.uniform(-100, 100)
            dy = (vung.centery - self.rect.centery) + random.uniform(-50, 50)
            vec = pygame.Vector2(dx, dy)
            if vec.length() == 0:
                vec = pygame.Vector2(1, 0)
            self.huong = vec.normalize()

        # Bắn theo tốc độ boss
        self.dem_ban += dt
        if self.dem_ban >= self.khoang_thoi_gian_ban:
            self.dem_ban = 0.0
            self.ban_ve_nguoi_choi()

    def ban_ve_nguoi_choi(self):
        if not self.muc_tieu:
            return
        dx = self.muc_tieu.rect.centerx - self.rect.centerx
        dy = self.muc_tieu.rect.centery - self.rect.centery
        vec = pygame.Vector2(dx, dy)
        if vec.length() == 0:
            vec = pygame.Vector2(1, 0)
        # Bắn nhiều đạn cùng lúc theo chùm
        angles = [-0.2, 0.0, 0.2]
        for a in angles:
            rot = vec.rotate_rad(a)
            vien_dan = Bullet(self.rect.center, rot, owner='enemy')
            # Điều chỉnh kích thước/hiện thị cho phù hợp (Bullet class tự tạo hình theo owner)
            self.nhom_tat_ca.add(vien_dan)
            self.nhom_dan.add(vien_dan)

    def take_damage(self, amount=1):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0

    # Alias update để tương thích
    cap_nhat = update
