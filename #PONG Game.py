import pygame

# Initialize Pygame
pygame.init()

# Display/Screen Setup
screen_width = 700
screen_height = 500
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# Define Colours
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_black = (0, 0, 0)
color_blue = (0, 0, 255)

# Defining Constants
frame_rate = 60
paddle_width = 20
paddle_height = 100
ball_radius = 9
font_size = 50
winning_points = 10

#Creating Paddle Class
class Paddle:
    def __init__(self, x_pos, y_pos):
        self.rect = pygame.Rect(x_pos, y_pos, paddle_width, paddle_height)
        self.color = color_red
        self.speed = 4
    
    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)
    
    def move(self, direction):
        if direction == 'up' and self.rect.top > 0:
            self.rect.y -= self.speed
        elif direction == 'down' and self.rect.bottom < screen_height:
            self.rect.y += self.speed

    def reset(self, x_pos, y_pos):
        self.rect.x = x_pos
        self.rect.y = y_pos

#Creating Ball Class
class Ball:
    def __init__(self, x_pos, y_pos):
        self.circle = pygame.Rect(x_pos - ball_radius, y_pos - ball_radius, ball_radius * 2, ball_radius * 2)
        self.color = color_blue
        self.max_speed = 5
        self.x_speed = self.max_speed
        self.y_speed = 0
    
    def draw(self):
        pygame.draw.ellipse(window, self.color, self.circle)
    
    def move(self):
        self.circle.x += self.x_speed
        self.circle.y += self.y_speed
    
    def reset(self):
        self.circle.center = (screen_width // 2, screen_height // 2)
        self.y_speed = 0
        self.x_speed *= -1

#Display Scores on the screen
def draw_scores(left_points, right_points):
    font = pygame.font.SysFont("comicsans", font_size)
    left_text = font.render(f"{left_points}", True, color_white)
    right_text = font.render(f"{right_points}", True, color_white)
    window.blit(left_text, (screen_width // 4 - left_text.get_width() // 2, 20))
    window.blit(right_text, (screen_width * 3 // 4 - right_text.get_width() // 2, 20))

#Draw the game elements such as paddles, ball
def draw_game_elements(left_paddle, right_paddle, ball, left_points, right_points):
    window.fill(color_black)
    draw_scores(left_points, right_points)
    left_paddle.draw()
    right_paddle.draw()
    pygame.draw.aaline(window, color_white, (screen_width // 2, 0), (screen_width // 2, screen_height))
    ball.draw()
    pygame.display.update()

#Function to manage the collision between ball and paddle
def handle_collisions(ball, left_paddle, right_paddle):
    if ball.circle.top <= 0 or ball.circle.bottom >= screen_height:
        ball.y_speed *= -1
    
    if ball.x_speed < 0 and left_paddle.rect.colliderect(ball.circle):
        ball.x_speed *= -1
        adjust_ball_speed(ball, left_paddle)
    elif ball.x_speed > 0 and right_paddle.rect.colliderect(ball.circle):
        ball.x_speed *= -1
        adjust_ball_speed(ball, right_paddle)

#Function that adjusts the speed of the ball
def adjust_ball_speed(ball, paddle):
    paddle_center = paddle.rect.centery
    ball_center = ball.circle.centery
    offset = (paddle_center - ball_center) / (paddle.rect.height / 2)
    ball.y_speed = -offset * ball.max_speed

#Function to specify the movement of the paddles
def move_paddles(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move('up')
    if keys[pygame.K_s]:
        left_paddle.move('down')
    if keys[pygame.K_UP]:
        right_paddle.move('up')
    if keys[pygame.K_DOWN]:
        right_paddle.move('down')

#Define the main logic of the code
def main():
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, screen_height // 2 - paddle_height // 2)
    right_paddle = Paddle(screen_width - 10 - paddle_width, screen_height // 2 - paddle_height // 2)
    ball = Ball(screen_width // 2, screen_height // 2)
    
    left_points = 0
    right_points = 0
    
    running = True
    while running:
        clock.tick(frame_rate)
        draw_game_elements(left_paddle, right_paddle, ball, left_points, right_points)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        move_paddles(keys, left_paddle, right_paddle)
        
        ball.move()
        handle_collisions(ball, left_paddle, right_paddle)
        
        if ball.circle.left < 0:
            right_points += 1
            ball.reset()
        elif ball.circle.right > screen_width:
            left_points += 1
            ball.reset()
        
        if left_points >= winning_points or right_points >= winning_points:
            winner = "Left Player Wins!" if left_points >= winning_points else "Right Player Wins!"
            font = pygame.font.SysFont("comicsans", font_size)
            winner_text = font.render(winner, True, color_white)
            window.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, screen_height // 2 - winner_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            left_points = 0
            right_points = 0
            ball.reset()
            left_paddle.reset(10, screen_height // 2 - paddle_height // 2)
            right_paddle.reset(screen_width - 10 - paddle_width, screen_height // 2 - paddle_height // 2)

    pygame.quit()

if __name__ == "__main__":
    main()
