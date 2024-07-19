import pygame
import sys
import random

# إعداد pygame
pygame.init()

# إعداد الشاشة
screen_width = 480
screen_height = 320
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("لعبة الطائر")

# إعداد الألوان
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# إعداد الطائر
bird_width = 40
bird_height = 30
bird_x = 50
bird_y = screen_height // 2
bird_velocity_y = 0
gravity = 0.5

# إعداد العقبات
obstacle_width = 50
obstacle_gap = 150
obstacle_velocity = 3

# إعداد الأشرار
enemy_width = 30
enemy_height = 30
enemy_velocity = 3
enemies = []

# إعداد الطلقات
bullet_width = 8
bullet_height = 4
bullets = []
bullet_velocity = 8

# إعداد النقاط
score = 0
level = 1
font = pygame.font.Font(None, 24)

def create_obstacle():
    gap_position = random.randint(50, screen_height - 50 - obstacle_gap)
    return {
        'x': screen_width,
        'top_height': gap_position,
        'bottom_height': screen_height - gap_position - obstacle_gap
    }

def create_enemy(obstacle):
    enemy_x = obstacle['x'] + obstacle_width
    possible_y_positions = []
    if obstacle['top_height'] > enemy_height:
        possible_y_positions.extend(range(0, obstacle['top_height'] - enemy_height + 1))
    if obstacle['bottom_height'] > enemy_height:
        possible_y_positions.extend(range(screen_height - obstacle['bottom_height'], screen_height - enemy_height + 1))
    
    if possible_y_positions:
        enemy_y = random.choice(possible_y_positions)
        return {
            'x': enemy_x,
            'y': enemy_y,
            'width': enemy_width,
            'height': enemy_height
        }
    return None

def create_boss(obstacle):
    boss_x = obstacle['x'] + obstacle_width
    return {
        'x': boss_x,
        'y': screen_height // 2 - 50,
        'width': 80,
        'height': 120
    }

def draw_obstacle(obstacle):
    pygame.draw.rect(screen, green, (obstacle['x'], 0, obstacle_width, obstacle['top_height']))
    pygame.draw.rect(screen, green, (obstacle['x'], screen_height - obstacle['bottom_height'], obstacle_width, obstacle['bottom_height']))

def draw_enemy(enemy):
    pygame.draw.rect(screen, red, (enemy['x'], enemy['y'], enemy['width'], enemy['height']))

def draw_bullet(bullet):
    pygame.draw.rect(screen, black, (bullet['x'], bullet['y'], bullet_width, bullet_height))

def draw_boss(boss):
    pygame.draw.rect(screen, red, (boss['x'], boss['y'], boss['width'], boss['height']))

def draw_score():
    score_text = font.render(f'Score: {score}', True, black)
    screen.blit(score_text, (10, 10))

def draw_level():
    level_text = font.render(f'Level: {level}', True, black)
    screen.blit(level_text, (screen_width - 100, 10))

def check_collision(bird_x, bird_y, obstacle):
    if (bird_x + bird_width > obstacle['x'] and bird_x < obstacle['x'] + obstacle_width):
        if (bird_y < obstacle['top_height'] or bird_y + bird_height > screen_height - obstacle['bottom_height']):
            return True
    return False

def check_enemy_collision(bird_x, bird_y, enemy):
    if (bird_x + bird_width > enemy['x'] and bird_x < enemy['x'] + enemy['width']):
        if (bird_y + bird_height > enemy['y'] and bird_y < enemy['y'] + enemy['height']):
            return True
    return False

def check_bullet_collision(bullet, enemy):
    if (bullet['x'] + bullet_width > enemy['x'] and bullet['x'] < enemy['x'] + enemy['width']):
        if (bullet['y'] + bullet_height > enemy['y'] and bullet['y'] < enemy['y'] + enemy['height']):
            return True
    return False

def reset_game():
    global bird_x, bird_y, bird_velocity_y, current_obstacle, enemies, bullets, score, level, obstacle_velocity, enemy_velocity
    bird_x = 50
    bird_y = screen_height // 2
    bird_velocity_y = 0
    current_obstacle = create_obstacle()
    enemies = []
    for _ in range(2):
        enemy = create_enemy(current_obstacle)
        if enemy:
            enemies.append(enemy)
    bullets = []
    score = 0
    level = 1
    obstacle_velocity = 3
    enemy_velocity = 3

def game_over():
    screen.fill(white)
    game_over_text = font.render(f'Game Over! Score: {score}', True, black)
    restart_text = font.render('Press R to Restart or Q to Quit', True, black)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))
    pygame.display.flip()

def level_up():
    global level, obstacle_velocity, enemy_velocity
    level += 1
    obstacle_velocity += 1
    enemy_velocity += 1

def create_boss_obstacle():
    global current_obstacle, boss
    current_obstacle = create_obstacle()
    boss = create_boss(current_obstacle)

reset_game()

# إعداد المؤقت
clock = pygame.time.Clock()
game_running = True
boss = None

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y < screen_height // 2:
                bird_velocity_y = -10
            else:
                bird_velocity_y = 10
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # إطلاق الطلقات عند الضغط على Enter
                bullets.append({'x': bird_x + bird_width, 'y': bird_y + bird_height // 2})
            elif event.key == pygame.K_r:  # إعادة اللعبة عند الضغط على R
                reset_game()
            elif event.key == pygame.K_q:  # إنهاء اللعبة عند الضغط على Q
                pygame.quit()
                sys.exit()

    if not game_running:
        continue

    # تحديث حركة الطائر
    bird_velocity_y += gravity
    bird_y += bird_velocity_y

    # تحديث حركة العقبة
    current_obstacle['x'] -= obstacle_velocity
    if current_obstacle['x'] < -obstacle_width:
        current_obstacle = create_obstacle()
        enemies = []
        for _ in range(2):
            enemy = create_enemy(current_obstacle)
            if enemy:
                enemies.append(enemy)
        score += 1  # زيادة النقاط عند المرور عبر العقبة

        if score % 5 == 0:
            level_up()

        if level % 5 == 0:
            create_boss_obstacle()

    # تحديث حركة الأشرار
    new_enemies = []
    for enemy in enemies:
        enemy['x'] -= enemy_velocity
        if enemy['x'] > -enemy_width:
            new_enemies.append(enemy)
    enemies = new_enemies

    if len(enemies) < 2 and level % 5 != 0:
        enemy = create_enemy(current_obstacle)
        if enemy:
            enemies.append(enemy)

    # تحديث حركة الطلقات
    new_bullets = []
    for bullet in bullets:
        bullet['x'] += bullet_velocity
        if bullet['x'] < screen_width:
            new_bullets.append(bullet)
    bullets = new_bullets

    # التحقق من التصادم
    if check_collision(bird_x, bird_y, current_obstacle) or bird_y < 0 or bird_y > screen_height - bird_height:
        game_running = False
        game_over()
    for enemy in enemies:
        if check_enemy_collision(bird_x, bird_y, enemy):
            game_running = False
            game_over()
        for bullet in bullets:
            if check_bullet_collision(bullet, enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break
        if boss and check_bullet_collision(bullet, boss):
            bullets.remove(bullet)
            boss = None  # القضاء على الزعيم بعد الاصطدام
            break

    # رسم العناصر
    screen.fill(white)
    pygame.draw.rect(screen, blue, (bird_x, bird_y, bird_width, bird_height))
    draw_obstacle(current_obstacle)
    for enemy in enemies:
        draw_enemy(enemy)
    if boss:
        draw_boss(boss)
    for bullet in bullets:
        draw_bullet(bullet)
    draw_score()
    draw_level()
    
    pygame.display.flip()
    clock.tick(30)  # تحديث الإطار بمعدل 30 إطارًا في الثانية
 