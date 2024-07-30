import pygame
import os
from settings import *
from player import Player
from enemy import Enemy

# Pygame'i başlat
pygame.init()
pygame.mixer.init()  # Pygame mixer'ı başlat

# Ses dosyalarını yükle
shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)
enemy_hit_sound = pygame.mixer.Sound(ENEMY_HIT_SOUND_PATH)
shoot_sound.set_volume(volume)
enemy_hit_sound.set_volume(volume)

# Müziği yükle ve çal
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)  # Sonsuz döngüde çal

# Ekran oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Uzay Oyunu")

# Resimleri yükle
player_image = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
enemy_image = pygame.image.load(ENEMY_IMAGE_PATH).convert_alpha()
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()

# Saat
clock = pygame.time.Clock()

def load_high_score():
    if not os.path.isfile(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as file:
        try:
            return int(file.read().strip())
        except ValueError:
            return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

def reset_game():
    global all_sprites, enemies, bullets, player, score, current_enemy_speed, current_enemy_count, last_difficulty_increase

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player(player_image, shoot_sound)
    all_sprites.add(player)

    current_enemy_speed = difficulty_settings[difficulty_index]["enemy_speed"]
    current_enemy_count = difficulty_settings[difficulty_index]["enemy_count"]

    for _ in range(current_enemy_count):
        enemy = Enemy(enemy_image, current_enemy_speed, enemies)
        all_sprites.add(enemy)
        enemies.add(enemy)

    score = 0
    last_difficulty_increase = pygame.time.get_ticks()

def game_loop():
    global running, high_score, score, last_difficulty_increase, current_enemy_speed, current_enemy_count

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets)

        all_sprites.update()
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            enemy_hit_sound.play()  # Düşman vurulma sesi
            enemy = Enemy(enemy_image, current_enemy_speed, enemies)
            all_sprites.add(enemy)
            enemies.add(enemy)

        current_time = pygame.time.get_ticks()
        if current_time - last_difficulty_increase > difficulty_increase_interval:
            last_difficulty_increase = current_time
            current_enemy_speed += 0.5
            if current_enemy_count < 10:
                enemy = Enemy(enemy_image, current_enemy_speed, enemies)
                all_sprites.add(enemy)
                enemies.add(enemy)
                current_enemy_count += 1

        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
            running = False

        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))  # Arka plan görüntüsünü ekrana çiz
        all_sprites.draw(screen)
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(60)

    if score > high_score:
        high_score = score
        save_high_score(high_score)

def game_over_screen():
    font_large = pygame.font.SysFont(None, 72)
    text_large = font_large.render("Game Over", True, RED)
    text_rect = text_large.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_large, text_rect)

    font_medium = pygame.font.SysFont(None, 48)
    text_medium = font_medium.render(f"Score: {score}", True, WHITE)
    text_rect_medium = text_medium.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text_medium, text_rect_medium)

    font_small = pygame.font.SysFont(None, 36)
    high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(high_score_text, high_score_rect)

    try_again_text = font_small.render("Press 'R' to Try Again", True, WHITE)
    try_again_rect = try_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(try_again_text, try_again_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
    return False

def settings_screen():
    global volume, difficulty_index
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    
    settings_running = True
    while settings_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and volume < 1.0:
                    volume += 0.1
                    pygame.mixer.music.set_volume(volume)
                    shoot_sound.set_volume(volume)
                    enemy_hit_sound.set_volume(volume)
                elif event.key == pygame.K_DOWN and volume > 0.0:
                    volume -= 0.1
                    pygame.mixer.music.set_volume(volume)
                    shoot_sound.set_volume(volume)
                    enemy_hit_sound.set_volume(volume)
                elif event.key == pygame.K_RIGHT:
                    difficulty_index = (difficulty_index + 1) % len(difficulty_levels)
                elif event.key == pygame.K_LEFT:
                    difficulty_index = (difficulty_index - 1) % len(difficulty_levels)
                elif event.key == pygame.K_b:
                    settings_running = False

        # Ses düzeyi ve zorluk seviyesi metinlerini güncelle
        volume_text = font.render(f"Ses Düzeyi: {int(volume * 100)}", True, WHITE)
        difficulty_text = font.render(f"Zorluk: {difficulty_levels[difficulty_index]}", True, WHITE)
        back_text = small_font.render("Geri Dön (B)", True, WHITE)

        volume_rect = volume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        screen.fill(BLACK)
        screen.blit(volume_text, volume_rect)
        screen.blit(difficulty_text, difficulty_rect)
        screen.blit(back_text, back_rect)
        pygame.display.flip()

    # Yeni zorluk ayarlarını uygula
    reset_game()
    return True

def main_menu():
    font = pygame.font.SysFont(None, 72)
    text = font.render("Uzay Oyunu", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    play_text = font.render("Oyna (O)", True, GREEN)
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    settings_text = font.render("Ayarlar (A)", True, BLUE)
    settings_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    return True
                elif event.key == pygame.K_a:
                    if not settings_screen():
                        return False

        screen.fill(BLACK)
        screen.blit(text, text_rect)
        screen.blit(play_text, play_rect)
        screen.blit(settings_text, settings_rect)
        pygame.display.flip()

    return False

def main():
    global high_score
    high_score = load_high_score()
    while True:
        if not main_menu():
            break
        reset_game()
        game_loop()
        if not game_over_screen():
            break

    pygame.quit()

if __name__ == "__main__":
    main()
