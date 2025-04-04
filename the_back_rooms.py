import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FOV = math.pi / 3  # Field of view (60 degrees)
HALF_FOV = FOV / 2
RAY_AMOUNT = SCREEN_WIDTH  # One ray per pixel for better quality
STEP_ANGLE = FOV / RAY_AMOUNT
MAX_DEPTH = 800
CELL_SIZE = 64
PLAYER_SPEED = 3
TURN_SPEED = 0.03

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("3D Hallway Navigation")
clock = pygame.time.Clock()

# Player settings (in map coordinates)
player_x = 1.5 * CELL_SIZE  # Start in the middle of the first hallway
player_y = 1.5 * CELL_SIZE
player_angle = 0

# Simple map (1 represents walls, 0 represents empty space)
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

def cast_ray(angle):
    # Ray casting variables
    ray_x = player_x
    ray_y = player_y
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    
    # Ray casting loop
    distance = 0
    hit_wall = False
    
    while not hit_wall and distance < MAX_DEPTH:
        distance += 1
        test_x = int((ray_x + distance * cos_a) / CELL_SIZE)
        test_y = int((ray_y + distance * sin_a) / CELL_SIZE)
        
        # Check if ray is out of bounds
        if test_x < 0 or test_x >= len(game_map[0]) or test_y < 0 or test_y >= len(game_map):
            distance = MAX_DEPTH
            break
            
        # Check if ray hit a wall
        if game_map[test_y][test_x] == 1:
            hit_wall = True
    
    # Calculate wall height
    if distance < MAX_DEPTH:
        # Fix fisheye effect
        distance = distance * math.cos(player_angle - angle)
        wall_height = min(int(CELL_SIZE * SCREEN_HEIGHT / distance), SCREEN_HEIGHT)
    else:
        wall_height = 0
        
    return wall_height, distance

def main():
    global player_x, player_y, player_angle
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Handle player movement
        keys = pygame.key.get_pressed()
        
        # Forward/backward movement
        if keys[pygame.K_w]:
            new_x = player_x + PLAYER_SPEED * math.cos(player_angle)
            new_y = player_y + PLAYER_SPEED * math.sin(player_angle)
            # Check collision before moving
            if game_map[int(new_y / CELL_SIZE)][int(new_x / CELL_SIZE)] == 0:
                player_x = new_x
                player_y = new_y
                
        if keys[pygame.K_s]:
            new_x = player_x - PLAYER_SPEED * math.cos(player_angle)
            new_y = player_y - PLAYER_SPEED * math.sin(player_angle)
            # Check collision before moving
            if game_map[int(new_y / CELL_SIZE)][int(new_x / CELL_SIZE)] == 0:
                player_x = new_x
                player_y = new_y
            
        # Rotation
        if keys[pygame.K_a]:
            player_angle -= TURN_SPEED
        if keys[pygame.K_d]:
            player_angle += TURN_SPEED
            
        # Clear screen
        screen.fill(BLACK)
        
        # Cast rays and draw walls
        for x in range(SCREEN_WIDTH):
            # Calculate ray angle
            ray_angle = player_angle - HALF_FOV + (x / SCREEN_WIDTH) * FOV
            wall_height, distance = cast_ray(ray_angle)
            
            # Calculate wall position
            wall_top = (SCREEN_HEIGHT - wall_height) // 2
            wall_bottom = wall_top + wall_height
            
            # Draw wall slice
            if distance < MAX_DEPTH:
                # Calculate shading based on distance
                shade = min(1.0, 1.0 - (distance / MAX_DEPTH))
                color = (int(255 * shade), int(255 * shade), int(255 * shade))
                # Draw the wall slice
                pygame.draw.line(screen, color, 
                               (x, wall_top), 
                               (x, wall_bottom))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main() 