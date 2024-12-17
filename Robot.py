import pygame
import random

# Pygame initialization
pygame.init()

# Constants
GRID_SIZE = 60  # Size of each grid square
GRID_COLUMNS = 3  # Number of columns in the grid
GRID_ROWS = 2  # Number of rows in the grid
SCREEN_WIDTH = 300  # Window width
SCREEN_HEIGHT = 300  # Window height
RED_SQUARE_SIZE = 20  # Size of the red squares (acid level squares)
ROBOT_SIZE = GRID_SIZE - 20  # Size of the robot
ROBOT_COLOR = (0, 200, 0)  # Green color for the robot
RED_COLOR = (255, 0, 0)  # Red color for high acid squares

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Acid Level Detection Robot")

# Offsets to center the grid
GRID_OFFSET_X = (SCREEN_WIDTH - (GRID_SIZE * GRID_COLUMNS)) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - (GRID_SIZE * GRID_ROWS + 50)) // 2

# Robot path movement (Squares: Initial -> 2 -> 1 -> 0 -> 3 -> 4 -> 5 -> out)
path = [(3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (1, 1), (2, 1), (3, 1)]
current_step = 0

# Generate random acid level squares (randomly place 2 acid squares in the grid)
acid_squares = set(random.sample(
    [(x, y) for x in range(GRID_COLUMNS) for y in range(GRID_ROWS)], 2))

# Track detected acid squares
detected_acid_squares = []

# Robot and Grid Positioning
robot_x, robot_y = path[0][0] * GRID_SIZE, path[0][1] * GRID_SIZE
acid_count = 0
status = "Stop"  # Initial status before robot enters grid

# Font for displaying text
font = pygame.font.Font(None, 18)

# Function to draw the grid


def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLUMNS):
            x = GRID_OFFSET_X + col * GRID_SIZE
            y = GRID_OFFSET_Y + row * GRID_SIZE
            pygame.draw.rect(screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 2)
            # Draw high acid squares (only display acid squares on the grid, not based on robot knowledge)
            if (col, row) in acid_squares:
                pygame.draw.rect(
                    screen,
                    RED_COLOR,
                    (x + (GRID_SIZE - RED_SQUARE_SIZE) // 2, y + (GRID_SIZE -
                     RED_SQUARE_SIZE) // 2, RED_SQUARE_SIZE, RED_SQUARE_SIZE),
                )

# Function to draw the robot


def draw_robot():
    x = GRID_OFFSET_X + robot_x
    y = GRID_OFFSET_Y + robot_y
    pygame.draw.rect(screen, ROBOT_COLOR,
                     (x + 10, y + 10, ROBOT_SIZE, ROBOT_SIZE))

# Function to update the robot's status


def update_status():
    status_text = font.render(f"Status: {status}", True, BLUE)
    count_text = font.render(f"High Acid Squares: {acid_count}", True, BLUE)
    position_text = font.render(
        f"Current Position: Square {current_step+1}", True, BLUE)
    detected_text = font.render(
        f"Detected Squares: {detected_acid_squares}", True, BLUE)
    screen.blit(status_text, (10, SCREEN_HEIGHT - 100))
    screen.blit(count_text, (10, SCREEN_HEIGHT - 80))
    screen.blit(position_text, (10, SCREEN_HEIGHT - 60))
    screen.blit(detected_text, (10, SCREEN_HEIGHT - 20))

# Function to generate final report


def generate_report():
    print("\nFinal Report:")
    print("Detected High Acid Squares:", detected_acid_squares)
    print("Total High Acid Squares Detected:", acid_count)
    print("Robot Navigation Path:", path)


def main():
    global robot_x, robot_y, status, acid_count, current_step, acid_status
    clock = pygame.time.Clock()
    running = True

    # Timer to track detection duration
    detection_start_time = None

    while running:
        screen.fill(BLACK)  # Clear the screen before drawing
        draw_grid()  # Draw grid and acid squares
        draw_robot()  # Draw robot on the grid
        update_status()  # Update and display the current status

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the current position of the robot
        current_pos = path[current_step]

        if current_pos == (3, 0):  # Initial position
            status = "Stop"
            # Prepare to move to the next position
            if current_step < len(path) - 1:
                current_step += 1
                robot_x = path[current_step][0] * GRID_SIZE
                robot_y = path[current_step][1] * GRID_SIZE
                status = "Moving"

        elif current_pos == (3, 1):  # Final position
            status = "Stopped at exit"
            running = False  # End of movement

        else:
            # Handle detection logic
            if detection_start_time is None:  # Start detecting when reaching a new square
                detection_start_time = pygame.time.get_ticks()
                status = "Detecting"

            if pygame.time.get_ticks() - detection_start_time < 1500:  # Stay in Detecting for 1.5 seconds
                pass  # Robot is still detecting
            else:  # Detection complete
                detection_start_time = None  # Reset detection timer

                if current_pos in acid_squares:  # Check if current square is a high acid square
                    status = "High Acid level detected"
                    acid_count += 1
                    detected_acid_squares.append(current_pos)

                # Prepare to move to the next square
                if current_step < len(path) - 1:
                    current_step += 1
                    robot_x = path[current_step][0] * GRID_SIZE
                    robot_y = path[current_step][1] * GRID_SIZE
                    status = "Moving"

        pygame.display.flip()
        clock.tick(1)
    generate_report()  # Generate and print final report
    pygame.quit()  # Quit pygame


if __name__ == "__main__":
    main()
