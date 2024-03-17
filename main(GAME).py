import pygame
import random
import math

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Meteor Destroyer")

spaceship_pos = [400, 500]
spaceship_vel = [0, 0]
spaceship_acc = [0, 0]
spaceship_radius = 10
asteroids = []
lasers = []
score = 0
lives = 3
score_threshold = 100

def add_vectors(vector1, vector2):
    return [vector1[0] + vector2[0], vector1[1] + vector2[1]]

def generate_asteroid():
    asteroid_size = random.randint(20, 50)
    asteroid_pos = [random.randint(0, screen_width), 0 - asteroid_size]
    asteroid_vel = [0, random.uniform(1, 3)]
    return {"pos": asteroid_pos, "vel": asteroid_vel, "size": asteroid_size}

def draw_asteroids():
    for asteroid in asteroids:
        pygame.draw.circle(screen, red, (int(asteroid["pos"][0]), int(asteroid["pos"][1])), asteroid["size"])

def draw_lasers():
    for laser in lasers:
        pygame.draw.line(screen, green, laser, (laser[0], laser[1] - 10), 3)

def move_lasers():
    for laser in lasers:
        laser[1] -= 5
    for laser in lasers[:]:
        if laser[1] <= 0:
            lasers.remove(laser)

def check_collision():
    global asteroids, lasers, score, lives
    for asteroid in asteroids[:]:
        distance = math.sqrt((asteroid["pos"][0] - spaceship_pos[0])**2 + (asteroid["pos"][1] - spaceship_pos[1])**2)
        if distance < asteroid["size"] + spaceship_radius:
            asteroids.remove(asteroid)
            lives -= 1
            if lives <= 0:
                game_over()

    for laser in lasers[:]:
        for asteroid in asteroids[:]:
            distance = math.sqrt((asteroid["pos"][0] - laser[0])**2 + (asteroid["pos"][1] - laser[1])**2)
            if distance < asteroid["size"]:
                asteroids.remove(asteroid)
                lasers.remove(laser)
                score += 10

def display_info():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, white)
    lives_text = font.render(f"Lives: {lives}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

def game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
def move_spaceship(score):
    if score >= score_threshold:
        return 0.15  
    else:
        return 0.1   

def game_loop():
    global spaceship_pos, spaceship_vel, spaceship_acc, asteroids, score, lives, lasers
    running = True
    asteroid_spawn_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lasers.append([spaceship_pos[0], spaceship_pos[1]])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship_acc[0] = -0.1
        elif keys[pygame.K_RIGHT]:
            spaceship_acc[0] = 0.1
        else:
            spaceship_acc[0] = 0

        spaceship_vel = add_vectors(spaceship_vel, spaceship_acc)
        spaceship_pos = add_vectors(spaceship_pos, spaceship_vel)

        if spaceship_pos[0] < 0:
            spaceship_pos[0] = screen_width
        elif spaceship_pos[0] > screen_width:
            spaceship_pos[0] = 0

        asteroid_spawn_timer += 1
        if asteroid_spawn_timer == 60:
            asteroids.append(generate_asteroid())
            asteroid_spawn_timer = 0

        for asteroid in asteroids:
            asteroid["pos"] = add_vectors(asteroid["pos"], asteroid["vel"])

        move_lasers()
        check_collision()

        spaceship_acc[0] = move_spaceship(spaceship_acc[0] == move_spaceship(score))  # Enhanced spaceship movement based on the score

        screen.fill(black)
        draw_asteroids()
        draw_lasers()
        pygame.draw.circle(screen, white, (int(spaceship_pos[0]), int(spaceship_pos[1])), spaceship_radius)
        display_info()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    game_loop()
    pygame.quit() 
