# ui.py
import pygame

def ve_ui(man_hinh, nguoi_choi, phong_chu):
    # Máu: vẽ 3 ô ở góc trái trên
    for i in range(nguoi_choi.max_hp):
        x = 10 + i * 40
        hcn = pygame.Rect(x, 10, 34, 34)
        mau = (200, 0, 0) if i < nguoi_choi.hp else (80, 80, 80)
        pygame.draw.rect(man_hinh, mau, hcn)
        pygame.draw.rect(man_hinh, (0, 0, 0), hcn, 2)

    # Đạn: hiển thị băng + dự trữ + trạng thái nạp
    chu_dan = f"Băng: {nguoi_choi.magazine}/{nguoi_choi.magazine_size}  |  Dự trữ: {nguoi_choi.reserve}"
    be_mat_chu = phong_chu.render(chu_dan, True, (255, 255, 255))
    man_hinh.blit(be_mat_chu, (10, 54))

    if nguoi_choi.reloading:
        t = phong_chu.render("Đang nạp...", True, (255, 200, 0))
        man_hinh.blit(t, (10, 84))

# Alias tiếng Anh để tương thích
draw_ui = ve_ui
