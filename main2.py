import pygame
import sys

# Setup
pygame.init()
pygame.mixer.init() # INITIALIZE SOUND MIXER
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick game ")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
large_font = pygame.font.SysFont("Arial", 60)

# --- LOAD SOUNDS --
try:
    hit_sound = pygame.mixer.Sound('audio/Boom9.wav')
    death_sound = pygame.mixer.Sound('audio/Jump7.wav')
except:
    print("Sound files not found. Audio is disabled.")
    hit_sound = None
    death_sound = None

# Colors
WHITE, BLUE, RED, BLACK, GRAY = (255, 255, 255), (0, 200, 255), (255, 80, 80), (10, 10, 20), (100, 100, 100)

# Game Variables
game_state = "MENU" 
score = 0
lives = 3
level = 1

# Objects
paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 120, 15)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 12, 12)
ball_speed = [5, -5]
bricks = []

def reset_game(full_reset=True):
    global score, lives, ball_speed, bricks, level
    
    # If full_reset is True, we go back to level 1 and score 0 (Main Menu start)
    if full_reset:
        score = 0
        level = 1
    
    # Always reset lives to 3 for the attempt
    lives = 3
    
    # Increase ball speed based on current level
    current_speed = 4 + level 
    ball_speed = [current_speed, -current_speed]
    
    ball.center = (WIDTH // 2, HEIGHT // 2 + 100)
    
    bricks.clear()
    rows = min(3 + level, 8) 
    for row in range(rows):
        for col in range(10):
            bricks.append(pygame.Rect(col * 80 + 2, row * 35 + 60, 75, 30))

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Initial brick setup
reset_game()

while True:
    screen.fill(BLACK)
    mx, my = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

    # --- STATE: MENU ---
    if game_state == "MENU":
        draw_text("Brick game", large_font, BLUE, 220, 150)
        
        play_btn = pygame.Rect(300, 280, 200, 50)
        inst_btn = pygame.Rect(300, 350, 200, 50)
        quit_btn = pygame.Rect(300, 420, 200, 50)

        pygame.draw.rect(screen, GRAY, play_btn)
        pygame.draw.rect(screen, GRAY, inst_btn)
        pygame.draw.rect(screen, GRAY, quit_btn)

        draw_text("PLAY", font, WHITE, 365, 288)
        draw_text("RULES", font, WHITE, 360, 358)
        draw_text("QUIT", font, WHITE, 370, 428)

        if click:
            if play_btn.collidepoint((mx, my)): 
                reset_game(full_reset=True) # Hard reset for new game
                game_state = "PLAYING"
            if inst_btn.collidepoint((mx, my)): game_state = "INSTRUCTIONS"
            if quit_btn.collidepoint((mx, my)): pygame.quit(); sys.exit()

    # --- STATE: INSTRUCTIONS ---
    elif game_state == "INSTRUCTIONS":
        draw_text("How to Play:", font, BLUE, 320, 150)
        draw_text("- Move paddle with mouse", font, WHITE, 250, 220)
        draw_text("- Don't let the ball fall", font, WHITE, 250, 270)
        draw_text("- Break all bricks to level up", font, WHITE, 250, 320)
        draw_text("Click anywhere to go back", font, GRAY, 240, 450)
        if click: game_state = "MENU"

    # --- STATE: PLAYING ---
    elif game_state == "PLAYING":
        paddle.centerx = mx
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.left <= 0 or ball.right >= WIDTH: ball_speed[0] *= -1
        if ball.top <= 50: ball_speed[1] *= -1 
        if ball.colliderect(paddle): ball_speed[1] *= -1
        
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speed[1] *= -1
                score += (10 * level)
                if hit_sound: hit_sound.play()
        
        if ball.bottom >= HEIGHT:
            if death_sound: death_sound.play()
            lives -= 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            if lives <= 0: game_state = "GAME_OVER"

        if not bricks:
            level += 1
            reset_game(full_reset=False) # Soft reset: Proceed to next level

        # HUD
        pygame.draw.line(screen, WHITE, (0, 50), (WIDTH, 50), 2)
        draw_text(f"Score: {score}", font, WHITE, 20, 10)
        draw_text(f"Level: {level}", font, BLUE, 250, 10)
        draw_text(f"Lives: {lives}", font, RED, 480, 10)
        draw_text(f"Bricks: {len(bricks)}", font, WHITE, 650, 10)

        for brick in bricks: pygame.draw.rect(screen, RED, brick)
        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

    # --- STATE: GAME OVER ---
    elif game_state == "GAME_OVER":
        draw_text("LIVES EXHAUSTED", large_font, RED, 180, 150)
        draw_text(f"Level Reached: {level} | Score: {score}", font, WHITE, 240, 250)
        
        retry_btn = pygame.Rect(300, 320, 200, 50)
        menu_btn = pygame.Rect(300, 390, 200, 50)
        
        pygame.draw.rect(screen, GRAY, retry_btn)
        pygame.draw.rect(screen, GRAY, menu_btn)
        
        draw_text("RETRY LEVEL", font, WHITE, 330, 330)
        draw_text("MAIN MENU", font, WHITE, 335, 400)
        
        if click:
            if retry_btn.collidepoint((mx, my)):
                # Reset game but KEEP level (Soft reset)
                reset_game(full_reset=False) 
                game_state = "PLAYING"
            if menu_btn.collidepoint((mx, my)):
                game_state = "MENU"

    pygame.display.flip()
    clock.tick(60)