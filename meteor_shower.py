import pygame, sys, random, pygame.font, os, pygame.mixer


class StartMenu:
    def __init__(self):
        self.background = pygame.image.load("images/bg/space1.png").convert()
        self.enter_button = pygame.image.load("images/bg/enter.png").convert_alpha()
        self.button_rect = self.enter_button.get_rect(center=(screen_width/2, screen_height/2+50))
        self.font = pygame.font.Font("images/font/Pixeltype.ttf", 110)
        self.text = self.font.render("Meteor Shower", True, (255, 222, 222))
        self.text_rect = self.text.get_rect(center=(screen_width/2, screen_height/2-100))
        self.version_font = pygame.font.Font("images/font/Pixeltype.ttf", 40)
        self.version_text = self.version_font.render("Alpha Ver. 0.32312323", True, (255, 255, 255))
        self.version_text_rect = self.version_text.get_rect()
        self.version_text_rect.bottomright = (screen_width, screen_height)

    def display(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.text_rect)
        screen.blit(self.enter_button, self.button_rect)
        screen.blit(self.version_text, self.version_text_rect)
        pygame.display.update()


    def wait_for_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

class Score:
    def __init__(self):
        self.screen = screen
        self.start_time = start_time
        self.font = pygame.font.Font("images/font/Pixeltype.ttf", 50)

    def update(self):
        current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
        score_surface = self.font.render(f'Score: {current_time}', True,(255, 255, 255))
        score_rect = score_surface.get_rect(center = (1100,50))
        self.screen.blit(score_surface,score_rect)
        pygame.display.update()

    def reset(self):
        self.start_time = int(pygame.time.get_ticks() / 1000)

    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/ship/ship.png").convert_alpha() 
        self.rect = self.image.get_rect(center = (screen_width/2,screen_height/2))
        self.laser_colors = ["g", "r", "b"]
        self.laser_color_counter = 0
        pygame.mixer.init()
        self.shoot_sound = pygame.mixer.Sound("sounds/shoot.ogg")


    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        pygame.display.update()
       
    
    def shooting_bullet(self):
        # Creating a list of colors and then cycling through them.
        color = self.laser_colors[self.laser_color_counter]
        self.laser_color_counter = (self.laser_color_counter + 1) % len(self.laser_colors)
        self.shoot_sound.play()
        return Bullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],color)

    def gameover(self):
        font = pygame.font.Font("images/font/Pixeltype.ttf", 50)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(text, text_rect)

        font_continue = pygame.font.Font("images/font/Pixeltype.ttf", 50)
        text_continue = font_continue.render("SPACE to continue", True, (255, 255, 255))
        text_continue_rect = text_continue.get_rect(center=(screen_width/2, screen_height/2 + 40))
        screen.blit(text_continue, text_continue_rect)

        font_exit = pygame.font.Font("images/font/Pixeltype.ttf", 50)
        text_exit = font_exit.render(" X  To exit ", True, (255, 255, 255))
        text_exit_rect = text_exit.get_rect(center=(screen_width/2, screen_height/2 + 80))
        screen.blit(text_exit, text_exit_rect)

        pygame.display.update() 
        score.reset()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  
                        return
                    elif event.key == pygame.K_x:  
                        pygame.quit()
                        sys.exit()


        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y, color):
        super().__init__()
        self.color = color
        self.image = pygame.image.load(f"images/laser/{self.color}laser.png").convert_alpha()    
        # Scaling the image to 20% of its original size.
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.2), int(self.image.get_height()*0.2)))
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        
        
    def update(self):
        # Moving the bullet to the right.
        self.rect.x += 22
        #Destroys the bullet within x range
        if self.rect.x >= screen_width - 199:                                       
            self.kill()
        


class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_files = ["1.png", "2.png", "3.png","4.png","5.png","6.png","7.png"]
        image_path = os.path.join("images/projectile", self.image_files[random.randint(0, len(self.image_files)-1)])
        self.image = pygame.image.load(image_path).convert_alpha()
        self.explosion_image = pygame.image.load("images/ship/explode1.png").convert_alpha()
        # Setting the position of the projectile.
        self.rect = self.image.get_rect(right = screen_width + random.randint(0, 400),centery=random.randint(0, screen_height))
        # randomly set speed
        self.speed = random.randint(4, 10)
        self.explode_sound = pygame.mixer.Sound("sounds/ship.flac")
        self.is_exploded = False
    
    
    #If the player collides with the enemy, the player dies and  explodes
    def update(self):
        self.rect.x -= self.speed
        if pygame.sprite.collide_mask(self, player):
            player.kill()
            self.explode_sound.play()
            self.is_exploded = True
            pygame.display.update()
        if self.is_exploded:
            self.image = self.explosion_image
            
        
            
    
          
#Basic pygame setup

pygame.init()
pygame.display.set_caption('Meteor Shower')
clock = pygame.time.Clock()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mouse.set_visible(False)
game_active = True
start_time = 0
score = Score()
background = pygame.image.load("images/bg/space1.png").convert()



# Creating groups.
start_menu = StartMenu()
start_menu.display()
start_menu.wait_for_input()


projectiles = pygame.sprite.Group()
projectile = Projectile()
projectiles.add(projectile)


player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullet_group = pygame.sprite.Group()




# add a spawn time for projectiles
spawn_time = pygame.time.get_ticks()
projectile_group = pygame.sprite.Group()
for i in range(9):
    projectile_group.add(Projectile())

#Game loop
while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        score.update()   
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = player.shooting_bullet()
            bullet_group.add(bullet)
    if not player.alive():
        projectile_group.empty()
        player_group.empty()
        player_group.add(player)
        player.gameover()
    # check if it's time to spawn a new projectile
    if pygame.time.get_ticks() - spawn_time >= 100:
        projectile_group.add(Projectile())
        spawn_time = pygame.time.get_ticks()
    projectile_group.update()
    # Checking if the bullet and projectile collide. If they do, it will remove the projectile and
    # bullet.
    for projectile in pygame.sprite.groupcollide(projectile_group, bullet_group, True, True):
        pass

    
    
    # Drawing the background, bullets, projectiles, player, and updating the bullets, projectiles, and player
    screen.blit(background, (0, 0))
    screen.blit(start_menu.version_text, start_menu.version_text_rect)
    bullet_group.draw(screen)
    projectile_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    bullet_group.update()
    projectiles.update()
    pygame.display.flip()
    clock.tick(120)

