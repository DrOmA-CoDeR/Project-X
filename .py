import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1080, 940
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("СИКСЕЕЕЕЕЕЕЕВЕН: КАРТЕЛЕВИК И ЖЭНЩИНЫ!")

clock = pygame.time.Clock()
FPS = 60  

try:
    pygame.mixer.music.load("gemini_music.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
except:
    pass

MENU_BG, BTN_COLOR, BTN_HOVER = (40, 10, 10), (200, 50, 50), (255, 100, 100)
SKY_TOP, SKY_BOTTOM = (30, 144, 255), (135, 206, 250)

font_title = pygame.font.SysFont("Impact", 72, bold=True)
font_menu = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
font_hud = pygame.font.SysFont("Comic Sans MS", 32, bold=True)
font_meme = pygame.font.SysFont("Impact", 120, bold=True)

# Игрок
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
xp, yp = 100, 0
velocity_y, move_x = 0, 0
speed, jump_power, gravity = 13, -24, 1.05
is_on_ground, is_god_mode, mario_angle = False, False, 0 

GROUND_HEIGHT = 100
ground_y = HEIGHT - GROUND_HEIGHT

camera_x, score = 0, 0
blocks, lucky_blocks, enemies, coins, clouds, fire_particles, text_particles = [], [], [], [], [], [], []
alcoh_enemies, beer_bottles = [], [] 
generated_chunks = set()

# ТЦК и НЛО
tck_bus_x, tck_bus_speed = -50, 6.5       
tck_width, tck_height = 170, 95
tck_bus_y = ground_y - tck_height
ufo_angle, screen_shake, db_earrape_timer = 0, 0, 0
plane_intro_state, plane_x, plane_y = "fly", -150, 200
towers = [{"rect": pygame.Rect(450, 240, 140, 600), "alive": True}, {"rect": pygame.Rect(700, 140, 140, 700), "alive": True}]
tower_debris = []
glitch_timer, weed_smoke_timer, rgb_hue = 0, 0, 0

for _ in range(8):
    clouds.append([random.randint(0, WIDTH), random.randint(30, 300), random.uniform(1.5, 3.5)])

def reset_game():
    global xp, yp, velocity_y, move_x, is_on_ground, camera_x, score, plane_intro_state, plane_x, plane_y, screen_shake, tck_bus_x, tck_bus_y, tck_bus_speed, glitch_timer, weed_smoke_timer, is_god_mode
    xp, yp, velocity_y, move_x, is_god_mode = 150, 0, 0, 0, False
    is_on_ground = False
    camera_x, score, screen_shake, glitch_timer, weed_smoke_timer = 0, 0, 0, 0, 0
    plane_intro_state, plane_x, plane_y = "fly", -150, 200
    tck_bus_x, tck_bus_y, tck_bus_speed = -50, ground_y - tck_height, 6.5
    blocks.clear(); lucky_blocks.clear(); enemies.clear(); coins.clear(); alcoh_enemies.clear(); beer_bottles.clear(); generated_chunks.clear(); tower_debris.clear(); fire_particles.clear(); text_particles.clear()
    for t in towers: t["alive"] = True
    generate_world_chunk(0); generate_world_chunk(1)

def generate_world_chunk(chunk_index):
    if chunk_index in generated_chunks: return
    generated_chunks.add(chunk_index)
    start_x = chunk_index * WIDTH
    if chunk_index == 0:
        lucky_blocks.append({"rect": pygame.Rect(start_x + 950, ground_y - 200, 50, 50), "active": True})
        return
    if random.random() < 0.8:
        blocks.append({"rect": pygame.Rect(start_x + random.randint(100, WIDTH-150), ground_y - random.randint(120, 280), 90, 280), "type": "pipe"})
    for _ in range(random.randint(3, 5)):
        w = random.randint(120, 260)
        px = start_x + random.randint(0, WIDTH - w)
        py = ground_y - random.randint(120, 420)
        blocks.append({"rect": pygame.Rect(px, py, w, 35), "type": "platform"})
        if random.random() < 0.6: lucky_blocks.append({"rect": pygame.Rect(px + w//2 - 25, py - 140, 50, 50), "active": True})
        else: coins.append({"rect": pygame.Rect(px + w//2 - 15, py - 50, 30, 35), "active": True})
    enemies.append({"rect": pygame.Rect(start_x + random.randint(200, WIDTH-50), ground_y - 50, 45, 50), "speed": random.choice([-7, 7]), "alive": True, "jump_timer": random.randint(10, 50)})
    alcoh_enemies.append({"x": start_x + random.randint(200, WIDTH - 200), "y": random.randint(100, 400), "start_y": random.randint(200, 400), "angle": random.uniform(0, 3.14), "shoot_timer": 0})

def update_intro_cutscene():
    global plane_intro_state, plane_x, plane_y, screen_shake, yp, velocity_y
    if plane_intro_state == "done": return
    if plane_intro_state == "fly":
        plane_x += 18; plane_y += 2.5
        if plane_x + 100 >= 450: 
            plane_intro_state = "crash"; screen_shake = 80; pygame.mixer.music.set_volume(1.0)
            for t in towers:
                t["alive"] = False
                for _ in range(40):
                    tower_debris.append({"x": random.randint(t["rect"].left, t["rect"].right), "y": random.randint(t["rect"].top, t["rect"].bottom), "vx": random.uniform(-18, 18), "vy": random.uniform(-28, -6), "w": random.randint(25, 55), "h": random.randint(25, 55)})
            yp, velocity_y = plane_y, -24
    elif plane_intro_state == "crash":
        screen_shake = max(0, screen_shake - 1)
        if screen_shake == 0: plane_intro_state = "done"; pygame.mixer.music.set_volume(0.2)

def trigger_nuke_explosion():
    global screen_shake, db_earrape_timer, weed_smoke_timer
    screen_shake, db_earrape_timer, weed_smoke_timer = 95, 130, 200
    pygame.mixer.music.set_volume(1.0)
    cx, cy = xp + PLAYER_WIDTH // 2, yp + PLAYER_HEIGHT // 2
    for e in enemies: e["alive"] = False
    for lb in lucky_blocks: lb["active"] = False
    for _ in range(15): text_particles.append([xp + random.randint(-200, 200), yp - random.randint(50, 150), 40])
    for _ in range(150): fire_particles.append([cx + random.randint(-150, 150), cy + random.randint(-150, 150), random.uniform(-25, 25), random.uniform(-25, 25), random.randint(20, 50)])

def draw_sky():
    for y in range(0, ground_y):
        f = y / ground_y
        pygame.draw.line(screen, (int(30+(135-30)*f), int(144+(206-144)*f), int(255+(250-255)*f)), (0, y), (WIDTH, y))

def draw_woman(surface, cx, cy):
    pygame.draw.rect(surface, (255, 20, 147), (cx - 12, cy, 24, 25), border_radius=5) 
    pygame.draw.circle(surface, (255, 218, 185), (cx, cy - 8), 9) 
    pygame.draw.ellipse(surface, (255, 255, 0), (cx - 14, cy - 14, 28, 12)) 
    pygame.draw.circle(surface, (255, 0, 0), (cx, cy - 6), 3) 

def draw_drunkard(surface, ax, ay):
    pygame.draw.line(surface, (255, 0, 255), (ax - 30, ay + 30), (ax + 80, ay + 30), 8) 
    pygame.draw.rect(surface, (139, 69, 19), (ax + 8, ay + 20, 34, 32), border_radius=4) 
    pygame.draw.circle(surface, (255, 200, 200), (ax + 25, ay + 10), 16) 
    pygame.draw.circle(surface, (255, 0, 0), (ax + 25, ay + 14), 8) 

def draw_mexican_cartel(surface, ex, ey):
    pygame.draw.rect(surface, (50, 50, 50), (ex, ey + 20, 45, 30)) 
    pygame.draw.circle(surface, (244, 164, 96), (ex + 22, ey + 10), 12) 
    pygame.draw.ellipse(surface, (255, 215, 0), (ex - 15, ey - 2, 75, 12)) 
    pygame.draw.polygon(surface, (255, 215, 0), [(ex + 7, ey - 2), (ex + 37, ey - 2), (ex + 22, ey - 18)])
    pygame.draw.line(surface, (0, 0, 0), (ex + 10, ey + 14), (ex + 34, ey + 14), 4) 

def draw_menu():
    screen.fill(MENU_BG)
    t_text = font_title.render("МЕКСИКАНСКИЙ СИКСЕЕВЕН КАРТЕЛЕВИК", True, (0, 255, 0))
    screen.blit(t_text, t_text.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
    b_start = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2, 500, 90)
    pygame.draw.rect(screen, BTN_HOVER if b_start.collidepoint(pygame.mouse.get_pos()) else BTN_COLOR, b_start, border_radius=25)
    s_txt = font_menu.render("ВХОД В НАРКО-АД", True, (255, 255, 255))
    screen.blit(s_txt, s_txt.get_rect(center=b_start.center))
    pygame.display.flip()
    return b_start

in_menu, game_run = True, True
reset_game()

while game_run:
    if in_menu:
        btn = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and btn.collidepoint(event.pos): in_menu = False; reset_game()
        clock.tick(FPS); continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: in_menu = True
            if plane_intro_state == "done":
                if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and is_on_ground: velocity_y = jump_power; is_on_ground = False
                if event.key == pygame.K_d: move_x = 1
                if event.key == pygame.K_a: move_x = -1
                if event.key == pygame.K_s: trigger_nuke_explosion()
                if event.key == pygame.K_e: is_god_mode = not is_god_mode
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and move_x == 1: move_x = 0
            if event.key == pygame.K_a and move_x == -1: move_x = 0

    update_intro_cutscene()
    current_chunk = int(xp // WIDTH)
    generate_world_chunk(current_chunk); generate_world_chunk(current_chunk + 1)
    
    if plane_intro_state == "fly": xp, yp = plane_x + 40, plane_y + 10
    else:
        if plane_intro_state == "done": xp += speed * move_x
        velocity_y += gravity; yp += velocity_y

    if not is_on_ground and plane_intro_state == "done": mario_angle += 25 
    else: mario_angle = 0

    if plane_intro_state == "done":
        tck_bus_x += tck_bus_speed; tck_bus_speed += 0.005
        ufo_angle += 0.05
        tck_bus_y = (ground_y - tck_height) + math.sin(ufo_angle * 2) * 140
        if mario_rect.colliderect(pygame.Rect(tck_bus_x, tck_bus_y, tck_width, tck_height)) and not is_god_mode: reset_game(); continue

    if plane_intro_state == "done":
        for alk in alcoh_enemies:
            alk["angle"] += 0.09; alk["y"] = alk["start_y"] + math.sin(alk["angle"]) * 220; alk["x"] += math.cos(alk["angle"]) * 6
            alk["shoot_timer"] += 1
            if alk["shoot_timer"] % 5 == 0: beer_bottles.append({"x": alk["x"] + 25, "y": alk["y"] + 30, "vx": random.uniform(-12, 12), "vy": random.uniform(-2, 4)})

        for btl in beer_bottles[:]:
            btl["x"] += btl["vx"]; btl["y"] += 9 
            if pygame.Rect(btl["x"], btl["y"], 25, 35).colliderect(mario_rect) and not is_god_mode: reset_game(); break
            if btl["y"] >= ground_y:
                for _ in range(4): fire_particles.append([btl["x"], ground_y - 5, random.uniform(-8, 8), random.uniform(-12, -4), random.randint(6, 15)])
                beer_bottles.remove(btl)

    screen_shake_val = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
    drunk_wave = math.sin(pygame.time.get_ticks() * 0.008) * 45 
    shift_x = screen_shake_val
    shift_y = int(screen_shake_val + drunk_wave)
    if screen_shake > 0: screen_shake -= 1
    if db_earrape_timer > 0:
        db_earrape_timer -= 1
        if db_earrape_timer == 0: pygame.mixer.music.set_volume(0.2)

    target_cam = xp - 250
    camera_x += (target_cam - camera_x) * 0.1
    camera_x = max(0, camera_x)
    if xp < camera_x: xp = camera_x

    mario_rect = pygame.Rect(xp, yp, PLAYER_WIDTH, PLAYER_HEIGHT)
    is_on_ground = False
    if yp + PLAYER_HEIGHT >= ground_y: yp = ground_y - PLAYER_HEIGHT; velocity_y = 0; is_on_ground = True

    for d in tower_debris:
        d["x"] += d["vx"]; d["y"] += d["vy"]; d["vy"] += 0.5
        if d["y"] + d["h"] > ground_y: d["y"] = ground_y - d["h"]; d["vx"] *= 0.5

    for b in blocks:
        br = b["rect"]
        if mario_rect.colliderect(br):
            if velocity_y > 0 and yp + PLAYER_HEIGHT - velocity_y <= br.top + 12: yp = br.top - PLAYER_HEIGHT; velocity_y = 0; is_on_ground = True
            elif velocity_y < 0 and yp - velocity_y >= br.bottom - 12: yp = br.bottom; velocity_y = 0
            elif move_x > 0: xp = br.left - PLAYER_WIDTH
            elif move_x < 0: xp = br.right

    for lb in lucky_blocks:
        lbr = lb["rect"]
        if mario_rect.colliderect(lbr):
            if velocity_y > 0 and yp + PLAYER_HEIGHT - velocity_y <= lbr.top + 10: yp = lbr.top - PLAYER_HEIGHT; velocity_y = 0; is_on_ground = True
            elif velocity_y < 0 and yp - velocity_y >= lbr.bottom - 12:
                yp = lbr.bottom; velocity_y = 0
                if lb["active"]:
                    lb["active"] = False; score += 1
                    for _ in range(3): text_particles.append([lbr.centerx + random.randint(-60, 60), lbr.top - 40, 40])

    for c in coins:
        if c["active"] and mario_rect.colliderect(c["rect"]): c["active"] = False; score += 1; glitch_timer = 6; weed_smoke_timer = 60 

    for e in enemies:
        if not e["alive"]: continue
        e["rect"].x += e["speed"]
        e["jump_timer"] -= 1
        if e["jump_timer"] <= 0: e["jump_timer"] = random.randint(20, 60); e["rect"].y -= 350 
        if e["rect"].y + 50 < ground_y: e["rect"].y += 7
        else: e["rect"].y = ground_y - 50
        if mario_rect.colliderect(e["rect"]):
            if velocity_y > 0 and yp + PLAYER_HEIGHT - velocity_y <= e["rect"].top + 15: e["alive"] = False; velocity_y = -16
            elif not is_god_mode: reset_game(); break

    rgb_hue = (rgb_hue + 7) % 255
    rgb_color = pygame.Color(0)
    rgb_color.hsva = (rgb_hue, 100, 100, 100)

    if db_earrape_timer > 0: screen.fill((random.randint(0,255), random.randint(0,255), 0)) 
    else: draw_sky()
    pygame.draw.circle(screen, (255, 0, 0), (WIDTH - 120 + shift_x, 120 + shift_y), 60) 
    
    # Отрисовка летящих дымящих косяков
    for idx in range(len(clouds)):
        clouds[idx][0] -= clouds[idx][2]
        if clouds[idx][0] < -100:
            clouds[idx][0] = WIDTH + 100
            clouds[idx][1] = random.randint(30, 300)
        cx, cy = int(clouds[idx][0] + shift_x), int(clouds[idx][1] + shift_y)
        pygame.draw.rect(screen, (210, 180, 140), (cx, cy, 70, 15), border_radius=2)
        pygame.draw.rect(screen, (255, 69, 0), (cx + 65, cy, 8, 15)) 
        pygame.draw.circle(screen, (220, 220, 220, 150), (cx + 80, cy - 5), 10)

    for t in towers:
        if t["alive"]: pygame.draw.rect(screen, (0,0,0), t["rect"].move(-camera_x + shift_x, shift_y))
    for d in tower_debris: pygame.draw.rect(screen, rgb_color, (int(d["x"] - camera_x + shift_x), int(d["y"] + shift_y), d["w"], d["h"]))

    if plane_intro_state == "fly": pygame.draw.rect(screen, (255, 0, 0), (int(plane_x - camera_x + shift_x), int(plane_y + shift_y), 110, 40))

    for b in blocks: pygame.draw.rect(screen, rgb_color, b["rect"].move(-camera_x + shift_x, shift_y))
    for lb in lucky_blocks: pygame.draw.rect(screen, (255, 255, 0) if lb["active"] else (0,0,0), lb["rect"].move(-camera_x + shift_x, shift_y))
    
    for c in coins:
        if c["active"]: draw_woman(screen, int(c["rect"].centerx - camera_x + shift_x), int(c["rect"].centery + shift_y))
    for e in enemies:
        if e["alive"]: draw_mexican_cartel(screen, int(e["rect"].x - camera_x + shift_x), int(e["rect"].y + shift_y))

    for alk in alcoh_enemies:
        if alk["x"] + WIDTH > camera_x and alk["x"] - WIDTH < camera_x: draw_drunkard(screen, int(alk["x"] - camera_x + shift_x), int(alk["y"] + shift_y))
    for btl in beer_bottles: pygame.draw.circle(screen, (0, 255, 0), (int(btl["x"] - camera_x + shift_x + 10), int(btl["y"] + shift_y + 15)), 14)

    if plane_intro_state == "done":
        bx, by = int(tck_bus_x - camera_x + shift_x), int(tck_bus_y + shift_y)
        ux, uy = bx + tck_width // 2, by - 250
        ufo_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(ufo_surface, (0, 255, 0, 70), [(ux - 40, uy + 20), (ux + 40, uy + 20), (bx + tck_width, by + tck_height), (bx, by + tck_height)])
        screen.blit(ufo_surface, (0, 0))
        pygame.draw.ellipse(screen, (255, 0, 255), (ux - 60, uy, 120, 40))
        pygame.draw.circle(screen, (0, 200, 255), (ux, uy + 5), 20) 
        pygame.draw.rect(screen, (255, 255, 255), (bx, by, tck_width, tck_height), border_radius=10)
        screen.blit(font_title.render("ТЦК", True, (255, 0, 0)), (bx + 20, by + 5))
        flashlight_color = (255, 0, 0) if pygame.time.get_ticks() % 160 < 80 else (0, 0, 255)
        pygame.draw.rect(screen, flashlight_color, (bx + 40, by - 30, tck_width - 80, 30), border_radius=5)

    # Море алкоголя (RGB Земля)
    start_tile = int(camera_x // WIDTH) * WIDTH
    for offset_x in [start_tile, start_tile + WIDTH, start_tile + WIDTH * 2]:
        pygame.draw.rect(screen, rgb_color, (offset_x - camera_x + shift_x, ground_y + shift_y, WIDTH, GROUND_HEIGHT))

    if plane_intro_state != "fly":
        mario_surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        mario_color = (255, 215, 0) if is_god_mode else (255, 0, 255)
        pygame.draw.polygon(mario_surf, mario_color, [(25, 0), (0, 50), (50, 50)])
        pygame.draw.circle(mario_surf, (255, 255, 255), (25, 30), 12) 
        pygame.draw.circle(mario_surf, (0, 0, 0), (25, 30), 5)
        rotated_mario = pygame.transform.rotate(mario_surf, mario_angle)
        new_rect = rotated_mario.get_rect(center=(int(xp - camera_x + shift_x + 25), int(yp + shift_y + 25)))
        screen.blit(rotated_mario, new_rect.topleft)
        if is_god_mode: pygame.draw.circle(screen, (255, 255, 0), new_rect.center, 40, 3)

    # --- ИСПРАВЛЕННЫЙ И РАЗДЕЛЕННЫЙ ЦИКЛ ЭФФЕКТОВ ---
    # Огненные частицы
    for p in fire_particles[:]:
        p[0] += p[2]; p[1] += p[3]; p[4] -= 0.5
        if p[4] <= 0: fire_particles.remove(p)
        else: pygame.draw.circle(screen, rgb_color, (int(p[0] - camera_x + shift_x), int(p[1] + shift_y)), int(p[4] * 0.4))
        
    # Текстовые частицы "СИКСЕЕЕЕВЕН"
    for pt in text_particles[:]:
        pt[1] -= 3; pt[2] -= 1
        if pt[2] <= 0: text_particles.remove(pt)
        else:
            m_txt = font_meme.render("СИКСЕЕЕЕЕЕЕЕВЕН!!", True, (random.randint(180, 255), 255, 0))
            screen.blit(m_txt, (int(pt[0] - camera_x + shift_x - 120), int(pt[1] + shift_y)))

    if weed_smoke_timer > 0:
        smoke_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        smoke_surf.fill((0, 200, 0, 80)) 
        screen.blit(smoke_surf, (0, 0))
        weed_smoke_timer -= 1

    if glitch_timer > 0: pygame.draw.rect(screen, (0, 255, 0), (0, 0, WIDTH, HEIGHT)); glitch_timer -= 1

    screen.blit(font_hud.render(f"ЖЭНЩИНЫ В КАРТЕЛЕ: {score}", True, (255, 255, 255)), (30, 25))
    if is_god_mode: screen.blit(font_hud.render("БЕЗУМНЫЙ ЧИТ АКТИВИРОВАН", True, (255, 215, 0)), (WIDTH - 450, 25))
        
    pygame.display.flip(); clock.tick(FPS)

pygame.quit()
sys.exit()
