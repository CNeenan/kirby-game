import pygame, time, random, math
pygame.init()

size = width, height = 1280, 864
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Kirby Chase')
background = pygame.image.load("background.gif")
font = pygame.font.SysFont('comicsansms', 32) 
white = (255, 255, 255)

# class for the player
class Player():
    def __init__(self):
        self.start_x = width/2
        self.start_y = height/2
        self.dx = 10
        self.dy = 10
        self.icon = pygame.image.load("kirby.gif")
        self.rect = self.icon.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
    
    # movement functions
    def goLeft(self):
        if self.rect.x > 0:
            self.rect.x -= self.dx
        else:
            self.rect.x = width

    def goRight(self):
        if self.rect.x < width:
            self.rect.x += self.dx
        else:
            self.rect.x = 0

    def goUp(self):
        if self.rect.y > 0:
            self.rect.y -= self.dy
        else:
            self.rect.y = height
        
    def goDown(self):
        if self.rect.y < height:
            self.rect.y += self.dy
        else:
            self.rect.y = 0

# class for the enemy
class Enemy():
    def __init__(self):
        self.start_x = random.randint(0, width)
        self.start_y = random.randint(0, height)
        self.icon = pygame.image.load("metaknight.gif")
        self.rect = self.icon.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.speed = 2
    
    def move_towards_player(self, player):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.rect.x - player.rect.x, self.rect.y - player.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speed
        self.rect.x -= dx * self.speed
        self.rect.y -= dy * self.speed

# class for the star
class Star():
    def __init__(self):
        self.start_x = random.randint(0, width)
        self.start_y = random.randint(0, height)
        self.icon = pygame.image.load("star.gif")
        self.rect = self.icon.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y

def main():
    # initialise characters and clock
    player = Player()
    enemies = []
    enemies.append(Enemy())
    star = Star()
    star_counter = 0
    power_ups = ['speed', 'attack']
    speed = 0
    attack = False
    clock = pygame.time.Clock()

    # game loop
    while True:
        # handle player quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # player movement
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            player.goLeft()
        elif key[pygame.K_d]:
            player.goRight()
        elif key[pygame.K_w]:
            player.goUp()
        elif key[pygame.K_s]:
            player.goDown()
        
        # attack
        elif key[pygame.K_SPACE]:
            if attack:
               enemies.pop()
               attack = False 

        for i in range(len(enemies)):
            # if the enemy collides with the player end the game
            if enemies[i].rect.colliderect(player.rect):
                main()

            # move enemy towards player
            enemies[i].move_towards_player(player)
        
        # if player collects a star
        if player.rect.colliderect(star.rect):
            star = Star()
            star_counter += 1
            
            # every 5 stars create a new enemy
            if star_counter % 5 == 0:
                enemies.append(Enemy())
            
            # every 10 stars give player a power up
            if star_counter % 10 == 0:
                power_up = random.choice(power_ups)
                if power_up == 'speed':
                    if player.dx < 20:
                        player.dx += 2
                        player.dy += 2
                        speed += 1
                else:
                    attack = True

        # text
        star_counter_display = font.render('Stars: ' + str(star_counter), True, white)
        star_counter_display_rect = star_counter_display.get_rect()
        
        if speed == 5:
            speed_display = font.render('Speed: Max', True, white )
        else:
            speed_display = font.render('Speed: ' + str(speed), True, white )
        speed_display_rect = speed_display.get_rect()
        speed_display_rect.x = 1000
        
        if attack:
            attack_display = font.render('Attack: Ready!', True, white)
        else:
            attack_display = font.render('Attack: Not Ready', True, white)
        attack_display_rect = attack_display.get_rect()
        attack_display_rect.x = 1000
        attack_display_rect.y = 100

        
        # display images 
        screen.blit(background, (0, 0))
        screen.blit(star.icon, star.rect)
        screen.blit(player.icon, player.rect)
        
        for i in range(len(enemies)):
            screen.blit(enemies[i].icon, enemies[i].rect)
        
        screen.blit(star_counter_display, star_counter_display_rect)
        screen.blit(speed_display, speed_display_rect)
        screen.blit(attack_display, attack_display_rect)

        # update display at 60fps
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
