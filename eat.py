import pygame
import random
import math
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

view_point = [0,0]

class Block(pygame.sprite.Sprite):
     
    def __init__(self, color, width, height):

        super().__init__()
        self.size = [width, height]
        self.image = pygame.Surface(self.size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = random.randrange(2,5) #cell speed
        self.move = [0, 0] 
        self.direction = None

        self.center_x = random.random()
        self.center_y = random.random()
 
      
         
    def update(self):
        directions = {"S":((-1,2),(1,self.speed)),"SW":((-self.speed,-1),(1,self.speed)),"W":((-self.speed,-1),(-1,2)),"NW":((-self.speed,-1),(-self.speed,-1)),"N":((-1,2),(-self.speed,-1)),"NE":((1,self.speed),(-self.speed,-1)),"E":((1,self.speed),(-1,2)),"SE":((1,self.speed),(1,self.speed))} #((min x, max x)(min y, max y))
        directionsName = ("S","SW","W","NW","N","NE","E","SE") #possible directions
        if random.randrange(0,5) == 2: #move about once every 5 frames
            if self.direction == None: #if no direction is set, set a random one
                self.direction = random.choice(directionsName)
            else:
                a = directionsName.index(self.direction) #get the index of direction in directions list
                b = random.randrange(a-1,a+2) #set the direction to be the same, or one next to the current direction
                if b > len(directionsName)-1: #if direction index is outside the list, move back to the start
                    b = 0
                self.direction = directionsName[b]
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative y to a random number between min y and max y

        """ Update the ball's position. """
        # Calculate a new x, y
        self.center_x = self.move[0] + self.center_x
        self.center_y = self.move[1] + self.center_y
        ##self.rect.x = self.radius * math.sin(self.angle * math.pi/2) + self.center_x + view_point[0]
        ##self.rect.y = self.radius * math.cos(self.angle * math.pi/2) + self.center_y + view_point[1]
        self.rect.x = self.center_x + view_point[0]
        self.rect.y = self.center_y + view_point[1]
        
        # Increase the angle in prep for the next round.
        #self.angle += self.speed
 
 
class Player(pygame.sprite.Sprite):
    """ Class to represent the player. """
    def __init__(self, color, width, height):
        """ Create the player image. """
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        

    def grow(self, point):
        self.width = self.width + point
        self.height = self.height + point
 
    def update(self):
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 200
        
        
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Loop until the user clicks the close button.
done = False
game = False
display_main = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
while done == False:
    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'Group.'
    block_list = pygame.sprite.Group()
 
    # This is a list of every sprite. All blocks and the player block as well.
    all_sprites_list = pygame.sprite.Group()
 
    for i in range(10):
        # This represents a block
        block = Block(BLACK, random.randrange(5,50), random.randrange(5,55))
 
        # Set a random center location for the block to orbit
        block.center_x = random.randrange(SCREEN_WIDTH)
        block.center_y = random.randrange(SCREEN_HEIGHT)
        # Add the block to the list of objects
        block_list.add(block)
        all_sprites_list.add(block)
     
    # Create a RED player block
    player = Player(RED, 20, 15)
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    all_sprites_list.add(player)
    #Menu loop-------------------------------
    while not done and display_main:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                display_main = False
                game = True

        screen.fill(BLACK)

        clock.tick(60)
        pygame.display.flip()
 
    score = 0
    grow = 0
    del_pos = [0,0]
    count = 0
    sec = 0
    min = 2
    # -------- Main Program Loop -----------
    while not done and game:
        count = count + 1
        if count == 60:
            count = 0
            print (min, sec)
            if min == 0 and sec == 0:
                    print('end')
                    game = False
                    display_main = True
            if sec == 0:
                sec = 59
                min = min - 1
                print (min,sec)
            sec = sec - 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pos = pygame.mouse.get_pos()
        del_pos[0] = (0.01*((SCREEN_WIDTH/2)-pos[0]))
        del_pos[1] = (0.01*((SCREEN_HEIGHT/2)-pos[1]))

        view_point[0] = view_point[0]+del_pos[0]
        view_point[1] = view_point[1]+del_pos[1]
 
        all_sprites_list.update()
 
        # Clear the screen
        screen.fill(WHITE)
 
        # See if the player block has collided with anything.
        blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)
        for block in blocks_hit_list:
            if block.size[0] * block.size[1] < player.width * player.height:
               block_list.remove(block)
               all_sprites_list.remove(block)
            else:
                blocks_hit_list = []
                print(block.size[0] in blocks_hit_list)
 
        # Check the list of collisions.
        for block in blocks_hit_list:
            score += 1
            grow = grow + 1
            if grow == 10:
                player.grow(5)
                grow = 0
            print( score )

 
        # Draw all the spites
        all_sprites_list.draw(screen)

        text = font.render("Time: "+ str(min) +" "+ str(sec), True, RED)
        screen.blit(text, [10, 10])

        text = font.render("Score: "+ str(score),True,RED)
        screen.blit(text, [10,40])
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
        # Limit to 60 frames per second
        clock.tick(60)
 
pygame.quit()
