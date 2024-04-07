import pygame
import random
pygame.init()

W, H = 1200, 800
FPS = 60

clock = pygame.time.Clock()
speed_increase_rate = 0.00001

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
bg = (0, 0, 0)

white = (255, 255, 255)
# Paddle
paddleW = 300
paddleH = 25
paddleSpeed = 20
paddlepos1 = W // 2 - paddleW // 2
paddlepos2 = H - paddleH - 30 
paddle = pygame.Rect(paddlepos1, paddlepos2, paddleW, paddleH)

# Ball
ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Game score
game_score = 0
game_score_fonts = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (0, 0, 0))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    if delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

# Sounds
collision_sound = pygame.mixer.Sound('catch.mp3')
unbreakable_sound = pygame.mixer.Sound('unbreak.mp3')

# Block settings
block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) for _ in range(len(block_list))]
unbreakable_list = [pygame.Rect(10 + 250 * i, 350 + 30 * j, 100, 50) for i in range(5) for j in range(1)]

# Game over screen
losefont = pygame.font.SysFont('comicsansms', 40)
losetext = losefont.render('Game Over', True, (255, 255, 255))
losetextRect = losetext.get_rect()
losetextRect.center = (W // 2, H // 2)

# Win screen
winfont = pygame.font.SysFont('comicsansms', 40)
wintext = winfont.render('You win yay', True, (0, 0, 0))
wintextRect = wintext.get_rect()
wintextRect.center = (W // 2, H // 2)

# Menu buttons
menu_font = pygame.font.SysFont('comicsansms', 60)
menu_options = ['Resume', 'Exit']
menu_texts = [menu_font.render(option, True, white) for option in menu_options]
menu_rects = [text.get_rect(center=(W // 2, H // 2 + i * 100)) for i, text in enumerate(menu_texts)]



# Game state
running = True
paused = True
menu_active = True
move_left = move_right = False

while running:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and menu_active:
            mouse_pos = pygame.mouse.get_pos()
            for index, rect in enumerate(menu_rects):
                if rect.collidepoint(mouse_pos):
                    if index == 0:
                        paused = False
                        menu_active = False
                    elif index == 1:
                        running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            # Press p to pause the game
            elif event.key == pygame.K_p:
                paused = True
                menu_active = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    # Update paddle position based on key state
    if move_left and paddle.left > 0:
         paddle.right -= paddleSpeed
         paddlepos1 -= paddleSpeed
    if move_right and paddle.right < W:
        paddle.right += paddleSpeed
        paddlepos1 += paddleSpeed
        
        

    if paused:
        screen.fill(bg)
        for index, text in enumerate(menu_texts):
            screen.blit(text, menu_rects[index])
        pygame.display.flip()
        continue

    screen.fill(bg)

    [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
    [pygame.draw.rect(screen, pygame.Color(255, 255, 255), unbreakable) for unbreakable in unbreakable_list]
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle)
    pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ballRadius)

    # Ball movement
    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy

    # Collision with walls and paddle
    if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
        dx = -dx
    if ball.centery < ballRadius + 50:
        dy = -dy
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    # Collision with blocks
    hitIndex = ball.collidelist(block_list)
    if hitIndex != -1:
        hitRect = block_list.pop(hitIndex)
        color_list.pop(hitIndex)
        dx, dy = detect_collision(dx, dy, ball, hitRect)
        game_score += 1
        collision_sound.play()
        paddleW -= 5
        paddle = pygame.Rect(paddlepos1, paddlepos2, paddleW, paddleH)

    # Collision with unbreakable bricks
    hit_unbreakable = ball.collidelist(unbreakable_list)
    if hit_unbreakable != -1:
        dx, dy = detect_collision(dx, dy, ball, unbreakable_list[hit_unbreakable])
        unbreakable_sound.play()

    # Check game over or win condition
    if ball.bottom > H:
        screen.fill((0, 0, 0))
        screen.blit(losetext, losetextRect)
    elif not len(block_list):
        screen.fill((255, 255, 255))
        screen.blit(wintext, wintextRect)

    # Update game score text
    game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
    screen.blit(game_score_text, game_score_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()