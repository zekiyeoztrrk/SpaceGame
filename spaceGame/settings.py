# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Uzay gemisi ayarları
player_width = 50
player_height = 75
player_speed = 5

# Düşman ayarları
enemy_width = 50
enemy_height = 60
enemy_speed = 3

# Atış ayarları
bullet_width = 5
bullet_height = 10
bullet_speed = 7

# Zorluk seviyeleri
difficulty_increase_interval = 5000  # Zorluk artış aralığı 
last_difficulty_increase = 0

# Zorluk seviyeleri ve ayarları
difficulty_levels = ["Kolay", "Orta", "Zor"]
difficulty_settings = [
    {"enemy_count": 3, "enemy_speed": 1},  # Kolay
    {"enemy_count": 5, "enemy_speed": 2},  # Orta
    {"enemy_count": 7, "enemy_speed": 3},  # Zor
]
difficulty_index = 1  # Varsayılan zorluk "Orta"

# Başlangıç düşman sayısı ve hız
initial_enemy_count = difficulty_settings[difficulty_index]["enemy_count"]
initial_enemy_speed = difficulty_settings[difficulty_index]["enemy_speed"]
current_enemy_speed = initial_enemy_speed
current_enemy_count = initial_enemy_count

# Ses ayarları
volume = 0.5  # Varsayılan ses düzeyi

# Resim dosyaları için yollar
PLAYER_IMAGE_PATH = "images/pngwing.com-2.png"
ENEMY_IMAGE_PATH = "images/pngwing.com-4.png"
BACKGROUND_IMAGE_PATH = "images/HuGGeENt6kGyixe3hT9tnY.jpg"

# Skor dosyası yolu
HIGH_SCORE_FILE = "high_score.txt"

# Ses dosyaları için yollar
SHOOT_SOUND_PATH = "sounds/laser-104024.mp3"
ENEMY_HIT_SOUND_PATH = "sounds/rock-break-183794.mp3"
MUSIC_PATH = "sounds/The Legend of Zelda - A Link To The Past - Select Screen.mp3"
