import pygame, os, math
from dan import Bullet
from cau_hinh import PLAYER_SPEED, PLAYER_MAX_HP, PLAYER_MAGAZINE, PLAYER_RESERVE_MAX, RELOAD_TIME

class NguoiChoi(pygame.sprite.Sprite):
    def __init__(self, vi_tri, nhom_tat_ca, nhom_dan):
        super().__init__()

        #  HÀM HỖ TRỢ LOAD ẢNH 
        def load_img(name):
            path = os.path.join("assets", "nguoi_choi", name)
          
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (80, 80))  
            return img

        #  LOAD TẤT CẢ ANIMATION 
        self.animations = {
            'Đứng Yên': [load_img('dungyen.png')],
            'Chạy': [load_img(f'chay{i}.png') for i in range(1, 9)],
            'Bắn': [load_img(f'ban{i}.png') for i in range(1, 5)],
            'Chết': [load_img(f'chet{i}.png') for i in range(1, 5)]
        }

        # TRẠNG THÁI LÚC BAN ĐẦU 
        self.state = 'Đứng Yên'
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=vi_tri)

        # Biến hướng (True = nhìn phải, False = nhìn trái)
        self.huong_phai = True

        #  CÁC NHÓM SPRITE 
        self.all_sprites = nhom_tat_ca
        self.bullets_group = nhom_dan

        #  CHỈ SỐ NHÂN VẬT
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp

        self.magazine = PLAYER_MAGAZINE
        self.magazine_size = PLAYER_MAGAZINE
        self.reserve = PLAYER_RESERVE_MAX

        self.reloading = False
        self.reload_time = RELOAD_TIME
        self._reload_timer = 0.0

        self.speed = PLAYER_SPEED

    
    # CẬP NHẬT ANIMATION
    
    def update_animation(self):
        animation_speed = 0.08
        self.frame_index += animation_speed

        if self.frame_index >= len(self.animations[self.state]):
            if self.state == 'Chết':
                self.frame_index = len(self.animations['Chết']) - 1
            else:
                self.frame_index = 0

        current_img = self.animations[self.state][int(self.frame_index)]

        # Lật ảnh nếu đang quay trái
        if not self.huong_phai:
            current_img = pygame.transform.flip(current_img, True, False)

        self.image = current_img

    
    # XỬ LÝ CẬP NHẬT VÀ DI CHUYỂN
    
    def cap_nhat(self, dt, phim):
        self.update_animation()

        van_toc = pygame.Vector2(0, 0)

        if phim[pygame.K_w] or phim[pygame.K_UP]:
            van_toc.y = -1
        if phim[pygame.K_s] or phim[pygame.K_DOWN]:
            van_toc.y = 1
        if phim[pygame.K_a] or phim[pygame.K_LEFT]:
            van_toc.x = -1
            self.huong_phai = False  # Quay trái
        if phim[pygame.K_d] or phim[pygame.K_RIGHT]:
            van_toc.x = 1
            self.huong_phai = True   # Quay phải

        if van_toc.length() > 0:
            van_toc = van_toc.normalize()
            self.state = 'Chạy'
        else:
            self.state = 'Đứng Yên'

        # Di chuyển
        self.rect.x += van_toc.x * self.speed * dt
        self.rect.y += van_toc.y * self.speed * dt

        # Giữ trong màn hình
        man_hinh = pygame.display.get_surface()
        self.rect.clamp_ip(man_hinh.get_rect())

        # Xử lý nạp đạn
        if self.reloading:
            self._reload_timer += dt
            if self._reload_timer >= self.reload_time:
                self._hoan_tat_nap()

    
    # CÁC HÀNH ĐỘNG CHIẾN ĐẤU
    
    def co_the_ban(self):
        return (not self.reloading) and self.magazine > 0

    def ban_vao_chuot(self):
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

        self.state = 'Bắn'
        self.frame_index = 0
        return vien_dan
# Các chức năng nạp đạn :
    def bat_dau_nap(self):
        if self.reloading or self.magazine >= self.magazine_size or self.reserve <= 0:
            return False
        self.reloading = True
        self._reload_timer = 0.0
        return True 
    
    def _hoan_tat_nap(self):
        can_them = self.magazine_size - self.magazine
        lay = min(can_them, self.reserve)
        self.magazine += lay
        self.reserve -= lay
        self.reloading = False
        self._reload_timer = 0.0
# Nhận sát thương khi trúng đạn :
    def nhan_sat_thuong(self, so_luong=1):
        self.hp -= so_luong
        if self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            self.state = 'Chết'

    # Alias tiếng Anh (để tương thích với code cũ)
    update = cap_nhat
    can_shoot = co_the_ban
    shoot_at_mouse = ban_vao_chuot
    start_reload = bat_dau_nap
    _finish_reload = _hoan_tat_nap
    take_damage = nhan_sat_thuong

# Alias tên lớp cũ
Player = NguoiChoi
