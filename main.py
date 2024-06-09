import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 700, 800
ROAD_WIDTH = 400
CAR_WIDTH, CAR_HEIGHT = 50, 100
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 100
FPS = 60
INITIAL_ENEMY_SPEED = 5

# Цвета
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Гонка по встречке')

# Шрифт
font = pygame.font.Font(None, 36)

# Классы
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > (WIDTH - ROAD_WIDTH) // 2:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < (WIDTH + ROAD_WIDTH) // 2:
            self.rect.x += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(random.choice(COLORS))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint((WIDTH - ROAD_WIDTH) // 2, (WIDTH + ROAD_WIDTH) // 2 - ENEMY_WIDTH)
        self.rect.y = -ENEMY_HEIGHT
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Основная функция
def main():
    clock = pygame.time.Clock()
    running = True
    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    enemy_speed = INITIAL_ENEMY_SPEED
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 1000)
    evade_count = 0
    collision_count = 0
    pause = False
    pause_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == spawn_event and not pause:
                enemy = Enemy(enemy_speed)
                enemies.add(enemy)
                all_sprites.add(enemy)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not pause:
            all_sprites.update()
            if pygame.sprite.spritecollide(player, enemies, True):
                collision_count += 1
                pause = True
                pause_timer = pygame.time.get_ticks()
            else:
                evade_count += len([enemy for enemy in enemies if enemy.rect.top > HEIGHT])
                enemies = pygame.sprite.Group([enemy for enemy in enemies if enemy.rect.top <= HEIGHT])
                all_sprites = pygame.sprite.Group(player, enemies)
        else:
            if pygame.time.get_ticks() - pause_timer > 3000:
                pause = False
                enemy_speed += 1

        screen.fill(WHITE)
        pygame.draw.rect(screen, DARK_BLUE, ((WIDTH - ROAD_WIDTH) // 2, 0, ROAD_WIDTH, HEIGHT))
        all_sprites.draw(screen)
        score_text = font.render(f'Аварий:{collision_count}', True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 10))
        if pause:
            collision_text = font.render('АВАРИЯ', True, BLACK)
            screen.blit(collision_text, (WIDTH // 2 - collision_text.get_width() // 2, HEIGHT // 2 - collision_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()