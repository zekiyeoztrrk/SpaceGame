import pygame
from bullet import Bullet
from settings import player_width, player_height, player_speed, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN

class Player(pygame.sprite.Sprite):
    def __init__(self, image, shoot_sound):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(image, (player_width, player_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2 
        self.rect.bottom = SCREEN_HEIGHT - 10 
        self.speed_x = 0
        self.mask = pygame.mask.from_surface(self.image)  # Mask oluştur
        self.shoot_sound = shoot_sound

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -player_speed
        if keys[pygame.K_RIGHT]:
            self.speed_x = player_speed

        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        self.shoot_sound.play()  # Atış sesi
