import pygame, sys, random, pygame.font, os, pygame.mixer



def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = font.render(f'Score: {current_time}', True,(255, 255, 255))
    score_rect = score_surface.get_rect(center = (1100,50))
    screen.blit(score_surface,score_rect)
    pygame.display.update()



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
        text_continue = font_continue.render("SPACE to continue", True, (255, 255, 255))
        text_continue_rect = text_continue.get_rect(center=(screen_width/2, screen_height/2 + 40))
        screen.blit(text_continue, text_continue_rect)

        font_exit = pygame.font.Font(None, 50)
        text_exit = font_exit.render(" X  To exit ", True, (255, 255, 255))
        text_exit_rect = text_exit.get_rect(center=(screen_width/2, screen_height/2 + 80))
        screen.blit(text_exit, text_exit_rect)

        pygame.display.update() 

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
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()*0.2), int(self.image.get_height()*0.2)))
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        self.explode_sound = pygame.mixer.Sound("sounds/ship.flac")
        


    def update(self):
        self.rect.x += 22
        #Destroys the bullet within x range
        if self.rect.x >= screen_width - 199:                                       
            self.kill()
        projectile_hit_list = pygame.sprite.spritecollide(self, projectiles, True)
        if len(projectile_hit_list) > 0:
            self.explode_sound.play()
        

class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_files = ["1.png", "2.png", "3.png","4.png","5.png","6.png","7.png"]
        image_path = os.path.join("images/projectile", self.image_files[random.randint(0, len(self.image_files)-1)])
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(right = screen_width + random.randint(0, 400),centery=random.randint(0, screen_height))
        # randomly set speed
        self.speed = random.randint(4, 10)
        self.explode_sound = pygame.mixer.Sound("sounds/ship.flac")
        
    
    
    def update(self):
        self.rect.x -= self.speed
        if pygame.sprite.collide_rect(self, player):
            player.kill()
            self.explode_sound.play()
            self.kill()
            player.gameover()
            pygame.display.update()
       
    
          
#Basic pygame setup

pygame.init()
pygame.display.set_caption('Meteor Shower')
clock = pygame.time.Clock()
screen_width, screen_height = 1100, 1200
screen = pygame.display.set_mode((screen_height,screen_width))
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 50)
game_active = True
start_time = 0


projectiles = pygame.sprite.Group()
projectile = Projectile()
projectiles.add(projectile)

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
        start_time = int(pygame.time.get_ticks() / 1000)
   

    # check if it's time to spawn a new projectile
    if pygame.time.get_ticks() - spawn_time >= 100:
        projectile_group.add(Projectile())
        spawn_time = pygame.time.get_ticks()
    projectile_group.update()
    # Checking if the bullet and projectile collide. If they do, it will remove the projectile and
    # bullet.
    for projectile in pygame.sprite.groupcollide(projectile_group, bullet_group, True, True):
        pass

    
    display_score()
    screen.blit(background, (0, 0))
    bullet_group.draw(screen)
    projectile_group.draw(screen)
    player_group.draw(screen)
    player_group.update()
    bullet_group.update()
    projectiles.update()
    pygame.display.flip()
    clock.tick(120)



 


