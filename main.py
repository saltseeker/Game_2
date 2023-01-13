import pygame, sys, random, pygame.font, os, pygame.mixer



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
       
      
    def shooting_bullet(self):
        color = self.laser_colors[self.laser_color_counter]
        self.laser_color_counter = (self.laser_color_counter + 1) % len(self.laser_colors)
        self.shoot_sound.play()
        return Bullet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],color)

   
    
    def gameover(self):
        font = pygame.font.Font(None, 80)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(text, text_rect)

        font_continue = pygame.font.Font(None, 50)
        text_continue = font_continue.render("Left mouse button to continue", True, (255, 255, 255))
        text_continue_rect = text_continue.get_rect(center=(screen_width/2, screen_height/2 + 40))
        screen.blit(text_continue, text_continue_rect)

        font_exit = pygame.font.Font(None, 50)
        text_exit = font_exit.render("To exit press right mouse button", True, (255, 255, 255))
        text_exit_rect = text_exit.get_rect(center=(screen_width/2, screen_height/2 + 80))
        screen.blit(text_exit, text_exit_rect)
        pygame.display.update() 
       

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        return
                    elif event.button == 3:  
                        pygame.quit()
                        sys.exit()


        

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y, color):
        super().__init__()
        self.color = color
        self.image = pygame.image.load(f"images/laser/{self.color}laser.png").convert_alpha()    
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.2), int(self.image.get_height()*0.2)))
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

    def update(self):
        self.rect.x += 22
        if self.rect.x >= screen_width - 199:                                       
            self.kill()
        
        
           
class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_files = ["1.png", "2.png", "3.png","4.png","5.png","6.png","7.png"]
        image_path = os.path.join("images/projectile", self.image_files[random.randint(0, len(self.image_files)-1)])
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(right = screen_width + random.randint(0, 400),centery=random.randint(0, screen_height))
        self.speed = random.randint(4, 10)
        self.explode_sound = pygame.mixer.Sound("sounds/explode.wav")
   
    
    
    
    def update(self):
        self.rect.x -= self.speed
        if pygame.sprite.collide_rect(self, player):
            player.kill()
            self.kill()
            self.explode_sound.play()
            player.gameover()
            pygame.display.update()
    
          





#Basic pygame setup
pygame.init()
pygame.display.set_caption('Meteor Shower Very_ALPHA Ver.0.00001')
clock = pygame.time.Clock()
screen_width, screen_height = 1100, 1200
screen = pygame.display.set_mode((screen_height,screen_width))
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 50)
game_active = True

# Creating a group of projectiles and adding a projectile to it.
projectiles = pygame.sprite.Group()
projectile = Projectile()
projectiles.add(projectile)

# Creating a player object and adding it to a group.
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullet_group = pygame.sprite.Group()

background = pygame.image.load("images/bg/space.png").convert()


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
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = player.shooting_bullet()
            bullet_group.add(bullet)
    if not player.alive():
        player_group.empty()
        player = Player()
        player_group.add(player)
        player.gameover()

    # check if it's time to spawn a new projectile
    projectile_group.update()
    if pygame.time.get_ticks() - spawn_time >= 100:
        projectile_group.add(Projectile())
        spawn_time = pygame.time.get_ticks()
    for projectile in pygame.sprite.groupcollide(projectile_group, bullet_group, True, True):
        pass

    
    # Drawing the background, bullets, projectiles, player, and updating the player and bullets.
    screen.blit(background, (0, 0))
    bullet_group.draw(screen)
    projectile_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    bullet_group.update()
    pygame.display.flip()
    clock.tick(120)