# cau_hinh.py - Cấu hình trò chơi

# Kích thước và tốc độ khung hình
RONG = 800
CAO = 600
SO_KHUNG_HINH = 60

# Thời gian sinh kẻ thù
KHOANG_SINH_KE_THU = 2.0  # giây

# Cài đặt người chơi
TOC_DO_NGUOI_CHOI = 240        # px/giây
MAU_TOI_DA_NGUOI_CHOI = 3
SUC_CHUA_BANG_DAN = 10         # Sức chứa 1 băng
DAN_DU_TRU_TOI_DA = 30         # Đạn dự trữ tối đa

# Nạp đạn
THOI_GIAN_NAP_DAN = 0.9        # giây

# Đạn
TOC_DO_DAN = 300               # px/giây
TOC_DO_DAN_KE_THU = 200

# Kẻ thù
TOC_DO_KE_THU = 80             # px/giây
KHOANG_BAN_KE_THU_TOI_THIEU = 1.2
KHOANG_BAN_KE_THU_TOI_DA = 3.0
# Tỷ lệ scale mặc định cho sprite kẻ thù (1.0 = nguyên bản, <1 nhỏ hơn)
ENEMY_SCALE = 0.4

# Alias giữ tương thích với mã hiện tại (tiếng Anh)
WIDTH = RONG
HEIGHT = CAO
FPS = SO_KHUNG_HINH

ENEMY_SPAWN_INTERVAL = KHOANG_SINH_KE_THU

PLAYER_SPEED = TOC_DO_NGUOI_CHOI
PLAYER_MAX_HP = MAU_TOI_DA_NGUOI_CHOI
PLAYER_MAGAZINE = SUC_CHUA_BANG_DAN
PLAYER_RESERVE_MAX = DAN_DU_TRU_TOI_DA

RELOAD_TIME = THOI_GIAN_NAP_DAN

BULLET_SPEED = TOC_DO_DAN
ENEMY_BULLET_SPEED = TOC_DO_DAN_KE_THU

ENEMY_SPEED = TOC_DO_KE_THU
ENEMY_SHOOT_INTERVAL_MIN = KHOANG_BAN_KE_THU_TOI_THIEU
ENEMY_SHOOT_INTERVAL_MAX = KHOANG_BAN_KE_THU_TOI_DA
# Export alias
ENEMY_SPRITE_SCALE = ENEMY_SCALE
