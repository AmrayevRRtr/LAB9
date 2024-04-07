import pygame


pygame.init()


W, H = 800, 600


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Paint")


drawing_color = BLACK
drawing_key = "pen"  
radius = 10  
drawing = False
eraser = False
screen.fill(WHITE)
pygame.display.update()

# Function to draw shapes
def draw(shape, color, start_pos, end_pos):
    if shape == "rect":
        pygame.draw.rect(screen, color, (start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])))
    elif shape == "circle":
        radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
        pygame.draw.circle(screen, color, start_pos, radius)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.KEYDOWN:
            # press 'q' if you want to draw rectangle
            if event.key == pygame.K_q:
                drawing_key = "rect"
            # press 'c' if you want to draw circle
            elif event.key == pygame.K_c:
                drawing_key = "circle"
            # press 'p' if you want to draw with pen
            elif event.key == pygame.K_p:
                drawing_key = "pen"
            # press 'e' if you want to erase something
            elif event.key == pygame.K_e:
                drawing_key = "eraser"
            # press 'b', 'r', 'g', 's' to make color black, red, green and blue, respectively 
            elif event.key == pygame.K_b:
                drawing_color = BLACK
            elif event.key == pygame.K_r:
                drawing_color = RED
            elif event.key == pygame.K_g:
                drawing_color = GREEN
            elif event.key == pygame.K_s:
                drawing_color = BLUE


    if drawing:
        end_pos = pygame.mouse.get_pos()
        if drawing_key == "pen":
            pygame.draw.circle(screen, drawing_color, end_pos, radius)
        elif drawing_key in ["rect", "circle"]:
            # screen.fill(WHITE)  # Clear screen to redraw shapes
            draw(drawing_key, drawing_color, start_pos, end_pos)
        elif drawing_key == "eraser":
            pygame.draw.circle(screen, WHITE, end_pos, radius)
        
        pygame.display.update()

