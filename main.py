# main.py
import pygame, random, sys
from cau_hinh import RONG, CAO, SO_KHUNG_HINH, KHOANG_SINH_KE_THU
from nguoi_choi import NguoiChoi
from ke_thu import Enemy
from boss import Boss
from ui import ve_ui
from menu_game import MenuTroChoi

pygame.init()
man_hinh = pygame.display.set_mode((RONG, CAO))
pygame.display.set_caption("Giữ Vững - Demo")
dong_ho = pygame.time.Clock()
phong_chu = pygame.font.SysFont(None, 28)

# Menu / trạng thái
menu_tro_choi = MenuTroChoi(man_hinh, phong_chu)

# Nhóm sprite
tat_ca_sprite = pygame.sprite.Group()
nhom_ke_thu = pygame.sprite.Group()
nhom_dan = pygame.sprite.Group()

nguoi_choi = None
dem_sinh_ke = 0.0
elapsed_time = 0.0  # Tổng thời gian chơi (giây)
boss_spawned = False

def bat_dau_vong_moi():
    global tat_ca_sprite, nhom_ke_thu, nhom_dan, nguoi_choi, dem_sinh_ke, elapsed_time, boss_spawned
    tat_ca_sprite.empty(); nhom_ke_thu.empty(); nhom_dan.empty()
    nguoi_choi = NguoiChoi((RONG // 2, CAO // 2), tat_ca_sprite, nhom_dan)
    tat_ca_sprite.add(nguoi_choi)

    # Bắt đầu vòng mới với màn hình trống — kẻ thù sẽ sinh theo thời gian

    dem_sinh_ke = 0.0
    # Reset boss timer/state for new round
    elapsed_time = 0.0
    boss_spawned = False

# Khởi đầu ở menu
menu_tro_choi.state = "menu"
bat_dau_vong_moi()

dang_chay = True
while dang_chay:
    dt = dong_ho.tick(SO_KHUNG_HINH) / 1000.0

    for su_kien in pygame.event.get():
        if su_kien.type == pygame.QUIT:
            dang_chay = False
        if su_kien.type == pygame.KEYDOWN and su_kien.key == pygame.K_ESCAPE:
            dang_chay = False

        # Chuột
        if su_kien.type == pygame.MOUSEBUTTONDOWN:
            if menu_tro_choi.state in ("menu", "gameover"):
                menu_tro_choi.xu_ly_click(su_kien.pos)
                if menu_tro_choi.state == "playing":
                    bat_dau_vong_moi()
            elif menu_tro_choi.state == "playing":
                if su_kien.button == 1 and nguoi_choi:
                    nguoi_choi.ban_vao_chuot()

        # Nạp đạn
        if su_kien.type == pygame.KEYDOWN and menu_tro_choi.state == "playing":
            if su_kien.key == pygame.K_r and nguoi_choi:
                nguoi_choi.bat_dau_nap()

    # Theo trạng thái trò chơi
    if menu_tro_choi.state == "menu":
        menu_tro_choi.ve_menu()

    elif menu_tro_choi.state == "playing":
        # Sinh kẻ thù theo thời gian
        dem_sinh_ke += dt
        if dem_sinh_ke >= KHOANG_SINH_KE_THU:
            dem_sinh_ke = 0.0
            # spawn just outside screen so enemies travel into the visible aread
            margin = 30
            side = random.choice(['left', 'right', 'top', 'bottom'])
            if side == 'left':
                vi_tri = (-margin, random.randint(0, CAO))
            elif side == 'right':
                vi_tri = (RONG + margin, random.randint(0, CAO))
            elif side == 'top':
                vi_tri = (random.randint(0, RONG), -margin)
            else:
                vi_tri = (random.randint(0, RONG), CAO + margin)
            ke_thu = Enemy(vi_tri, nguoi_choi, tat_ca_sprite, nhom_dan)
            nhom_ke_thu.add(ke_thu); tat_ca_sprite.add(ke_thu)

        # Cập nhật
        phim = pygame.key.get_pressed()
        for obj in list(tat_ca_sprite):
            if hasattr(obj, 'update'):
                try:
                    if isinstance(obj, NguoiChoi):
                        obj.cap_nhat(dt, phim)
                    else:
                        obj.update(dt)
                except TypeError:
                    try:
                        obj.update()
                    except:
                        pass

        # Va chạm: đạn người chơi -> kẻ thù, đạn kẻ thù -> người chơi
        for vien_dan in list(nhom_dan): 
            owner = getattr(vien_dan, 'chu_so_huu', None)
            # Đạn của người chơi
            if owner == 'player':
                danh_trung = pygame.sprite.spritecollide(vien_dan, nhom_ke_thu, False)
                if danh_trung:
                    for t in danh_trung:
                        if hasattr(t, 'take_damage'):
                            try:
                                t.take_damage(1)
                            except Exception:
                                t.kill()
                            if getattr(t, 'hp', 1) <= 0:
                                try:
                                    t.set_state('dead')
                                except Exception:
                                    t.kill()
                        else:
                            t.kill()
                    vien_dan.kill()
                    continue

            # Đạn của kẻ thù trúng người chơi
            if owner == 'enemy' and nguoi_choi and vien_dan.rect.colliderect(nguoi_choi.rect):
                vien_dan.kill()
                nguoi_choi.nhan_sat_thuong(1)
                if nguoi_choi.hp <= 0:
                    menu_tro_choi.state = "gameover"

        # Va chạm: kẻ thù chạm người chơi
        if nguoi_choi is not None:
            danh_sach = pygame.sprite.spritecollide(nguoi_choi, nhom_ke_thu, False)
            if danh_sach:
                for t in danh_sach:
                    nguoi_choi.nhan_sat_thuong(1)
                    if hasattr(t, 'take_damage'):
                        try:
                            t.take_damage(1)
                        except Exception:
                            if not hasattr(t, 'hp'):
                                t.kill()
                    else:
                        t.kill()
                if nguoi_choi.hp <= 0:
                    menu_tro_choi.state = "gameover"

        # Vẽ
        man_hinh.fill((30, 30, 30))
        tat_ca_sprite.draw(man_hinh)
        ve_ui(man_hinh, nguoi_choi, phong_chu)

        # Cập nhật thời gian chơi và spawn boss ở phút thứ 5 (300s)
        elapsed_time += dt
        if (not boss_spawned) and elapsed_time >= 300.0:
            boss_spawned = True
            # Sinh boss ở vị trí giữa trên cùng
            vi_tri_boss = (RONG // 2, 80)
            boss = Boss(vi_tri_boss, nguoi_choi, tat_ca_sprite, nhom_dan)
            nhom_ke_thu.add(boss)
            tat_ca_sprite.add(boss)

    elif menu_tro_choi.state == "gameover":
        menu_tro_choi.ve_thua_cuoc()

    pygame.display.flip()

pygame.quit()
sys.exit()
