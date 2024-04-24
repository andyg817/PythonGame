import random
import pygame
from pygame.locals import *
import time
import threading

black = (0, 0, 0)
white = (255, 255, 255)
grey = (120, 120, 120)
green = (0, 255, 0)
bright_green = (0, 200, 0)

# Constants from main.py - Andrew
W, H = 800, 600
pSize = 50
pSpeed = 5
pHealth = 100
pAttack = 10
pDefense = 5
pHColor = (0, 255, 0)  # Green
mSize = 50
mSpeed = 5
mHealth = 50
mHColor = (255, 0, 0)  # Red
pACooldown = 2000
mACooldown = 1000
pATimer = 0
mATimer = 0
dHelath = 200
coinVal = random.randint(1,10)
coins = 0

# Load all images - main.py - Andrew
mList = ["ghost.png", "skeleton.png", "slime.png", "goblin.png", "zombie.png", "spider.png"]
mImg = pygame.image.load(random.choice(mList))
mImg = pygame.transform.scale(mImg, (mSize, mSize))
pImg = pygame.image.load("player.png")
pImg = pygame.transform.scale(pImg, (pSize, pSize))
prImg = pygame.image.load("princess.png")
prImg = pygame.transform.scale(prImg, (pSize, pSize))
bImg = pygame.image.load("floor.png")
bImg = pygame.transform.scale(bImg, (W, H))
drImg = pygame.image.load("droom.png")
drImg = pygame.transform.scale(drImg, (W, H))
wImg = pygame.image.load("wall.png")
wImg = pygame.transform.scale(wImg, (W, H))
cImg = pygame.image.load("coins.png")
cImg = pygame.transform.scale(cImg, (50, 50))
powerImg = pygame.image.load("powerup.png")
powerImg = pygame.transform.scale(powerImg, (50, 50))

#Thread for file update
def file_writer():
    while True:
        with open('communication.txt', 'r') as file:
            data = file.read()

        if data == "locked":
            continue

        else:
            with open('communication.txt', 'w') as update_file:
                update_file.write(Player.direction)
            Player.direction = ""
            break

# Create a function for rendering text objects
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Create a function for buttons
def button(msg, x, y, w, h, ic, ac, gameDisplay):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font(None, 20)
    textSurf, textRect = text_objects(msg, smallText, (0, 0, 0))
    textRect.center = (x + w // 2, y + h // 2)
    gameDisplay.blit(textSurf, textRect)

def message_button(msg, x, y, w, h, ic, ac, gameDisplay):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font(None, 20)
    textSurf, textRect = text_objects(msg, smallText, (0, 0, 0))
    textRect.center = (x + w // 2, y + h // 2)
    gameDisplay.blit(textSurf, textRect)

    return False  # Return False if the button is not clicked

# Create a function for the "Paused" state
def paused(gameDisplay):
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(grey)
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Paused", largeText, (0, 0, 0))
        TextRect.center = (W // 2, H // 2)
        gameDisplay.blit(TextSurf, TextRect)

        continue_button = button("Continue", 150, 450, 100, 50, white, black, gameDisplay)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_p:
                    continue_button = True

        if continue_button:
            pause = False  # Set pause to False to continue the game

        pygame.display.update()
        #clock.tick(15)

def timedEvent(gameDisplay):
    random_num = random.randint(1, 4)
    option1 = ""
    option2 = ""
    message = ""
    event_number = 0

    #Event1
    if(random_num == 1):
        message = "A sound echoes through the dungeon. Do you want to investigate?"
        option1 = "Yes, let's go."
        option2 = "Wait, a minute."
        event_number = 10

    #Event2
    if(random_num == 2):
        message = "You found a hole in the ground. Do you want to enter it?"
        option1 = "Jump In"
        option2 = "No, you mad??"
        event_number = 20


    #Event3
    if(random_num == 3):
        message = "You found a strange vial wiht a liquid in it."
        option1 = "Drink it"
        option2 = "Throw it away"
        event_number = 30

    #Event4
    if(random_num == 4):
        message = "You come across a strange statue. It seems like it's looking at you"
        option1 = "Destroy It"
        option2 = "Pick it up"
        event_number = 40

    smallText = pygame.font.Font(None, 30)
    textSurf, textRect = text_objects(message, smallText, (0, 0, 0))
    textRect.center = (W // 2, H // 2 - 50)
    gameDisplay.blit(textSurf, textRect)

    # Display buttons
    button_width = 100
    button_height = 50
    button_gap = 20
    button_x = (W - button_width * 3 - button_gap * 2) // 2
    button_y = H // 2

    pygame.display.update()

    # Wait for user input
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        option1_button = message_button(option1, button_x, button_y, button_width, button_height, white, black, gameDisplay)
        option2_button = message_button(option2, button_x + button_width + button_gap, button_y, button_width, button_height, white, black, gameDisplay)
        option3_button = message_button("Do nothing", button_x + 2 * (button_width + button_gap), button_y, button_width, button_height, white, black, gameDisplay)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_1:
                    print("Option 1 selected")
                    event_number = event_number + 1
                    waiting_for_input = False
                elif event.key == pygame.K_2:
                    print("Option 2 selected")
                    event_number = event_number + 2
                    waiting_for_input = False
                elif event.key == pygame.K_3:
                    print("Option 3 Selected")
                    event_number = event_number + 3
                    waiting_for_input = False

        pygame.display.update()
    return event_number

def difficulty(gameDisplay):
    diff = ""
    gameDisplay.blit(bImg, (0, 0))
    messages = ["Choose the Difficulty"]
    random_message = random.choice(messages)
    instructions = "Movement: <- ^ v -> \n Attack: Spacebar \n Heal: R \n Pause: P"
    smallText = pygame.font.Font(None, 30)

    #Difficulty Message
    textSurf, textRect = text_objects(random_message, smallText, (0, 0, 0))
    textRect.center = (W // 2, H // 2 - 100)

    #Instructions Message
    textSurf1, textRect1 = text_objects(instructions, smallText, (0, 0, 0))
    textRect1.center = (W // 2, 500)

    gameDisplay.blit(textSurf, textRect)
    # Instructions Message
    lines = instructions.split('\n')
    for i, line in enumerate(lines):
        textSurf_line, textRect_line = text_objects(line, smallText, (0, 0, 0))
        textRect_line.center = (W // 2, 400 + i * 30)  # Adjust the vertical spacing
        gameDisplay.blit(textSurf_line, textRect_line)

    gameDisplay.blit(textSurf, textRect)

    # Display buttons
    button_width = 100
    button_height = 50
    button_gap = 20
    button_x = (W - button_width * 3 - button_gap * 2) // 2
    button_y = H // 2

    pygame.display.update()

    # Wait for user input
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        option1_button = message_button("Easy", button_x, button_y, button_width, button_height, white, black, gameDisplay)
        option2_button = message_button("Medium", button_x + button_width + button_gap, button_y, button_width, button_height, white, black, gameDisplay)
        option3_button = message_button("Hard", button_x + 2 * (button_width + button_gap), button_y, button_width, button_height, white, black, gameDisplay)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_1:
                    diff = "1"
                    waiting_for_input = False
                elif event.key == pygame.K_2:
                    diff = "2"
                    waiting_for_input = False
                elif event.key == pygame.K_3:
                    diff = "3"
                    waiting_for_input = False

        pygame.display.update()
    return diff
def attack(pAttack):
    damage = pAttack
    return damage

def block(pDefense, incDamage):
    pDamage = max(0, incDamage - pDefense)
    return pDamage

def drawHealthBar(surface, x, y, currHealth, maxHealth, color):
    bar_width = int((currHealth / maxHealth) * pSize)
    playerHealthRect = pygame.Rect(x, y, bar_width, 8)
    pygame.draw.rect(surface, color, playerHealthRect)
    monsterHealthRect = pygame.Rect(x, y, bar_width, 8)
    pygame.draw.rect(surface, color, monsterHealthRect)

def drawDHealthBar(surface, x, y, currHealth, maxHealth, color):
    dwidth = int((currHealth / maxHealth) * 200)
    dragonHealthRect = pygame.Rect(x, y, dwidth, 8)
    pygame.draw.rect(surface, color, dragonHealthRect)

# Define an empty list to hold room information--------------------------------------------------------------------
room_list = []


# Function to generate random room information
def generate_room(room):
    wall_list = []

    # 1
    if room == 0:
        wall_list.append(Wall(600, 20, 0, 0))
        wall_list.append(Wall(20, 790, 20, 0))

        # right wall with door
        wall_list.append(Wall(590, 20, 780, 360))
        wall_list.append(Wall(240, 20, 780, 20))

        # bottom wall with door
        wall_list.append(Wall(20, 340, 20, 580))
        wall_list.append(Wall(20, 360, 460, 580))

    # 2
    elif room < 9:
        wall_list.append(Wall(20, 790, 0, 0))

        # left wall with door
        wall_list.append(Wall(590, 20, 0, 360))
        wall_list.append(Wall(240, 20, 0, 20))

        # right wall with door
        wall_list.append(Wall(590, 20, 780, 360))
        wall_list.append(Wall(240, 20, 780, 20))

        # bottom wall with door
        wall_list.append(Wall(20, 340, 20, 580))
        wall_list.append(Wall(20, 360, 460, 580))
    # 3
    elif room == 9:
        wall_list.append(Wall(20, 790, 20, 0))
        wall_list.append(Wall(600, 20, 780, 0))

        # bottom wall with door
        wall_list.append(Wall(20, 340, 20, 580))
        wall_list.append(Wall(20, 360, 460, 580))

        # left wall with door
        wall_list.append(Wall(590, 20, 0, 360))
        wall_list.append(Wall(240, 20, 0, 20))
    # 4
    elif room % 10 == 0 and room < 40:
        wall_list.append(Wall(600, 20, 0, 0))

        # right wall with door
        wall_list.append(Wall(590, 20, 780, 360))
        wall_list.append(Wall(240, 20, 780, 20))

        # bottom wall with door
        wall_list.append(Wall(20, 340, 20, 580))
        wall_list.append(Wall(20, 360, 460, 580))

        # top wall with door
        wall_list.append(Wall(20, 340, 20, 0))
        wall_list.append(Wall(20, 360, 460, 0))

    # 5
    elif room == 40:
        wall_list.append(Wall(600, 20, 0, 0))
        wall_list.append(Wall(20, 790, 0, 580))

        # right wall with door
        wall_list.append(Wall(590, 20, 780, 360))
        wall_list.append(Wall(240, 20, 780, 20))

        # top wall with door
        wall_list.append(Wall(20, 340, 20, 0))
        wall_list.append(Wall(20, 360, 460, 0))

    # 6
    elif room > 40 and room < 49:
        wall_list.append(Wall(20, 790, 20, 580))

        # right wall with door
        wall_list.append(Wall(590, 20, 780, 360))
        wall_list.append(Wall(240, 20, 780, 20))

        # top wall with door
        wall_list.append(Wall(20, 340, 20, 0))
        wall_list.append(Wall(20, 360, 460, 0))

        # left wall with door
        wall_list.append(Wall(590, 20, 0, 360))
        wall_list.append(Wall(240, 20, 0, 20))
    # 7
    elif room == 49:
        wall_list.append(Wall(20, 790, 20, 580))
        wall_list.append(Wall(600, 20, 780, 0))

        wall_list.append(Wall(20, 790, 20, 0))

        wall_list.append(Wall(600, 20, 0, 0))

    # 8
    elif room % 10 == 9:
        wall_list.append(Wall(600, 20, 780, 0))

        # bottom wall with door
        wall_list.append(Wall(20, 340, 20, 580))
        wall_list.append(Wall(20, 360, 460, 580))

        # top wall with door
        wall_list.append(Wall(20, 340, 20, 0))
        wall_list.append(Wall(20, 360, 460, 0))

        # left wall with door
        wall_list.append(Wall(590, 20, 0, 360))
        wall_list.append(Wall(240, 20, 0, 20))
    # 9
    else:
        # right wall with door
        wall_list.append(Wall(590, 20, 780, 360))
        wall_list.append(Wall(240, 20, 780, 20))

        # left wall with door
        wall_list.append(Wall(590, 20, 0, 360))
        wall_list.append(Wall(240, 20, 0, 20))

        # bottom wall with door
        wall_list.append(Wall(20, 340, 20, 580))
        wall_list.append(Wall(20, 360, 460, 580))

        # top wall with door
        wall_list.append(Wall(20, 340, 20, 0))
        wall_list.append(Wall(20, 360, 460, 0))

    return wall_list


# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, height, width, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a grey wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill((grey))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    room_changed = False

    #Room changed direction
    direction = ""

    #for finishing the game
    finish = ""

    # Constructor function
    def __init__(self, x, y, w, h, vel, scale_factor=3):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = vel

        self.scale_factor = scale_factor
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        # Set height, width
        self.image = pygame.Surface([50, 50])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

        # Current room index
        self.current_room = 0  # Start in the first room

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
    
    # Change the speed of the player
    def resetSpeed(self):
        self.change_x = 0
        self.change_y = 0

    # Find a new position for the player
    def update(self, walls):
        # Get the old position, in case we need to go back to it
        old_x = self.rect.topleft[0]
        old_y = self.rect.topleft[1]

        # Update position according to our speed (vector)
        new_x = old_x + self.change_x
        new_y = old_y + self.change_y

        # Put the player in the new spot
        self.rect.topleft = (new_x, new_y)

        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.topleft = (old_x, old_y)

        # reset position if outside of screen----
        if new_x > 800:
            self.rect.topleft = (20, new_y)
            self.current_room = self.current_room + 1
            Player.room_changed = True
            Player.direction = "r"
        elif new_y > 600:
            self.rect.topleft = (new_x, 20)
            self.current_room = self.current_room + 10
            Player.room_changed = True
            Player.direction = "d"
        elif new_x < 0:
            self.rect.topleft = (790, new_y)
            self.current_room = self.current_room - 1
            Player.room_changed = True
            Player.direction = "l"
        elif new_y < 0:
            self.rect.topleft = (new_x, 590)
            self.current_room = self.current_room - 10
            Player.room_changed = True
            Player.direction = "u"
        if(Player.finish == "f"):
            Player.direction = "f"

player_x, player_y = 350, 250

# Create the player paddle object
player = Player(player_x, player_y, 32, 32, 5, scale_factor=3)
movingsprites = pygame.sprite.RenderPlain((player))


# This is the main function where our program begins
def main():
    score = 0
    # Constants from main.py - Andrew
    W, H = 800, 600
    pSize = 50
    pSpeed = 5
    pHealth = 100
    pAttack = 10
    pDefense = 5
    pHColor = (0, 255, 0)  # Green
    mSize = 50
    mSpeed = 1
    dSpeed = .5
    mHealth = 50
    mHColor = (255, 0, 0)  # Red
    pACooldown = 90000
    mACooldown = 200000
    pATimer = 0
    mATimer = 0
    dHealth = 200
    coinVal = random.randint(1, 10)
    coins = 0
    chestSize = 50
    chestSpeed = 0
    chestHealth = 10
    chestHColor = (255, 0, 0)
    chestACooldown = 200000
    chestATimer = 0
    heals = 3

    #difficulty Variable
    diff = ""

    #Event variable
    event_num = 0

    #number of statues
    statues_num = 0

    mList = ["ghost.png", "skeleton.png", "slime.png", "goblin.png", "zombie.png", "spider.png"]
    mImg = pygame.image.load(random.choice(mList))
    mImg = pygame.transform.scale(mImg, (mSize, mSize))
    dImg = pygame.image.load("dragon.png")
    dImg = pygame.transform.scale(dImg, (100, 100))
    chestList = ["chest.png"]
    chestImg = pygame.image.load(random.choice(chestList))
    chestImg = pygame.transform.scale(chestImg, (chestSize, chestSize))

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([800, 600])
    # Set the title of the window
    pygame.display.set_caption('Dungeon Crawler')
    # Enable this to make the mouse disappear when over our window
    # pygame.mouse.set_visible(0)
    # This is a font we use to draw text on the screen (size 36)
    font = pygame.font.Font(None, 36)

    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())
    # Used for converting color maps and such
    background = background.convert()
    # Fill the screen with a black background
    background.fill(black)

    walls = pygame.sprite.RenderPlain(generate_room(player.current_room))


    #INITIAL SCREEN WITH DIFFICLTY SELECTION
    diff = difficulty(screen)

    if(diff == "1"):
        print("Easy Mode Selected")
        heals = 4
        mSpeed = 0.70
        pHealth = 150
        
    elif(diff == "2"):
        #Default Difficulty, no changes to game values will be made
        print("Medium Mode Selected")
    else:
        print("Hard Mode Selected")
        mSpeed = 2
        pHealth = 70


    clock = pygame.time.Clock()

    # Added monster x, and y from main.py
    mDead = False
    chestDead = False
    monster_x = random.randint(0, W - mSize)
    monster_y = random.randint(0, H - mSize)
    chest_x = random.randint(0, W - chestSize)
    chest_y = random.randint(0, H - chestSize)

    dDead = False
    dragon_x = random.randint(0, W - 100)
    dragon_y = random.randint(0, H - 100)

    coin = None
    def spawnCoin():
        nonlocal coin
        coin = cImg.get_rect()
        coin.topleft = (monster_x + 50, monster_y + 50)

    princess = None
    def spawnPrincess():
        nonlocal princess
        princess = prImg.get_rect()
        princess.topleft = (dragon_x, dragon_y)

    powerup = None
    def spawn_speed_powerup():
        nonlocal powerup
        powerup = powerImg.get_rect()
        powerup.topleft = (monster_x + 50, monster_y + 50)

    # Set the initial time
    start_time = time.time()
    # Set the desired interval in seconds
    interval = 20

    running = True
    while running:
        clock.tick(40)

        # Check the elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        #HERE FILE COMMS
        if(Player.direction != "" or Player.finish == "f"):
            # Start the file_writer thread
            file_writer_thread = threading.Thread(target=file_writer)
            file_writer_thread.start()

        # getting the current player x and y
        player_x = player.rect.topleft[0]
        player_y = player.rect.topleft[1]

        # Monster Movement
        if not mDead:
            if monster_x < player_x:
                monster_x += mSpeed
            elif monster_x > player_x:
                monster_x -= mSpeed
            if monster_y < player_y:
                monster_y += mSpeed
            elif monster_y > player_y:
                monster_y -= mSpeed

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Player Movement
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == K_UP:
                    player.changespeed(0, -5)
                if event.key == K_DOWN:
                    player.changespeed(0, 5)
                if event.key == pygame.K_p:
                    paused(screen)

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    player.changespeed(5, 0)
                if event.key == K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == K_UP:
                    player.changespeed(0, 5)
                if event.key == K_DOWN:
                    player.changespeed(0, -5)
                if event.key == K_r and heals > 0:
                    pHealth += 100
                    heals -= 1
            
        if (elapsed_time >= interval):
            print(f"Timer reached {interval} seconds!")
                    
            event_num = timedEvent(screen)

            # Reset the player's movement
            player.resetSpeed()

            if event_num == 11:
                print("You go to investigate the sound")
                if(player.current_room != 49):
                    current_room = 49
                    Player.room_changed = True
            
            elif event_num == 12:
                print("You Waited for another sound")
                
            elif event_num == 13:
                print("You ignored the sound")
                
            elif event_num == 21:
                print("Game Over - You fell to your death!")
                running = False
                break
                
            elif event_num == 22:
                print("You ignored the hole")
                
            elif event_num == 23:
                print("You ignored the hole")
                
            elif event_num == 31:
                print("You drink the vial")
                pHealth += 50
                
            elif event_num == 32:
                print("You throw it away")
                pHealth -= 20
                
            elif event_num == 33:
                print("Keep the vial")
                heals += 1
                
            elif event_num == 41:
                print("Destroy the Statue")
                
            elif event_num == 42:
                print("Pick the Statue")
                pAttack += 30
                statues_num += 1
                if(statues_num == 3):
                    print("Game Over - The power of the statues was to much to handle!")
                    running = False
                    break

                
            elif event_num == 43:
                print("Ignore the Statue") 

                #Spawn a monster or next monster that spawns is faster/harder to kill
                mHealth = 150
                mSpeed = 4

                mDead = False

            # Reset the timer for the next interval
            start_time = time.time()

        player.update(walls)

        walls = pygame.sprite.RenderPlain(generate_room(player.current_room))

        # Check for collision
        playerRect = pygame.Rect(player.rect.topleft[0], player.rect.topleft[1], pSize, pSize)
        monsterRect = pygame.Rect(monster_x, monster_y, mSize, mSize)
        chestRect = pygame.Rect(chest_x, chest_y, chestSize, chestSize)

        currTime = pygame.time.get_ticks()
        pATimer += currTime
        mATimer += currTime
        if playerRect.colliderect(monsterRect) and not mDead:
            if mATimer >= mACooldown:
                if not keys[pygame.K_h]:
                    pHealth -= 10
                mATimer = 0
            if pATimer >= pACooldown:
                if keys[pygame.K_SPACE]:
                    mHealth -= (10 + 0.2*pAttack)
                pATimer = 0
            if pHealth <= 0:
                print("Game Over - Player defeated!")
                running = False
            elif mHealth <= 0:
                spawnCoin()
                coinVal = random.randint(1, 10)
                mDead = True
        if coin and playerRect.colliderect(coin):
            coin = None
            coins += coinVal

        if playerRect.colliderect(chestRect) and not chestDead:
            if chestATimer >= chestACooldown:
                if not keys[pygame.K_h]:
                    pHealth -= 1
                chestATimer = 0
            if pATimer >= pACooldown:
                if keys[pygame.K_SPACE]:
                    chestHealth -= 15
                pATimer = 0
            if pHealth <= 0:
                print("Game Over - Player defeated!")
                running = False
            elif chestHealth <= 0:
                spawn_speed_powerup()
                chestDead = True
        if powerup and playerRect.colliderect(powerup):
            powerup = None
            pAttack += 20

        # commented out which would draw the square representing the Player class instance
        # movingsprites.draw(screen)
        walls.draw(screen)
        pygame.display.flip()
        if (Player.room_changed == True):
            mDead = False
            mHealth = 50
            random_num = random.randint(1, 3)
            mImg = pygame.image.load(random.choice(mList))
            mImg = pygame.transform.scale(mImg, (mSize, mSize))
            monster_x = random.randint(0, W - mSize)
            monster_y = random.randint(0, H - mSize)
            if(random_num == 1):
                chestDead = False
                chestHealth = 10
                chest_x = random.randint(0, W - chestSize)
                chest_y = random.randint(0, H - chestSize)

        dragonRect = pygame.Rect(dragon_x, dragon_y, 200, 200)
        if (player.current_room == 49):
            interval = 100
            Player.room_changed = False
            dImg = pygame.image.load("dragon.png")
            dImg = pygame.transform.scale(dImg, (200, 200))
            if not dDead:
                if dragon_x < player_x:
                    dragon_x += dSpeed
                elif monster_x > player_x:
                    dragon_x -= dSpeed
                if dragon_y < player_y:
                    dragon_y += dSpeed
                elif dragon_y > player_y:
                    dragon_y -= dSpeed

            if playerRect.colliderect(dragonRect) and not dDead:
                if mATimer >= mACooldown:
                    if not keys[pygame.K_h]:
                        pHealth -= 10
                    mATimer = 0
                if pATimer >= pACooldown:
                    if keys[pygame.K_SPACE]:
                        dHealth -= (10 + 0.2*pAttack)
                    pATimer = 0
                if pHealth <= 0:
                    print("Game Over - Player defeated!")
                    Player.finish = "f"
                    running = False
                elif dHealth <= 0:
                    spawnPrincess()
                    dDead = True
        if princess and playerRect.colliderect(princess):
            print("Congratulations you saved the princess!")
            running = False


        if(player.current_room != 49):
            Player.room_changed = False

        # Draw everything
        screen.blit(bImg, (0, 0))
        screen.blit(pImg, (player.rect.topleft[0], player.rect.topleft[1]))
        drawHealthBar(screen, player.rect.topleft[0], player.rect.topleft[1], pHealth, 100, pHColor)
        if coin:
            screen.blit(cImg, coin)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(text, (20, 20))
        if not mDead:
            screen.blit(mImg, (monster_x, monster_y))
            drawHealthBar(screen, monster_x, monster_y, mHealth, 50, mHColor)
        if player.current_room == 49:
            mDead = True
            screen.blit(drImg, (0, 0))
            screen.blit(pImg, (player.rect.topleft[0], player.rect.topleft[1]))
            drawHealthBar(screen, player.rect.topleft[0], player.rect.topleft[1], pHealth, 100, pHColor)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Coins: {coins}", True, (255, 215, 0))
            if (dDead == False):
                screen.blit(text, (20, 20))
                screen.blit(dImg, (dragon_x, dragon_y))
                drawDHealthBar(screen, dragon_x, dragon_y, dHealth, 200, mHColor)
            if princess:
                screen.blit(prImg, princess)

        if powerup and chestDead:
            screen.blit(powerImg, powerup)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Power: {pAttack}", True, (255, 0, 0))
        screen.blit(text, (20, 40))
        if not mDead:
            screen.blit(mImg, (monster_x, monster_y))
            drawHealthBar(screen, monster_x, monster_y, mHealth, 50, mHColor)
        if not chestDead and player.current_room != 49:
            screen.blit(chestImg, (chest_x, chest_y))
            drawHealthBar(screen, chest_x, chest_y, chestHealth, 10, chestHColor)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Heals: {heals}", True, (0, 255, 0))
        screen.blit(text, (20, 60))


# This calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()

with open('communication.txt', 'r') as file:
    data = file.read()

    with open('communication.txt', 'w') as update_file:
        update_file.write("f")