#Valley of the Kings ~ The Undiscovered Tomb (TEXT ADVENTURE)
#CST 205
#Nautilus Group
#04 March 2017

import time
class Player:
    ######################################
    """
    The Player object will hold all info
    about the player themselves. This
    will include inventory later.
    """
    ######################################

    def __init__(self, start_x, start_y):
        ######################################
        """
        The 'position' variable corresponds to
        the player's position on a 2d map.
        At current, this corresponds to a room,
        but the same concept can be reused for
        different map types.

        Inventory is added here so you can
        have a really cool sword.
        """
        ######################################
        treasure = False
        self.position = {
            'x': start_x,
            'y': start_y
            }
        self.inventory = []

    def pickup_item(self, item): #Only
      inventory.append(item)

    def print_inventory(self):  #Prints item(s) in inventory
      for item in self.inventory:
        print(item, '\n')

class Room:
    ######################################
    """
    Rooms are the locations that the player
    might enter. Rooms have a name,
    a description, and actionable contents.
    """
    ######################################
    def __init__(self,name,description,item = None):
        self.name = name
        self.description = description
        self.item = item

    #Returns item in current room
    def get_item():
      return self.item


    def print_room(self):
        ######################################
        """
        We need a way to print the contents
        of a room and it is easier to do so
        from within the Room object itself.
        """
        ######################################
        printNow("%s\n%s"%(self.name,self.description))
        if self.item != None: #Ignore this for empty rooms.
            printNow("Upon searching the room you find %s"%(self.item))

    def intro_message(self):
      raise NotImplementedError()

    def modify_player(self, player):
      raise NotImplementedError()


######################################
"""
Global objects and variables are
declared first.

'n_rooms' is a list of all the Rooms
in our dungeon.

'n_dungeon' is a 2d list (or matrix)
that contains indices that correspond
to the rooms in 'n_rooms'. E.g. if
the matrix has a value of '0' that
corresponds to n_rooms[0], which
is the entryway.
"""
######################################


n_rooms = [
    Room('Corridor','You have arrived in the main corridor. To the south of you is the staircase leading out.','a key.'),
    Room('Well Room','You are in the middle of a large well room. The room is round.','gold.'),
    Room('Antechamber','This room is full of mirrors, shattered in thier frames.','a rope.'),
    Room('Hallway','This room is intricately decorated.','a sword.'),
    Room('Burial Chamber','This room is full of jars and a mummy sarcophagus.','jewels.'),
    Room('Treasury','This room is filled with treasure. All the walls are covered in hieroglyphics, except the west wall. Strange!','the treasure.'),
    Room('Secret Room', 'This room has a gold statue of Menes.','the statue.')
]

n_dungeon = [
            [-1, -1, -1, -1, -1],
            [-1, 6,  5,  4, -1],
            [-1, -1, -1 , 3, -1],
            [-1,  1,  0,  2, -1],
            [-1, -1, -1, -1, -1],
            ]

#This is the main function of the game.  Ra is an homage to the original working title of the game.
def Ra():
    ######################################
    """
    Step 1: Create a player and position
            them in the starting room.

    Step 2: We accept input from the user
            in the form of verb/noun
            pairs. We've stored what
            function calls to handle
            each verb in the 'verbs'
            dictionary. These Strings
            will be executed with the
            eval() function in python.

    Step 3: Print the information for
            the initial room.

    Step 4: Prompt the user for an input
            and execute the appropriate
            'verb.' A special case is
            'exit' or 'quit' which closes
            the game.
    """
    ######################################
    joe = Player(2,3) #Step 1

    #Toggles when the user is done playing. Initial value of done is determined by answers to the Prologue questions
    #done = prologue()
    done = prologue()
    treasure = False
    verbs = { #Step 2 #Future enhancements - add other interactions (i.e. drop, eat, drink)
        'move': 'move_player(joe,n_dungeon,noun)',
        'pickup': 'pickup_item(joe,n_dungeon,noun)'
    }

    print_help()  #Prints help menu telling user what the basic commands are for movement and interacting with items

    enter_room(joe,n_dungeon) #Step 3

    while not done:
        if 'statue' in joe.inventory:  #This is the win criteria for the game
          treasure = True
        if joe.position['x'] == 2 and joe.position['y'] == 3 and treasure == True:
          done = True
        if done == True:
            #Epilogue
            printNow('You just barely make it back to the Corridor without having awoken the mummies.  You glance back.')
            time.sleep(1)
            printNow('Part of you wants to go back and explore more, but you realize that adventure is better left to another day.')
            time.sleep(1)
            printNow('You have escaped the tomb with the treasure, the legendary statue of Menes!')
            time.sleep(1)
            showInformation('You win!')
            return 0
        #Step 4
        ans = requestString("What do you want to do? Type help for more instructions.")  #User prompt and input box for main game
        ans = str(ans).lower()  #Lowers user response to all lowercase to make it easier for comparing string values
        if ans == 'help':  #Brings up help menu anytime user types 'help'
          showInformation("""To navigate throughout the tomb use the verb 'move' followed by a space and a direction (north, east, south, or west).
          \nTo add an item to your inventory enter the verb 'pickup' followed by a space and the name of the item in the room.  Some items will come in handy later on in other rooms.
          \nThe goal is to find the hidden treasure and escape the tomb without waking the dead.""")
        if ans == 'exit' or ans == 'quit':
            break
        else:
            try:  #Takes user input and separates words into verb and noun pairs
                verb = ans.split(' ')[0]
                noun = ans.split(' ')[1]
                done = eval(verbs[verb])
                if verb != 'move':
                    enter_room(joe,n_dungeon)
                else:
                    if treasure and not (joe.position['x'] == 2 and joe.position['y'] == 3 and treasure == True): #Have the statue
                        printNow('KEEP RUNNING! The whole place is going to fall apart!')

            except:
                printNow('I do not recognize that input!')

#Function to print help menu
def print_help():
    hlp = """
    Welcome adventurer!

    \t1) To navigate throughout the tomb use the verb 'move' followed by a space and a direction (north, east, south, or west).

    \t2) To add an item to your inventory enter the verb 'pickup' followed by a space and the name of the item in the room.  Some items will come in handy later on in other rooms.

    \t3) The goal is to find the hidden treasure and escape the tomb without waking the dead.
    """
    printNow(hlp)

def enter_room(player,d_map):
    ######################################
    """
    Step 1: We try to figure out which
            rooms border this one. Currently,
            these will all have doors
            connecting to the current room.

    Step 2: Print the current room. Name,
            description, and contents.

    Step 3: Print a list of the doors
            we found in Step 1.
    """
    ######################################
    adj_rooms = []
    try: #Step 1
        if d_map[player.position['y']-1][player.position['x']] >= 0:
            adj_rooms.append('North')
        if d_map[player.position['y']+1][player.position['x']] >= 0:
            adj_rooms.append('South')
        if d_map[player.position['y']][player.position['x']-1] >= 0:
          if player.position['y'] == 1 and player.position['x'] == 2: #This accounts for the secret room.
            printNow("") #Do nothing
          else:
            adj_rooms.append('West')
        if d_map[player.position['y']][player.position['x']+1] >= 0:
            adj_rooms.append('East')
    except:
        pass

    printNow('')  #Prints a new line for clarity

    #Step 2
    n_rooms[d_map[player.position['y']][player.position['x']]].print_room()

    #Step 3
    if len(adj_rooms) > 0:
        output = "There are doors to the"
        for rm in adj_rooms:
            output += ' ' + rm + ','
        printNow(output[:-1] + '.')

#Picks up the key if player is in the room with the key and does not already have the key in inventory
def pickup_key(player,d_map):
    if n_rooms[d_map[player.position['y']][player.position['x']]].item == 'a key.':
        player.inventory.append('key')
        printNow("Your inventory now contains: %s"%player.inventory)
        n_rooms[d_map[player.position['y']][player.position['x']]].item = None; #Room reset to empty
    else:
        printNow("There is no key in this room.")

#Picks up the gold if player is in the room with the gold and does not already have the gold in inventory
def pickup_gold(player,d_map):
    if n_rooms[d_map[player.position['y']][player.position['x']]].item == 'gold.':
        player.inventory.append('gold')
        printNow("Your inventory now contains: %s"%player.inventory)
        n_rooms[d_map[player.position['y']][player.position['x']]].item = None;#Room reset to empty
    else:
        printNow("There is no gold in this room.")

#Picks up the statue if player is in the room with the statue and does not already have the statue in inventory
def pickup_statue(player,d_map):
    if n_rooms[d_map[player.position['y']][player.position['x']]].item == 'the statue.':
        player.inventory.append('statue')
        printNow("Your inventory now contains: %s"%player.inventory)
        n_rooms[d_map[player.position['y']][player.position['x']]].item = None;#Room reset to empty
        printNow('\nWhoa! That made something angry. The whole tomb is rumbling and shaking. You hear the sound of spiders and mummies heading toward you.\n\nRUN FOR THE ENTRANCE!!!')
    else:
        printNow("There is no statue in this room.")

#Picks up the treasure if player is in the room with the treasure and does not already have the treasure in inventory
def pickup_treasure(player,d_map):
    if n_rooms[d_map[player.position['y']][player.position['x']]].item == 'the treasure.':
        player.inventory.append('treasure')
        printNow("Your inventory now contains: %s"%player.inventory)
        n_rooms[d_map[player.position['y']][player.position['x']]].item = None;#Room reset to empty
    else:
        printNow("There is no treasure in this room.")

#Picks up the jewels if player is in the room with the jewels and does not already have the jewels in inventory
def pickup_jewels(player,d_map):
    if n_rooms[d_map[player.position['y']][player.position['x']]].item == 'jewels.':
        player.inventory.append('jewels')
        printNow("Your inventory now contains: %s"%player.inventory)
        n_rooms[d_map[player.position['y']][player.position['x']]].item = None;#Room reset to empty
    else:
        printNow("There are no jewels in this room.")

#Picks up the rope if player is in the room with the rope and does not already have the rope in inventory
def pickup_rope(player,d_map):
    if n_rooms[d_map[player.position['y']][player.position['x']]].item == 'a rope.':
        player.inventory.append('rope')
        printNow("Your inventory now contains: %s"%player.inventory)
        n_rooms[d_map[player.position['y']][player.position['x']]].item = None;#Room reset to empty
    else:
        printNow("There is no rope in this room.")

#Picks up the sword if player is in the room with the sword and does not already have the sword in inventory
def pickup_sword(player,d_map):
    if n_rooms[d_map[player.position['y']][player.position['x']]].item == 'a sword.':
        player.inventory.append('sword')
        printNow("Your inventory now contains: %s"%player.inventory)
        n_rooms[d_map[player.position['y']][player.position['x']]].item = None;#Room reset to empty
    else:
        printNow("There is no sword in this room.")

#Evaluates the item entered by user and attempts to run the correct function.
#Always returns false to keep game running (done = false)
def pickup_item(player, d_map, item):
    items = {
        'key': 'pickup_key(player,d_map)',
        'gold': 'pickup_gold(player,d_map)',
        'treasure': 'pickup_treasure(player,d_map)',
        'jewels': 'pickup_jewels(player,d_map)',
        'rope': 'pickup_rope(player,d_map)',
        'sword': 'pickup_sword(player,d_map)',
        'statue': 'pickup_statue(player,d_map)'
    }
    try:

        eval(items[item.lower()])
        return False
    except:
        printNow('Not a valid item to pick up!')

def move_north(player,d_map):
    ######################################
    """
    This function moves a player 'north',
    which is where position['y'] -= 1

    The rest of the function is there to
    make sure we CAN move north.

    Check 1: Is there a place to the north
            on the dungeon map?

    Check 2: Is there a valid room to the
            north?


    """
    ######################################
    if player.position['y'] - 1 >= 0: #Check 1
        if d_map[player.position['y']-1][player.position['x']] >= 0: #Check 2
          #We can't move north without a key, so that's checked here.
          if 'key' in player.inventory:
            player.position['y'] = player.position['y'] - 1
            printNow("You use the key to open the locked door.")
            enter_room(player,d_map)
            printNow('You hear the sound of shuffling feet, unearthly moans, and a strange insectile screeching. It\'s hard to tell, but the noise might be coming from the South of you!')
          else:
            printNow("This door is locked. Try finding and picking up the key.")
        else:
            printNow('There is no door to the north!')
    else:
        printNow('There is no door to the north!')
    return False

def move_south(player,d_map):
    ######################################
    """
    This function moves a player 'south',
    which is where position['y'] += 1

    The rest of the function is there to
    make sure we CAN move south.

    Check 1: Is there a place to the south
            on the dungeon map?

    Check 2: Is there a valid room to the
            south?
    """

    if player.position['y'] + 1 < len(d_map): #Check 1
        if d_map[player.position['y']+1][player.position['x']] >= 0: #Check 2
          if 'sword' in player.inventory: #If you move too far south without the sword you die.
            printNow("You use the sword to fight off the giant spiders.")
            player.position['y'] = player.position['y'] + 1
            enter_room(player,d_map)
          elif player.position['y'] < 2:
            printNow("You begin to wish you had picked up the sword as a band of mummies rush through the door and quickly consume your soul.")
            showInformation("You Lose!")
            return True
          else:
            printNow("Your path is blocked by giant spiders.  You must find something to fight them off.")
        else:
            printNow('There is no door to the south!')
    else:
        printNow('There is no door to the south!')
    return False

def move_west(player,d_map):
    ######################################
    """
    This function moves a player 'west',
    which is where position['x'] -= 1

    The rest of the function is there to
    make sure we CAN move west.

    Check 1: Is there a place to the west
            on the dungeon map?

    Check 2: Is there a valid room to the
            west?
    """
    ######################################

    if player.position['x'] - 1 >= 0: #Check 1
        if d_map[player.position['y']][player.position['x']-1] >= 0: #Check 2
          if 'rope' in player.inventory: #Can't go down the crevice w/o the rope
            player.position['x'] = player.position['x'] - 1
            printNow("You use the rope to climb down the steep crevice.")
            enter_room(player,d_map)
          else:
            printNow("You open the door and see a massive crevice.  Try finding something to climb down.")
        else:
            printNow('There is no door to the west!')
    else:
        printNow('There is no door to the west!')
    return False

def move_east(player,d_map):
    ######################################
    """
    This function moves a player 'east',
    which is where position['x'] += 1

    The rest of the function is there to
    make sure we CAN move east.

    Check 1: Is there a place to the east
            on the dungeon map?

    Check 2: Is there a valid room to the
            east?
    """
    ######################################
    if player.position['x'] + 1 < len(d_map[0]):
        if d_map[player.position['y']][player.position['x']+1] >= 0:
            player.position['x'] = player.position['x'] + 1;
            enter_room(player,d_map)
        else:
            printNow('There is no door to the east!')
    else:
        printNow('There is no door to the east!')
    return False

def move_player(player, d_map, direction):
    ######################################
    """
    This function allows us to move
    any direction with a single call.

    We use a try/except pair to make sure
    that only directions with key values
    in the direc dictionary are able to be
    called.
    """
    ######################################
    direc = {
        'north': 'move_north(player,d_map)',
        'south': 'move_south(player,d_map)',
        'east': 'move_east(player,d_map)',
        'west': 'move_west(player,d_map)'
    }
    try:
        return eval(direc[direction.lower()])
    except:
        printNow('Not a valid movement direction! Please choose north, south, east, or west.')




def story_intro(): #Flavor  #Used import time to add dramatic pauses as text prints for the user
  printNow("For nearly 500 years, Egyptian pharaohs and kings were buried in the 'The Great and Majestic Necropolis'.")
  time.sleep(2)
  printNow("Hundreds of tombs were cut out of the rock . Vast labyrinths connected burial chambers, treasury rooms, libraries, altars, and more.")
  time.sleep(2)
  printNow("In the late 16th century, the royal burials stopped.  Centuries went by as the tombs lay undisturbed,")
  time.sleep(2)
  printNow("nearly forgotten, except as retold in fables and myths.  In 1985 the first tomb of Rameses VII was discovered.")
  time.sleep(2)
  printNow("Over the next 30 years, over 60 tombs of some of the most powerful rulers ever to live would be unearthed.")
  time.sleep(2)
  printNow("But the greatest tomb of them all lay undisturbed and discovered...")
  time.sleep(4)
  printNow("...that is...")
  time.sleep(4)
  printNow("...until now!")

def story_welcome(): #Flavor  #Used import time to add dramatic pauses as text prints for the user
  printNow("Welcome explorer!  You are a young archeologist on a trip to explore the already discovered ruins of the Valley of the Kings.")
  time.sleep(2)
  printNow("You are there for a research trip as part of your university studies.  You strayed away from your group to explore and take some pictures")
  time.sleep(2)
  printNow("when you noticed something peculiar nearby.  On a wind blown rock wall was a symbol you recalled from an old Egyptian book you read recently.")
  time.sleep(2)
  printNow("The symbol was for a mythological Egyptian pharaoh named Menes who, as legend tells,")
  time.sleep(2)
  printNow("was the first king to unite both the Upper and Lower parts of Egypt and create the 1st Egyptian Dynasty.")

def second_choice(): #Flavor  #If user chooses 'yes', this choice launches the main game
  answer = ""
  while answer != "yes" and answer != "no":
    answer = requestString("Do you dare enter the passageway? (Yes or No):")
    answer = answer.lower()
    if answer == "no":
      printNow("You have made a monumental discovery, but you need a team and proper equipment to explore.")
      time.sleep(2)
      printNow("You hurry back to your group to tell the others.")
      time.sleep(2)
      printNow("As you make your way back to the group, the passageway seals behind you never to be found again.")
      time.sleep(1)
      showInformation("YOU LOSE!")
      return True
    elif answer == "yes":
      printNow("Adventure is not for the faint of heart.  You enter the passageway and begin to descend the staircase.")
      return False
    else:
      showWarning("You must enter either 'yes' or 'no'")

def first_choice(): #Flavor  #First choice in prologue. User must choose 'yes' in order to advance towards start of game
  answer = ""
  while answer != "yes" and answer != "no":
    answer = requestString("Should you go in for a closer look? (Yes or No):")
    answer = answer.lower()
    if answer == "no":
      printNow("You realize that discoveries and adventures are for real archeologists and not young students.")
      time.sleep(2)
      printNow("You head back to the safety of your group never to know the mysteries that lay nearby.")
      time.sleep(1)
      showInformation("YOU LOSE!")
      return True
    elif answer == "yes":
      printNow("Upon closer inspection you confirm this is the symbol for Menes, the legendary ruler of the 1st Dynasty.")
      time.sleep(2)
      printNow("How can this be?  How is it that you have made this discovery?")
      time.sleep(2)
      printNow("As you lean closer to inspect the rock wall, your elbow bumps a loose stone and a passageway appears before your very eyes.")
      time.sleep(2)
      printNow("Ahead of you is a dark staircase leading deep below the sand.  This is your moment.")
      return second_choice()
    else:
      showWarning("You must enter either 'yes' or 'no'")

def prologue(): #Plays the Prologue
  story_intro()
  time.sleep(2)
  story_welcome()
  time.sleep(2)
  done = first_choice()
  return done  #This returns done and launches the main game if the user has chosen 'yes' for both responses
