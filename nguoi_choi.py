import pygame, os
from dan import Bullet
from cau_hinh import PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_MAGAZINE, PLAYER_RESERVE_MAX, RELOAD_TIME

class NguoiChoi(pygame.sprite.Sprite):
    def __init__(self, vi_tri, nhom_tat_ca, nhom_dan):
        super().__init__()

        # ===== Hàm hỗ trợ load ảnh =====
        def load_img(name):
            path = os.path.join("assets", "nguoi_choi", name)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (80, 100))
            return img

        # ===== Load toàn bộ animation =====
        self.animations = {
            'Đứng Yên': [load_img('dungyen.png')],
            'Chạy': [load_img(f'chay{i}.png') for i in range(1, 9)],
            'Bắn': [load_img(f'ban{i}.png') for i in range(1, 5)],
            'Chết': [load_img(f'chet{i}.png') for i in range(1, 5)],
            'Trúng Đạn': [load_img(f'trungdan{i}.png') for i in range(1, 6)],
            'Thay Đạn': [load_img(f'thaydan{i}.png') for i in range(1, 9)],
            'Nhào Lộn': [load_img(f'nhaolon{i}.png') for i in range(1, 8)]
        }

        # ===== Trạng thái khởi tạo =====
        self.state = 'Đứng Yên'
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=vi_tri)

        # ===== Nhóm sprite =====
        self.all_sprites = nhom_tat_ca
        self.bullets_group = nhom_dan

        # ===== Hướng nhìn =====
        self.huong_phai = True

        # ===== Chỉ số nhân vật =====
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.magazine = PLAYER_MAGAZINE
        self.magazine_size = PLAYER_MAGAZINE
        self.reserve = PLAYER_RESERVE_MAX
        self.reloading = False
        self.reload_time = RELOAD_TIME
        self._reload_timer = 0.0

        # ===== Di chuyển =====
        self.speed = PLAYER_SPEED
        self.roll_speed = PLAYER_SPEED * 1.5

        # ===== Điều khiển animation =====
        self.anim_speeds = {
            'Đứng Yên': 0.08,
            'Chạy': 0.12,
            'Bắn': 0.18,
            'Chết': 0.10,
            'Trúng Đạn': 0.05,  # 👈 animation trúng đạn chậm lại
            'Thay Đạn': 0.07,
            'Nhào Lộn': 0.15
        }

        # ===== Trạng thái đặc biệt =====
        self.is_rolling = False
        self.roll_direction = pygame.Vector2(0, 0)
        self.roll_duration = 0.35
        self.roll_timer = 0.0

    # ===== Cập nhật animation =====
    def update_animation(self, dt=1/60):
        speed = self.anim_speeds.get(self.state, 0.1)
        self.frame_index += speed * dt * 60
        frames = self.animations[self.state]

        if self.frame_index >= len(frames):
            if self.state in ['Chết', 'Trúng Đạn', 'Thay Đạn', 'Nhào Lộn', 'Bắn']:
                if self.state == 'Nhào Lộn':
                    self.is_rolling = False
                    self.state = 'Đứng Yên'
                elif self.state == 'Trúng Đạn' and self.hp > 0:
                    self.state = 'Đứng Yên'
                elif self.state == 'Thay Đạn':
                    self.reloading = False
                    self.state = 'Đứng Yên'
                self.frame_index = 0
            else:
                self.frame_index = 0

        pos = self.rect.center
        img = frames[int(self.frame_index)]
        if not self.huong_phai:
            img = pygame.transform.flip(img, True, False)
        self.image = img
        self.rect = self.image.get_rect(center=pos)

    # ===== Cập nhật di chuyển =====
    def cap_nhat(self, dt, phim):
        self.update_animation(dt)

        if self.state == 'Chết':
            return

        # Nếu đang nhào lộn
        if self.is_rolling:
            self.roll_timer += dt
            self.rect.x += self.roll_direction.x * self.roll_speed * dt
            self.rect.y += self.roll_direction.y * self.roll_speed * dt
            if self.roll_timer >= self.roll_duration:
                self.is_rolling = False
                self.state = 'Đứng Yên'
            self.rect.clamp_ip(pygame.display.get_surface().get_rect())
            return

        # Di chuyển bình thường
        van_toc = pygame.Vector2(0, 0)
        if phim[pygame.K_w] or phim[pygame.K_UP]:
            van_toc.y = -1
        if phim[pygame.K_s] or phim[pygame.K_DOWN]:
            van_toc.y = 1
        if phim[pygame.K_a] or phim[pygame.K_LEFT]:
            van_toc.x = -1
            self.huong_phai = False
        if phim[pygame.K_d] or phim[pygame.K_RIGHT]:
            van_toc.x = 1
            self.huong_phai = True

        # Cho phép di chuyển khi thay đạn hoặc trúng đạn
        if van_toc.length() > 0:
            van_toc = van_toc.normalize()
            if not self.is_rolling and self.state != 'Chết':
                if not self.reloading:
                    self.state = 'Chạy'
        else:
            if not self.is_rolling and not self.reloading:
                self.state = 'Đứng Yên'

        self.rect.x += van_toc.x * self.speed * dt
        self.rect.y += van_toc.y * self.speed * dt
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

        # Nạp đạn
        if self.reloading:
            self._reload_timer += dt
            if self._reload_timer >= self.reload_time:
                self._hoan_tat_nap()

        # Nhào lộn
        if phim[pygame.K_LSHIFT]:
            huong = van_toc if van_toc.length() > 0 else pygame.Vector2(1 if self.huong_phai else -1, 0)
            self.bat_dau_nhao_lon(huong)

    # ===== Bắn =====
    def co_the_ban(self):
        return (not self.reloading) and self.magazine > 0 and not self.is_rolling and self.hp > 0

    def ban_vao_chuot(self):
        if not self.co_the_ban():
            return None
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        vec = pygame.Vector2(dx, dy)
        if vec.length() == 0:
            vec = pygame.Vector2(1, 0)
        vien_dan = Bullet(self.rect.center, vec, owner='player')
        self.all_sprites.add(vien_dan)
        self.bullets_group.add(vien_dan)
        self.magazine -= 1
        self.state = 'Bắn'
        self.frame_index = 0
        return vien_dan

    # ===== Nạp đạn =====
    def bat_dau_nap(self):
        if self.reloading or self.magazine >= self.magazine_size or self.reserve <= 0:
            return False
        self.reloading = True
        self.frame_index = 0
        self.state = 'Thay Đạn'
        self._reload_timer = 0.0
        return True

    def _hoan_tat_nap(self):
        can_them = self.magazine_size - self.magazine
        lay = min(can_them, self.reserve)
        self.magazine += lay
        self.reserve -= lay
        self.reloading = False
        self.frame_index = 0
        self.state = 'Đứng Yên'

    # ===== Trúng đạn =====
    def nhan_sat_thuong(self, so_luong=1):
        if self.hp <= 0:
            return
        self.hp -= so_luong
        if self.hp < 0:
            self.hp = 0
        self.frame_index = 0
        self.state = 'Trúng Đạn'
        if self.hp == 0:
            self.state = 'Chết'

    # ===== Nhào lộn =====
    def bat_dau_nhao_lon(self, huong: pygame.Vector2):
        if self.is_rolling or self.state == 'Chết':
            return
        if huong.length() == 0:
            huong = pygame.Vector2(1 if self.huong_phai else -1, 0)
        self.roll_direction = huong.normalize()
        self.is_rolling = True
        self.state = 'Nhào Lộn'
        self.frame_index = 0
        self.roll_timer = 0.0

    # ===== Aliases =====
    update = cap_nhat
    can_shoot = co_the_ban
    shoot_at_mouse = ban_vao_chuot
    start_reload = bat_dau_nap
    _finish_reload = _hoan_tat_nap
    take_damage = nhan_sat_thuong
    start_roll = bat_dau_nhao_lon

Player = NguoiChoi
