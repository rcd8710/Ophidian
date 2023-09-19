import math
import pygame
import random
import heapq

pygame.init()

# Initial Screen
width = 400
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

# Snake Attributes
snakex = 2
snakey = 2
snakedx = 5
snakedy = 0  # Start moving horizontally
snake_size = 10
snake_speed = 5
ai_snake_speed = 20
snake_body = [(snakex, snakey)]
snake_length = 1
ai_snake_length = snake_length

# Food
foodx = random.randrange(0, width - snake_size, snake_size)
foody = random.randrange(0, height - snake_size, snake_size)
score = 0
run = True
run_ai = False
run_ai2 = False
game_state = "start"
path = []

# Load player-controlled snake head and body images
player_snake_head_image = pygame.image.load("snake.png")
player_snake_body_image = pygame.image.load("snake scales_origin.png")

# Load AI-controlled snake head and body images
ai_snake_head_image = pygame.image.load("pngwing.com(3).png")
ai_snake_body_image = pygame.image.load("red scales.jpg")

ai2_snake_head_image = pygame.image.load("basilisk.png")
ai2_snake_body_image = pygame.image.load("white scales.jpg")

# Snake scaling
head_scale = 4
snake_scale = 1
ai_head_scale = 2.2
ai2_head_scale = 3

def reset_game():
    global snakex, snakey, snakedx, snakedy, snake_body, snake_length, foodx, foody, score
    snakex = 2
    snakey = 2
    snakedx = 5
    snakedy = 0  # Reset to start moving horizontally
    snake_body = [(snakex, snakey)]
    snake_length = 1
    foodx = random.randrange(0, width - snake_size, snake_size)
    foody = random.randrange(0, height - snake_size, snake_size)
    score = 0

def draw_text(text, size, x, y):
    font_path = "slkscr.ttf"
    font = pygame.font.Font(font_path, size)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))

def draw_text_centered(text, size, y):
    font_path = "slkscr.ttf"
    font = pygame.font.Font(font_path, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = width // 2  # Center horizontally
    text_rect.y = y
    screen.blit(text_surface, text_rect)

def find_path(start, goal, obstacles):
    # Define heuristic function (Manhattan distance)
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # A* algorithm
    open_list = [(0, start)]
    heapq.heapify(open_list)
    came_from = {start: None}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return list(reversed(path[:-1]))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            if next_pos in obstacles or next_pos[0] < 0 or next_pos[0] >= width or next_pos[1] < 0 or next_pos[1] >= height:
                continue
            new_g_score = g_score[current] + 1
            if next_pos not in g_score or new_g_score < g_score[next_pos]:
                g_score[next_pos] = new_g_score
                f_score = new_g_score + heuristic(next_pos, goal)
                heapq.heappush(open_list, (f_score, next_pos))
                came_from[next_pos] = current

    return []

# Modify the game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "start":
                game_state = "play"
            elif game_state == "game_over":
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "play"  # Set the game state to "play" when restarting
            elif game_state == "play":
                if event.key == pygame.K_q and not run_ai:  # Activate AI mode
                    run_ai = True
                    path = []  # Reset AI path when enabling AI mode
                elif event.key == pygame.K_UP and snakedy == 0:  # Prevent moving opposite direction
                    snakedx = 0
                    snakedy = -snake_speed
                elif event.key == pygame.K_LEFT and snakedx == 0:  # Prevent moving opposite direction
                    snakedx = -snake_speed
                    snakedy = 0
                elif event.key == pygame.K_DOWN and snakedy == 0:  # Prevent moving opposite direction
                    snakedx = 0
                    snakedy = snake_speed
                elif event.key == pygame.K_RIGHT and snakedx == 0:  # Prevent moving opposite direction
                    snakedx = snake_speed
                    snakedy = 0
                elif event.key == pygame.K_r:
                    run_ai2= True
                    run_ai=False
                    draw_text_centered("BASILISK", 30, 10)
                    path = []

    if run_ai:
        if not path:
            path = find_path((snakex, snakey), (foodx, foody), snake_body)
            if path:
                new_goal = path[-1]
                foodx, foody = new_goal

        # Determine how many grid units the AI snake should move in this loop iteration
        ai_move_units = ai_snake_speed // snake_speed

        # Inside the AI mode section of the game loop
        for _ in range(ai_move_units):
            if path:
                next_pos = path.pop(0)

                # Check if the snake ate food
                if snakex == foodx and snakey == foody:
                    # Increase the AI snake's length by one
                    ai_snake_length += 1

                    # Generate new food coordinates
                    foodx = random.randrange(0, width - snake_size, snake_size)
                    foody = random.randrange(0, height - snake_size, snake_size)

                # Add the new head position to the snake's body
                snake_body.append((snakex, snakey))

                # Remove the tail if the snake's length exceeds its current body length
                if len(snake_body) > ai_snake_length:
                    snake_body.pop(0)

                snakex, snakey = next_pos

    if run_ai2:
        if not path:
            path = find_path((snakex, snakey), (foodx, foody), snake_body)
            if path:
                new_goal = path[-1]
                foodx, foody = new_goal

        # Determine how many grid units the AI snake should move in this loop iteration
        ai_move_units = ai_snake_speed*3 // snake_speed

        # Inside the AI mode section of the game loop
        for _ in range(ai_move_units):
            if path:
                next_pos = path.pop(0)

                # Check if the snake ate food
                if snakex == foodx and snakey == foody:
                    # Increase the AI snake's length by one
                    ai_snake_length += 1

                    # Generate new food coordinates
                    foodx = random.randrange(0, width - snake_size, snake_size)
                    foody = random.randrange(0, height - snake_size, snake_size)

                # Add the new head position to the snake's body
                snake_body.append((snakex, snakey))

                # Remove the tail if the snake's length exceeds its current body length
                if len(snake_body) > ai_snake_length:
                    snake_body.pop(0)

                snakex, snakey = next_pos

    screen.fill((0, 0, 0))

    # Draw the body segments first, using the appropriate image set based on game state
    for i, segment in enumerate(reversed(snake_body)):
        if i != 0:
            if run_ai:
                scaled_body = pygame.transform.scale(ai_snake_body_image,
                                                     (int(snake_size * snake_scale), int(snake_size * snake_scale)))
            elif run_ai2:
                scaled_body = pygame.transform.scale(ai2_snake_body_image,
                                                     (int(snake_size * snake_scale), int(snake_size * snake_scale)))
            else:
                scaled_body = pygame.transform.scale(player_snake_body_image,
                                                     (int(snake_size * snake_scale), int(snake_size * snake_scale)))
            screen.blit(scaled_body, segment)

    head_x, head_y = snake_body[0]
    angle = math.atan2(foody - head_y, foodx - head_x)
    angle_degrees = math.degrees(angle)

    # Rotate the head image based on the angle, using the appropriate image set
    if run_ai:
        scaled_head = pygame.transform.scale(ai_snake_head_image,
                                             (int(snake_size * ai_head_scale), int(snake_size * ai_head_scale)))
    elif run_ai2:
        scaled_head = pygame.transform.scale(ai2_snake_head_image,
                                             (int(snake_size * ai2_head_scale), int(snake_size * ai2_head_scale)))
    else:
        scaled_head = pygame.transform.scale(player_snake_head_image,
                                             (int(snake_size * head_scale), int(snake_size * head_scale)))
    scaled_head_rotated = pygame.transform.rotate(scaled_head, -angle_degrees)

    # Draw the rotated head image
    screen.blit(scaled_head_rotated,
                (head_x - scaled_head_rotated.get_width() / 2, head_y - scaled_head_rotated.get_height() / 2))

    # Draw the food and score
    pygame.draw.circle(screen, (255, 0, 0), (foodx + snake_size // 2, foody + snake_size // 2), snake_size // 2)
    draw_text(f"Score: {score}", 15, 8, 8)

    if run_ai:
        draw_text_centered("VIPER", 30, 10)
    if run_ai2:
        draw_text_centered("BASILISK", 30, 10)
    if game_state == "start":
        draw_text("Press any key to start", 23, width // 2 - 165, height // 3)
    elif game_state == "play":
        snakex += snakedx
        snakey += snakedy

        if snakex > width or snakex < 0 or snakey > height or snakey < 0:
            game_state = "game_over"

        if snakex < foodx + snake_size and snakex + snake_size > foodx and snakey < foody + snake_size and snakey + snake_size > foody:
            score += 1

            foodx = random.randrange(0, width - snake_size, snake_size)
            foody = random.randrange(0, height - snake_size, snake_size)
            snake_length += 1  # Grow the snake by adding new segments to the body

        # Move the snake's body segments
        snake_body.append((snakex, snakey))

        if len(snake_body) > snake_length:
            snake_body.pop(0)

    elif game_state == "game_over":
        draw_text("Game Over", 40, width // 2 - 80, height // 2 - 20)
        draw_text("Press SPACE to restart", 20, width // 2 - 120, height // 2 + 20)

    # Update the display
    pygame.display.update()

    # Limit frame rate
    pygame.time.Clock().tick(30)

pygame.quit()
