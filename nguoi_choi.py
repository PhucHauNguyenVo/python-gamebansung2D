import pygame, os
from dan import Bullet
from cau_hinh import PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_MAGAZINE, PLAYER_RESERVE_MAX, RELOAD_TIME

class NguoiChoi(pygame.sprite.Sprite):
    
    
    # 1. KHỞI TẠO (CONSTRUCTOR)
    
    def __init__(self, vi_tri, nhom_tat_ca, nhom_dan):
        super().__init__()

        # ===== Hàm hỗ trợ load ảnh (Định nghĩa cục bộ) =====
        # (Giữ nguyên vị trí trong __init__ theo yêu cầu không sửa code)
        def load_img(name):
            path = os.path.join("assets", "nguoi_choi", name)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (80, 100))
            return img

        # ===== Load animation chạy với flip =====
        def load_chay_animation():
            animations = {}
            animations[0] = [load_img(f'chaythang{i}.png') for i in range(1, 9)]
            animations[1] = [load_img(f'chay_ngiengphai{i}.png') for i in range(1, 9)]
            animations[2] = [load_img(f'chayphai{i}.png') for i in range(1, 9)]
            animations[3] = [load_img(f'chay_phaixuong{i}.png') for i in range(1, 9)]
            animations[4] = [load_img(f'chayxuong{i}.png') for i in range(1, 9)]
            animations[5] = [pygame.transform.flip(frame, True, False) for frame in animations[3]]
            animations[6] = [pygame.transform.flip(frame, True, False) for frame in animations[2]]
            animations[7] = [pygame.transform.flip(frame, True, False) for frame in animations[1]]
            return animations

        # ===== Load animation bắn (đủ 8 hướng) =====
        def load_ban_animation():
            animations = {}
            animations[0] = [load_img(f'banthang{i}.png') for i in range(1, 9)]
            animations[1] = [load_img(f'ban_ngiengphai{i}.png') for i in range(1, 9)]
            animations[2] = [load_img(f'banphai{i}.png') for i in range(1, 9)]
            animations[3] = [load_img(f'ban_phaixuong{i}.png') for i in range(1, 9)]
            animations[4] = [load_img(f'banxuong{i}.png') for i in range(1, 9)]
            animations[5] = [load_img(f'ban_traixuong{i}.png') for i in range(1, 9)]
            animations[6] = [load_img(f'bantrai{i}.png') for i in range(1, 9)]
            animations[7] = [load_img(f'ban_traithang{i}.png') for i in range(1, 9)]
            return animations

        # ===== Load animation trúng đạn (4 hướng) =====
        def load_trungdan_animation():
            animations = {}
            animations['phai'] = [load_img(f'trungdan_phai{i}.png') for i in range(1, 3)]
            animations['trai'] = [load_img(f'trungdan_trai{i}.png') for i in range(1, 3)]
            animations['thang'] = [load_img(f'trungdan_giua{i}.png') for i in range(1, 3)]
            animations['xuong'] = [load_img(f'trungdan_duoi{i}.png') for i in range(1, 3)]
            return animations

        # ===== Load animation nhảy với flip =====
        def load_nhay_animation():
            animations = {}
            animations[0] = [load_img(f'nhaylen{i}.png') for i in range(1, 12)]
            animations[1] = [load_img(f'nhay_ngienglen{i}.png') for i in range(1, 12)]
            animations[2] = [load_img(f'nhayphai{i}.png') for i in range(1, 12)]
            animations[3] = [load_img(f'nhay_ngiengxuong{i}.png') for i in range(1, 12)]
            animations[4] = [load_img(f'nhayxuong{i}.png') for i in range(1, 12)]
            animations[5] = [pygame.transform.flip(frame, True, False) for frame in animations[3]]
            animations[6] = [pygame.transform.flip(frame, True, False) for frame in animations[2]]
            animations[7] = [pygame.transform.flip(frame, True, False) for frame in animations[1]]
            return animations

        # ===== Load toàn bộ animation =====
        self.animations = {
            'Đứng Yên': [load_img(f'dungyen{i}.png') for i in range(1, 9)],
            'Chạy': load_chay_animation(),
            'Bắn': load_ban_animation(),
            'Trúng Đạn': load_trungdan_animation(),
            'Chết': [load_img(f'chet{i}.png') for i in range(1, 13)],
            'Nhảy': load_nhay_animation(),
            'Thay Đạn': [load_img(f'thaydan{i}.png') for i in range(1, 9)]
        }

        # ===== Trạng thái khởi tạo =====
        self.state = 'Đứng Yên'
        self.frame_index = 0
        self.huong_index = 0
        self.image = self.animations[self.state][self.huong_index]
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
        self.jump_speed = PLAYER_SPEED * 2.0
        self.jump_distance = 150  # Quãng đường nhảy ngang
        self.jump_height = 80     # Độ cao nhảy (pixel)
        
        # ===== Điều khiển animation =====
        self.anim_speeds = {
            'Đứng Yên': 0.08,
            'Chạy': 0.12,
            'Bắn': 0.9,
            'Chết': 0.10,
            'Trúng Đạn': 0.3,
            'Thay Đạn': 0.15,  
            'Nhảy': 0.9
        }

        # ===== Trạng thái nhảy =====
        self.is_jumping = False
        self.jump_start_pos = pygame.Vector2(0, 0)  # Vị trí bắt đầu nhảy
        self.jump_direction = pygame.Vector2(0, 0)  # Hướng nhảy
        self.jump_travelled = 0.0                    # Quãng đường đã đi
        self.current_jump_distance = self.jump_distance  # Khoảng cách nhảy hiện tại
        self.jump_cooldown = 0.8
        self.last_jump_time = -999.0

        self.shoot_cooldown = 0.5
        self.last_shot_time = -999
        self.time_elapsed = 0.0


    # 2. VÒNG LẶP CHÍNH & CẬP NHẬT (MAIN LOOP & UPDATE)

    def cap_nhat(self, dt, phim):
        self.update_animation(dt)
        self.time_elapsed += dt
        if self.reloading:
           self._reload_timer += dt
        if self._reload_timer >= self.reload_time:
            self._hoan_tat_nap()
            self._reload_timer = 0.0

        if self.state == 'Chết':
            return

        # XỬ LÝ NHẢY với chuyển động parabol
        if self.is_jumping:
            import math
            # Di chuyển theo hướng ngang
            move_amount = self.jump_speed * dt
            delta = self.jump_direction * move_amount
            self.rect.centerx += delta.x
            self.rect.centery += delta.y
            self.jump_travelled += move_amount
            
            # Tính độ cao theo parabol: y = -4h/d^2 * x * (x - d)
            # h = jump_height, d = current_jump_distance, x = jump_travelled
            progress = self.jump_travelled / self.current_jump_distance
            if progress <= 1.0:
                # Công thức parabol: cao nhất ở giữa (progress = 0.5)
                height_offset = -4 * self.jump_height * progress * (progress - 1)
                target_y = self.jump_start_pos.y - height_offset
                self.rect.centery = target_y
            else:
                # Kết thúc nhảy
                self.is_jumping = False
                self.jump_travelled = 0.0
                self.state = 'Đứng Yên'
                self.frame_index = 0
                self.rect.centery = self.jump_start_pos.y
            
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

        # Cập nhật hướng dựa trên vector di chuyển
        if van_toc.length() > 0:
            self.huong_index = self.tinh_huong_tu_phim(van_toc)

        # Cho phép di chuyển
        if van_toc.length() > 0:
           van_toc = van_toc.normalize()
           # Nếu đang thay đạn thì vẫn cho di chuyển
           if self.state not in ['Chết', 'Trúng Đạn']:
            if self.state != 'Thay Đạn':
              self.state = 'Chạy'
        else:
           # Nếu không di chuyển
           if self.state not in ['Bắn', 'Trúng Đạn', 'Chết', 'Thay Đạn']:
            self.state = 'Đứng Yên'

        self.rect.x += van_toc.x * self.speed * dt
        self.rect.y += van_toc.y * self.speed * dt
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())

        # NHẢY (Space hoặc Shift)
        now = self.time_elapsed
        if (phim[pygame.K_SPACE] or phim[pygame.K_LSHIFT]) and not self.is_jumping:
            if now - self.last_jump_time >= self.jump_cooldown:
                # Xác định hướng nhảy
                if van_toc.length() > 0:
                    dir_vec = van_toc.normalize()
                else:
                    dir_vec = pygame.Vector2(1 if self.huong_phai else -1, 0)
                self.bat_dau_nhay(dir_vec)
                self.last_jump_time = now

    def update_animation(self, dt=1/60):
        speed = self.anim_speeds.get(self.state, 0.1)
        if self.state in ['Bắn', 'Trúng Đạn']:
            speed *= 0.6

        # Đứng Yên
        if self.state == 'Đứng Yên':
            frames = self.animations[self.state]
            img = frames[self.huong_index]
        # Chạy, Bắn, Nhảy
        elif self.state in ['Chạy', 'Bắn', 'Nhảy']:
            self.frame_index += speed * dt * 60
            frames = self.animations[self.state][self.huong_index]
            if self.frame_index >= len(frames):
                if self.state == 'Bắn':
                    self.state = 'Đứng Yên'
                    self.frame_index = 0
                elif self.state == 'Nhảy':
                    # Animation nhảy lặp lại cho đến khi kết thúc nhảy
                    self.frame_index = 0
                else:
                    self.frame_index = 0
            img = frames[int(self.frame_index)]
        # Trúng Đạn
        elif self.state == 'Trúng Đạn':
            self.frame_index += speed * dt * 60
            huong = self.lay_huong_trungdan()
            frames = self.animations['Trúng Đạn'][huong]
            if self.frame_index >= len(frames):
                if self.hp > 0:
                    self.state = 'Đứng Yên'
                self.frame_index = 0
            img = frames[int(self.frame_index)]
        else:
            # Chết và các trạng thái khác
            self.frame_index += speed * dt * 60
            frames = self.animations[self.state]
            if self.frame_index >= len(frames):
                if self.state == 'Chết':
                    self.frame_index = len(frames) - 1
                else:
                    self.frame_index = 0
            img = frames[int(self.frame_index)]
            if not self.huong_phai and self.state not in ['Đứng Yên', 'Chạy', 'Bắn', 'Trúng Đạn', 'Nhảy']:
                img = pygame.transform.flip(img, True, False)

        pos = self.rect.center
        self.image = img
        self.rect = self.image.get_rect(center=pos)



    # 3.CÁC HÀM HÀNH ĐỘNG GAMEPLAY (GAMEPLAY ACTIONS)
    
    def co_the_ban(self):
        time_since_last_shot = self.time_elapsed - self.last_shot_time
        return (not self.reloading
                and self.magazine > 0
                and not self.is_jumping
                and self.hp > 0
                and time_since_last_shot >= self.shoot_cooldown)

    def ban_vao_chuot(self):
        if not self.co_the_ban():
            return None
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        vec = pygame.Vector2(dx, dy)
        if vec.length() == 0:
            vec = pygame.Vector2(1, 0)

        # Cập nhật hướng nhìn theo vị trí chuột
        self.huong_index = self.tinh_huong_tu_vector(vec)

        vien_dan = Bullet(self.rect.center, vec, owner='player')
        self.all_sprites.add(vien_dan)
        self.bullets_group.add(vien_dan)
        self.magazine -= 1
        self.last_shot_time = self.time_elapsed
        self.state = 'Bắn'
        self.frame_index = 0
        return vien_dan

    def bat_dau_nap(self):
        if self.reloading or self.magazine >= self.magazine_size or self.reserve <= 0:
            return False
        if self.state in ['Bắn', 'Nhảy', 'Trúng Đạn', 'Chết']:
            return False  # Không thể thay đạn khi đang bắn, nhảy, trúng đạn hoặc chết
        
        self.reloading = True
        self.state = 'Thay Đạn'
        self.frame_index = 0
        return True

    def _hoan_tat_nap(self):
        if not self.reloading:
            return
        can_them = self.magazine_size - self.magazine
        lay = min(can_them, self.reserve)
        self.magazine += lay
        self.reserve -= lay
        self.reloading = False
        self.state = 'Đứng Yên'

    def bat_dau_nhay(self, huong: pygame.Vector2):
        if self.is_jumping or self.state == 'Chết':
            return
        if huong.length() == 0:
            huong = pygame.Vector2(1 if self.huong_phai else -1, 0)
        
        # Cập nhật hướng animation
        self.huong_index = self.tinh_huong_tu_phim(huong)
        
        # Điều chỉnh khoảng cách nhảy theo hướng
        # Nếu nhảy theo trục Y (lên/xuống) thì tăng khoảng cách
        if abs(huong.y) > abs(huong.x):  # Nhảy chủ yếu theo Y
            self.current_jump_distance = self.jump_distance * 1.5  # Tăng 50%
        else:  # Nhảy chủ yếu theo X hoặc chéo
            self.current_jump_distance = self.jump_distance
        
        self.jump_direction = huong.normalize()
        self.jump_start_pos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        self.is_jumping = True
        self.jump_travelled = 0.0
        self.state = 'Nhảy'
        self.frame_index = 0

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

    
    # 4. HÀM TÍNH TOÁN HỖ TRỢ (HELPER CALCULATIONS)
   
    def tinh_huong_tu_vector(self, vec):
        if vec.length() == 0:
            return self.huong_index
        import math
        angle = math.atan2(vec.y, vec.x) * 180 / math.pi
        if angle < 0:
            angle += 360
        if 337.5 <= angle or angle < 22.5:
            return 2
        elif 22.5 <= angle < 67.5:
            return 3
        elif 67.5 <= angle < 112.5:
            return 0
        elif 112.5 <= angle < 157.5:
            return 5
        elif 157.5 <= angle < 202.5:
            return 6
        elif 202.5 <= angle < 247.5:
            return 7
        elif 247.5 <= angle < 292.5:
            return 4
        else:
            return 1

    def tinh_huong_tu_phim(self, van_toc):
        if van_toc.length() == 0:
            return self.huong_index
        x, y = van_toc.x, van_toc.y
        if x == 0 and y == -1:
            return 4
        elif x == 1 and y == -1:
            return 1
        elif x == 1 and y == 0:
            return 2
        elif x == 1 and y == 1:
            return 3
        elif x == 0 and y == 1:
            return 0
        elif x == -1 and y == 1:
            return 5
        elif x == -1 and y == 0:
            return 6
        elif x == -1 and y == -1:
            return 7
        return self.huong_index

    def lay_huong_trungdan(self):
        if self.huong_index in [0, 1, 7]:
            return 'thang'
        elif self.huong_index in [2, 3]:
            return 'phai'
        elif self.huong_index == 4:
            return 'xuong'
        else:
            return 'trai'

    # =========================================================================
    # 5. ALIASES (TÊN THAY THẾ)
    # =========================================================================
    update = cap_nhat
    can_shoot = co_the_ban
    shoot_at_mouse = ban_vao_chuot
    start_reload = bat_dau_nap
    _finish_reload = _hoan_tat_nap
    take_damage = nhan_sat_thuong
    start_jump = bat_dau_nhay

Player = NguoiChoi