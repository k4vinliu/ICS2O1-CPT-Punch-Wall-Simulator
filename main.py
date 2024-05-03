#Kevin Liu
#ICS2O1 -  CPT
#June 19th, 2023
#Verified by: Terrence Fu

#Punch Wall Simulator V1 (Comes with animations making it somewhat laggy)

'''SOME INFORMATION REGARDING GAME'''
#Maximize game window for better experience (window size is 1920x960)
#Sometimes it randomly zooms in to one area and doesn't display everything (I think it's because if you go to Start > Settings > System > Display, the scale is default set to 150% so you have to set it to 100%)
#V1 is limited to only three gloves and three pets. Later versions will have more.

'''Instructions'''
#1. Click the red button to gain one power point
#2. Buy gloves to increase power points gained per click (only the most recent glove bought is equipped)
#3. Buy pets to help generate power points autimatically (you can buy multiple of the same pets but price increases by 15% each time)

#Import pygame and modules
import pygame
pygame.init()

'''Pets'''
#Load the images and icons for the pets
cat_img = pygame.image.load('cat.png')
dog_img = pygame.image.load('dog.png')
wolf_img = pygame.image.load('wolf.png')
cat_icon = pygame.image.load('cat_icon.png')
dog_icon = pygame.image.load('dog_icon.png')
wolf_icon = pygame.image.load('wolf_icon.png')

'''Gloves'''
redGloves_img = pygame.image.load('redGloves.jpg')
blueGloves_img = pygame.image.load('blueGloves.jpg')
blackGloves_img = pygame.image.load('blackGloves.jpg')

'''Colors'''
#Set color codes for some colors that are going to be used
DARK_BLUE = (51, 90, 114)
WHITE = (255, 255, 255)
LIGHT_GREEN = (0, 255, 0)
GRAY = (155, 155, 155)

#Load images
background_img = pygame.image.load('wall.png') #Background image (the wall)
button_img = pygame.image.load('buttonn.png') #Button image
man_img = pygame.image.load('manpunching.png') #Man punching image
title_img = pygame.image.load('title.png') #Title
instructions_img = pygame.image.load('instructions.PNG') #Instructions

class MainButton: #Make the button object
  def __init__(self, x, y): #Initialize MainButton by setting its position, size, and animation state
    self.x = x #X coordinate on window
    self.y = y #Y coordinate on window
    self.length = 250 #Length of button
    self.height = 250 #Height of button
    self.animation_state = 0  #Animation state of button
  def draw(self): #Draw and make the button look animated, override main draw function
    if self.animation_state > 0: #Make the button shrink then go back to regular size
      button_img_scaled = pygame.transform.scale(button_img, (int(0.9 * self.length), int(0.9 * self.height)))
      window.blit(button_img_scaled, (button_img_scaled.get_rect(center =( int(self.x + self.length/2), int(self.y + self.height/2)))))
      self.animation_state -= 1
    else:
      window.blit(button_img, (button_img.get_rect(center = (int(self.x + self.length/2), int(self.y + self.height/2)))))
  def collidepoint(self, mouse_pos): #Render the user clicking the button
    return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)

class Scoreboard(): #Define scoreboard object to keep track of power points
  def __init__(self, x, y): #Initialize scoreboard by setting its position and size
    self.x = x
    self.y = y
    self.length = 100
    self.height = 100
  def draw(self): #Override main draw function to draw the scoreboard with custom font
    #Set the font
    font = pygame.font.Font('Morning Beach.ttf', 24) #Import the custom font that will be used for the whole game
    SCORE = font.render('{} power points'.format(int(user.score)), True, WHITE) #Text for the amount of power points user has
    PERSECOND = font.render('power points generated per second: {}'.format(user.persecond), True, WHITE) #Text for number of power points user gains per second
    #Draw the scoreboard info
    window.blit(SCORE, (SCORE.get_rect(center = (int(self.x + self.length/2), int(self.y + self.height/2)))))
    window.blit(PERSECOND, PERSECOND.get_rect(center = (int(self.x + self.length/2), int(self.y + self.height/2 + 20))))

class Pet: #Define the Pet object (cat, dog, and wolf all fall under the parent pet class)
  def __init__(self, name, x, y, image, icon, base_cost, increase, pps): #Initialize the pet by setting its position, image, icon, and ability
    self.name = name #Name of pet
    self.x = x 
    self.y = y 
    self.length = 300
    self.height = 64
    self.image = image
    self.icon = icon
    self.base_cost = base_cost 
    self.increase = increase 
    self.pps = pps #Power points per second
    self.quantity = 0 
    self.created = 0
  def collidepoint(self, mouse_pos): #Render if user clicks pet
    return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos)
  def getCost(self): #Updates and returns the cost to buy the pet (increases cost to purchase the same pet)
    return self.base_cost * self.increase ** (self.quantity)
  def draw(self, solid = True): #Transparent if user can't afford to purchase, becomes opaque when user can
    pets_cost_font = pygame.font.Font('Morning Beach.ttf', 24)
    pets_quantity_font = pygame.font.Font('Morning Beach.ttf', 24)
    cost = pets_cost_font.render('{}'.format(format_number(int(self.getCost()))), True, LIGHT_GREEN) #Display the cost in light green
    quantity = pets_quantity_font.render('{}'.format(self.quantity), True, GRAY) #Display the number of each pet bought in grey
    icon = self.image
    if solid == False:
      icon.set_alpha(200) #Makes image look transparent
    else:
      icon.set_alpha(1000) #Makes image look opaque
    #Display pet, cost, and quantity on the right hand side of the screen
    window.blit(icon, (self.x, self.y))
    window.blit(cost, (self.x + 115, self.y + self.height - 1))
    window.blit(quantity, (self.x + self.length - 40, self.y + 10))

class Glove: #Define the glove object by setting its position, image, cost, and ability
  def __init__(self, name, x, y, image, cost, cm, purchased):
    self.name = name
    self.x = x
    self.y = y
    self.length = 200
    self.height = 200
    self.image = image
    self.cost = cost
    self.cm = cm #Click multiplier 
    self.purchased = False #Check whether glove is already purchased
  def collidepoint(self, mouse_pos):
    return pygame.Rect(self.x, self.y, self.length, self.height).collidepoint(mouse_pos) #Render the user clicking the gloves
  def getCost(self):
    return self.cost #Return cost of glove
  def draw(self, solid = True):
    glove_cost_font = pygame.font.Font('Morning Beach.ttf', 24)
    glove_cost = glove_cost_font.render('{}'.format(format_number(int(self.getCost()))), True, LIGHT_GREEN) #Display cost of glove in light green
    glove_purchased = glove_cost_font.render('purchased', True, DARK_BLUE) #Display word "purchased" in dark blue so user knows they already purchased it
    if solid == False:
      self.image.set_alpha(200) #Transparnet
    else:
      self.image.set_alpha(1000) #Opaque
    window.blit(self.image, (self.x, self.y))
    window.blit(glove_cost, (self.x + 115, self.y + self.height - 1))
    if self.purchased == True: #Display "purchased" is user purchases glove
      window.blit(glove_purchased, (self.x + 105, self.y + self.height - 18))

class Player: #Define player object
  def __init__(self): #Initialize player by setting its score and upgrades to default values (no upgrades or pets)
    self.score = 0 #Default power points set to 0
    self.click_multiplier = 1 #Default power points per click set to 1
    self.persecond = 0 #Default power points gained per second set to 0
  def updateTotalPPS(self, pet_list): #Update power points per second
    self.persecond = 0
    for pet in pet_list: 
      self.persecond += pet.pps * pet.quantity

#Set window dimensions to the size of background image
windowLength = 1920
windowHeight = 960
window = pygame.display.set_mode((windowLength, windowHeight))

#Create the button, scoreboard, and user object
button = MainButton(100, 100)
score_board = Scoreboard(180, 0)
user = Player()

#Create building objects
store_pos = 212
cat = Pet('Cat', 1450, store_pos, cat_img, cat_icon, base_cost = 50, increase = 1.15, pps = 1)
dog = Pet('Dog', 1450, store_pos + 64*2, dog_img, dog_icon, base_cost = 100, increase = 1.15, pps = 2)
wolf = Pet('Wolf', 1450, store_pos + 64*4, wolf_img, wolf_icon, base_cost = 1000, increase = 1.15, pps = 10)
pet_list = [cat, dog, wolf]

#Create glove objects
glove_pos = 230
redGlove = Glove('Red Glove', 1000, glove_pos, redGloves_img, cost = 500, cm = 2, purchased = False)
blueGlove = Glove('Blue Glove', 1000, glove_pos + 115 * 2, blueGloves_img, cost = 1000, cm = 3, purchased = False)
blackGlove = Glove('Black Glove', 1000, glove_pos + 115 * 4, blackGloves_img, cost = 5000, cm = 5, purchased = False)
glove_list = [redGlove, blueGlove, blackGlove]

def format_number(n): #Python formatting function for floats
    if n >= 1000000000:
        if (n / 1000000000 ) % 1 == 0:
            n = '{:.0f} billion'.format(n / 1000000000) #Format float with no decimal places
        else:
            n = '{:.2f} billion'.format(n / 1000000000) #Format float 2 decimal places
    elif n >= 1000000:
        if (n / 1000000) % 1 == 0:
            n = '{:.0f} million'.format(n / 1000000) 
        else:
            n = '{:.2f} million'.format(n / 1000000)
    return n 
      
def draw(): #Main draw function
  #Draw the background
  window.blit(background_img, (0, 0))
  #Draw button
  button.draw()
  #Draw man
  window.blit(man_img, (500, 300))
  #Draw title
  window.blit(title_img, (600, 40))
  #Draw instructions
  window.blit(instructions_img, (50, 500))
  #Draw scoreboard
  score_board.draw()
  #Draw pets
  for pet in pet_list:
    if(user.score >= pet.getCost()): #See if user can afford the pet
      pet.draw(solid = True)
    else:
      pet.draw(solid = False)
    #Add power points generated by pets
    user.score += pet.quantity * pet.pps * .05
    pet.created += pet.quantity * pet.pps * .01
  #Draw gloves
  for glove in glove_list:
    if(user.score >= glove.getCost() and glove.purchased == False): #See if user can afford glove and hasn't purchased it already
      glove.draw(solid = True)
    else:
      glove.draw(solid = False)
  pygame.display.update() #Update display
  
main = True
while main == True: #While loop for the game
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN: #User clicks something
      mouse_pos = event.pos
      if button.collidepoint(mouse_pos): #Clicks button
        #Add power points and play animation
        user.score += 1 * user.click_multiplier
        button.animation_state = 1
      for pet in pet_list:
        if pet.collidepoint(mouse_pos) and user.score >= pet.getCost(): #Clicks pet
          #Buy the pet and update values
          user.score -= pet.getCost()
          pet.quantity += 1
          user.updateTotalPPS(pet_list)
      for glove in glove_list:
        if glove.collidepoint(mouse_pos) and user.score >= glove.getCost() and glove.purchased == False: #Clicks glove
          #Buy glove and update values
          user.score -= glove.getCost()
          user.click_multiplier = glove.cm
          glove.purchased = True 
    if event.type == pygame.QUIT:
      main = False     
  draw() #Calling the main draw function to draw everything
pygame.quit() #Quit game (everything restarts and values get set to default again)