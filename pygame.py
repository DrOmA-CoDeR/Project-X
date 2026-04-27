import pygame

pygame.init()

# Код, описывающий окно программы
WIDTH = 1080   # Ширина окна
HEIGHT = 940   # Высота окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Создаём контроль FPS
clock = pygame.time.Clock()
FPS = 60  # Увеличил FPS для более плавного движения

# Параметры игрока
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
xp = WIDTH // 2 - PLAYER_WIDTH // 2  # Начальная позиция по центру
yp = 0  # Начальная позиция по Y

# Параметры физики
speed = 10  # Скорость перемещения по горизонтали
jump_power = -15  # Сила прыжка (отрицательная, так как Y растёт вниз)
gravity = 0.8  # Сила гравитации
velocity_y = 0  # Вертикальная скорость

# Флаги движения
move_x = 0  # Флаг движения по Х: 0 - стоит, -1 - влево, 1 - вправо
is_on_ground = True  # Флаг нахождения на земле

# Параметры земли
GROUND_HEIGHT = 100  # Высота земли
ground_y = HEIGHT - GROUND_HEIGHT  # Y координата земли

# Игровой цикл и флаг выполнения программы
game_run = True
while game_run:
    # БЛОК ОБРАБОТКИ СОБЫТИЙ ИГРЫ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        
        # Обработка нажатия клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and is_on_ground:
                velocity_y = jump_power  # Прыжок только если на земле
                is_on_ground = False
            if event.key == pygame.K_s:
                move_y = 1
            if event.key == pygame.K_d:
                move_x = 1
            if event.key == pygame.K_a:
                move_x = -1
            # Можно также добавить прыжок на пробел
            if event.key == pygame.K_SPACE and is_on_ground:
                velocity_y = jump_power
                is_on_ground = False
        
        # Обработка отпускания клавиш
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and move_x == 1:
                move_x = 0
            if event.key == pygame.K_a and move_x == -1:
                move_x = 0
    
    # БЛОК ИГРОВОЙ ЛОГИКИ
    
    # Горизонтальное движение
    xp += speed * move_x
    
    # Вертикальная физика
    velocity_y += gravity  # Добавляем гравитацию к скорости
    yp += velocity_y  # Перемещаем игрока по вертикали
    
    # Коллизия с землёй
    if yp + PLAYER_HEIGHT >= ground_y:
        yp = ground_y - PLAYER_HEIGHT  # Ставим игрока на землю
        velocity_y = 0  # Сбрасываем вертикальную скорость
        is_on_ground = True  # Игрок на земле
    else:
        is_on_ground = False  # Игрок в воздухе
    
    # Коллизия с потолком (опционально)
    if yp <= 0:
        yp = 0
        if velocity_y < 0:
            velocity_y = 0  # Можно раскомментировать, если не хотим прилипать к потолку
    
    # Ограничение движения по горизонтали (чтобы не выходил за края)
    if xp < 0:
        xp = 0
    if xp + PLAYER_WIDTH > WIDTH:
        xp = WIDTH - PLAYER_WIDTH
    
    # ОЧИСТКА ЭКРАНА
    screen.fill((135, 206, 235))  # Голубое небо
    
    # РИСОВАНИЕ ЗЕМЛИ
    pygame.draw.rect(screen, (101, 67, 33), (0, ground_y, WIDTH, GROUND_HEIGHT))  # Коричневая земля
    
    # Добавим траву на землю
    pygame.draw.rect(screen, (34, 139, 34), (0, ground_y, WIDTH, 10))  # Зелёная полоска сверху земли
    
    # РИСОВАНИЕ ИГРОКА
    pygame.draw.rect(screen, (255, 0, 0), (xp, yp, PLAYER_WIDTH, PLAYER_HEIGHT))
    
    
    # ОТОБРАЖЕНИЕ (обновление экрана)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
