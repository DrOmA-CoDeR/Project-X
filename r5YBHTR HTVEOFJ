import pygame
import sys
import random

# Инициализация Pygame и звукового движка
pygame.init()
pygame.mixer.init() # Важно: запускаем микшер звуков

# Код, описывающий окно программы
WIDTH = 1080   
HEIGHT = 940   
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Марио на Pygame — Со звуком!")

# Создаём контроль FPS
clock = pygame.time.Clock()
FPS = 60  

# --- ЗАГРУЗКА И НАСТРОЙКА ЗВУКОВ ---
# Безопасная загрузка аудио (чтобы игра не вылетала, если файлов нет)
try:
    # Загружаем фоновую музыку
    pygame.mixer.music.load("gemini_music.mp3")
    # Устанавливаем громкость (от 0.0 до 1.0)
    pygame.mixer.music.set_volume(0.2)
    # Запускаем бесконечное воспроизведение (-1 означает зацикливание)
    pygame.mixer.music.play(-1)
    

except pygame.error:
    print("Предупреждение: Аудиофайлы не найдены. Игра запущена без звука.")
    music_loaded = False
# --------------------------------------------

# Цветовая палитра для визуала
SKY_TOP = (30, 144, 255)     
SKY_BOTTOM = (135, 206, 250)  
TEXT_COLOR = (255, 255, 255)
MENU_BG = (20, 20, 40)
BTN_COLOR = (70, 130, 180)
BTN_HOVER_COLOR = (100, 149, 237)

# Инициализация шрифтов
font_title = pygame.font.SysFont("Arial", 64, bold=True)
font_menu = pygame.font.SysFont("Arial", 36, bold=True)

# Параметры игрока
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
xp = WIDTH // 2 - PLAYER_WIDTH // 2  
yp = 0  

# --- ЗАГРУЗКА И НАСТРОЙКА КАРТИНОК ИГРОКА ---
try:
    mario_right_img = pygame.image.load("бегright.png").convert_alpha()
    mario_right = pygame.transform.scale(mario_right_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    mario_left = pygame.transform.flip(mario_right, True, False)
except pygame.error:
    mario_right = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(mario_right, (255, 0, 0), (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT), border_radius=8)
    pygame.draw.circle(mario_right, (255, 255, 0), (40, 15), 6) 
    mario_left = pygame.transform.flip(mario_right, True, False)

current_sprite = mario_right

# Параметры физики
speed = 10  
jump_power = -16  
gravity = 0.8  
velocity_y = 0  

# Флаги движения
move_x = 0  
is_on_ground = True  

# Параметры земли
GROUND_HEIGHT = 100  
ground_y = HEIGHT - GROUND_HEIGHT  

# --- ДЕКОРАЦИИ И ЭФФЕКТЫ ---
clouds = []
for _ in range(5):
    cx = random.randint(0, WIDTH)
    cy = random.randint(50, 250)
    c_speed = random.uniform(0.2, 0.6)
    clouds.append([cx, cy, c_speed])

particles = []

def draw_sky_gradient():
    for y in range(0, ground_y):
        color_factor = y / ground_y
        r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * color_factor)
        g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * color_factor)
        b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * color_factor)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def draw_clouds():
    for cloud in clouds:
        cloud[0] -= cloud[2]  
        if cloud[0] < -100:
            cloud[0] = WIDTH + 100
            cloud[1] = random.randint(50, 250)
        pygame.draw.circle(screen, (255, 255, 255, 200), (int(cloud[0]), cloud[1]), 35)
        pygame.draw.circle(screen, (255, 255, 255, 200), (int(cloud[0] - 25), cloud[1] + 5), 25)
        pygame.draw.circle(screen, (255, 255, 255, 200), (int(cloud[0] + 25), cloud[1] + 5), 25)

def update_particles():
    if move_x != 0 and is_on_ground:
        if random.random() < 0.4:  
            px = xp + PLAYER_WIDTH // 2 if move_x == -1 else xp
            py = yp + PLAYER_HEIGHT
            particles.append([px, py, random.uniform(-2, 2), random.uniform(-1, -3), 8])
            
    for p in particles[:]:
        p[0] += p[2]  
        p[1] += p[3]  
        p[4] -= 0.2   
        if p[4] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(screen, (240, 240, 240), (int(p[0]), int(p[1])), int(p[4]))

def draw_menu():
    screen.fill(MENU_BG)
    title_text = font_title.render("SUPER MARIO", True, (255, 69, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title_text, title_rect)
    
    btn_start_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
    btn_exit_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 90, 300, 60)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if btn_start_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BTN_HOVER_COLOR, btn_start_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, BTN_COLOR, btn_start_rect, border_radius=10)
        
    if btn_exit_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (220, 20, 60), btn_exit_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, (178, 34, 34), btn_exit_rect, border_radius=10)
        
    start_text = font_menu.render("Играть", True, TEXT_COLOR)
    exit_text = font_menu.render("Выход", True, TEXT_COLOR)
    
    screen.blit(start_text, start_text.get_rect(center=btn_start_rect.center))
    screen.blit(exit_text, exit_text.get_rect(center=btn_exit_rect.center))
    
    pygame.display.flip()
    return btn_start_rect, btn_exit_rect

# --- ГЛАВНЫЙ СТРУКТУРНЫЙ ЦИКЛ ---
in_menu = True
game_run = True

while game_run:
    if in_menu:
        btn_start, btn_exit = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_start.collidepoint(event.pos):
                    in_menu = False  
                if btn_exit.collidepoint(event.pos):
                    game_run = False
        clock.tick(FPS)
        continue

    # БЛОК ОБРАБОТКИ СОБЫТИЙ ИГРЫ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  
                in_menu = True
            
            # Прыжок на W
            if event.key == pygame.K_w and is_on_ground:
                velocity_y = jump_power  
                is_on_ground = False                
            # Прыжок на ПРОБЕЛ
            if event.key == pygame.K_SPACE and is_on_ground:
                velocity_y = jump_power
                is_on_ground = False                
            if event.key == pygame.K_d:
                move_x = 1
                current_sprite = mario_right  
            if event.key == pygame.K_a:
                move_x = -1
                current_sprite = mario_left   

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and move_x == 1:
                move_x = 0
            if event.key == pygame.K_a and move_x == -1:
                move_x = 0
    
    # БЛОК ИГРОВОЙ ЛОГИКИ
    xp += speed * move_x
    velocity_y += gravity  
    yp += velocity_y  
    
    if yp + PLAYER_HEIGHT >= ground_y:
        yp = ground_y - PLAYER_HEIGHT  
        velocity_y = 0  
        is_on_ground = True  
    else:
        is_on_ground = False  
    
    if yp <= 0:
        yp = 0
        if velocity_y < 0:
            velocity_y = 0  
    
    if xp < 0:
        xp = 0
    if xp + PLAYER_WIDTH > WIDTH:
        xp = WIDTH - PLAYER_WIDTH
    
    # --- РЕНДЕР СЦЕНЫ ---
    draw_sky_gradient()  
    pygame.draw.circle(screen, (255, 223, 0), (WIDTH - 120, 120), 50)
    pygame.draw.circle(screen, (255, 255, 150, 100), (WIDTH - 120, 120), 65, 4) 
    
    draw_clouds()        
    update_particles()   
    
    pygame.draw.rect(screen, (101, 67, 33), (0, ground_y, WIDTH, GROUND_HEIGHT))  
    pygame.draw.rect(screen, (34, 139, 34), (0, ground_y, WIDTH, 18), border_radius=2)   
    pygame.draw.rect(screen, (50, 205, 50), (0, ground_y, WIDTH, 6))   
    
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, (139, 69, 19), (i, ground_y + 30), (i + 10, ground_y + 45), 3)

    screen.blit(current_sprite, (xp, yp))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
