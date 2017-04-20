from random import shuffle
from random import randint
from time import sleep

isPathSet = False


class Room:
  #Initializes every room to have no surrounding rooms and to be in an unlocked state
  north = None
  east = None
  south = None
  west = None
  up = None
  down = None
  locked = false

  isPainted = False
  def __init__(self, name, description, items,coords = (0,0)):
    self.name = name
    self.description = description
    self.items = items
    self.huds = {}
    self.make_huds()
    self.coords = coords

  def make_huds(self):
      global isPathSet
      if not isPathSet:
          setMediaFolder()
          isPathSet = True

      hud_normal = makePicture('assets\\images\\huds\\%s HUD.jpg'%self.name)
      hud_red = makePicture('assets\\images\\huds\\%s Red HUD.jpg'%self.name)
      hud_green = makePicture('assets\\images\\huds\\%s Green HUD.jpg'%self.name)

      title_font_size = 77-16
      sty = makeStyle(sansSerif,bold,title_font_size)
      addTextWithStyle(hud_normal,32+title_font_size,70,self.name,sty,black)
      addTextWithStyle(hud_red,32+title_font_size,70,self.name,sty,black)
      addTextWithStyle(hud_green,32+title_font_size,70,self.name,sty,black)
      self.huds['normal']=hud_normal
      self.huds['red']=hud_red
      self.huds['green']=hud_green

  def get_hud(self,index):
      return self.huds[index]
  def add_hud_description(self, desc,type):
      font_size = 25
      isLong = False
      if len(desc) > 450:
          font_size = 15
          isLong = True

      sty = makeStyle(sansSerif,bold,font_size)
      #Text Area: width (x): 30-842; height (y): 602-863
      ln = desc.split('\n')
      line_num = 0
      for line in ln:
          lines = txt_to_lines(line,font_size,isLong)
          for l in lines:
              line_num += 1
              addTextWithStyle(self.huds[type],32,604+font_size*line_num,l,sty,black)
          line_num += 1


  #Allows rooms to be placed in various locations around current room object
  def setNorth(self, room):
    self.north = room
  def setSouth(self, room):
    self.south = room
  def setEast(self, room):
    self.east = room
  def setWest(self, room):
    self.west = room
  def setDown(self, room):
    self.down = room
  def setUp(self, room):
    self.up = room
  #Returns the adjacent rooms of the current room
  def getNorth(self):
    return self.north
  def getSouth(self):
    return self.south
  def getEast(self):
    return self.east
  def getWest(self):
    return self.west
  def getDown(self):
    return self.down
  def getUp(self):
    return self.up
  #Returns if the room is locked or not
  def isLocked(self):
    return self.locked
  #Sets the state of a room to locked or unlocked
  def setLocked(self, locked):
    self.locked = locked

  #Returns the name of the room object
  def getName(self):
    return self.name

  #Returns the description of the room object
  def getDescription(self):
    return self.description

  #Sets the description of room
  def setDescription(self, description):
    self.description = description

  #Returns the list of items in the room object
  def getItems(self):
    return self.items

  #Adds an item to the list of items in the room
  def addItem(self, item):
    self.items.append(item)

  #Removes an item from the room
  def removeItem(self, item):
    self.items.remove(item)

  #Creates a string of all the adjacent rooms to the current room
  def getAdjacentRooms(self):
    adjRooms = ""
    if self.north != None:
      adjRooms = adjRooms + "To the north is the %s. "%self.north.getName()
    if self.east != None:
      adjRooms = adjRooms + "To the east is the %s. "%self.east.getName()
    if self.south != None:
      adjRooms = adjRooms + "To the south is the %s. "%self.south.getName()
    if self.west != None:
      adjRooms = adjRooms + "To the west is the %s. "%self.west.getName()
    if self.down != None:
      adjRooms = adjRooms + "Below you is the %s. "%self.down.getName()
    if self.up != None:
      adjRooms = adjRooms + "Above you is the %s. "%self.up.getName()
    return adjRooms

  #Returns image path
  def getImagePath(self):
    return self.img_path
  #Prints the room object as a string
  def __str__(self):
    return ("%s: %s.  This room contains %s\n%s\n")%(self.name, self.description, self.items,self.getAdjacentRooms())

class Player:
  #The items the player is holding
  inventory = []
  #Has secret room been found?
  secretRoomFound = false
  #Is the safe locked
  safeLocked = true
  #variables for examined objects. This is to prevent spawning multiple Page Pieces.
  floorMatDone = false
  portraintDone = false
  couchDone = false
  portraitDone = false
  #Holds the room that the current player is in
  currentRoom = None
  #is the player under the effects of a potion
  hasDrunkRed = False
  hasDrunkGreen = False
  def __init__(self, name, room):
    self.name = name
    self.currentRoom = room
    self.hud = None
  #Returns name of current player
  def getName(self):
    return self.name


  ###Pickup Item Function###
  #step 1: Don't pickup if item is already in inventory
  #step 2: Make sure item is in current room
  #step 3: Print "Item not found" if item not in current room
  def pickupItem(self, item):
    #Check if player is already holding that item
    if 'Page Piece' in item:
        #Quotes from _Twenty Thousand Leagues Under the Sea_, by Jules Verne
        #http://www.gutenberg.org/files/2488/2488-h/2488-h.htm
      nautilus_text = {
        'Page Piece 1': '"Fine," I replied, "but the Nautilus lives in a separate world, and the secrets of its scientists don\'t make their way ashore."',
        'Page Piece 2': 'Just remember one thing: I owe everything to the ocean; it generates electricity, and electricity gives the Nautilus heat, light, motion, and, in a word, life itself.',
        'Page Piece 3': 'It was a squid of colossal dimensions, fully eight meters long. It was traveling backward with tremendous speed in the same direction as the Nautilus.',
        'Page Piece 4': ' The Nautilus wasn\'t going to strike the double-decker where it was clad in impenetrable iron armor, but below its waterline, where the metal carapace no longer protected its planking.'
      }
      showInformation('You pickup the fragile page and read \'%s\' before it crumbles into dust.'%nautilus_text[item])
      try:
          self.currentRoom.removeItem(item)
      except:
          pass
    elif item in self.inventory:
      printNow("You are already carrying that item")
      showInformation("You are already carrying that item")
    else:
      #Check if item is in the current room
      if item in self.currentRoom.getItems():
        if item == "Tape" or item == "Matches":
          printNow("This might come in handy later")
          showInformation("This might come in handy later")


        if item == "Lantern":
          printNow("This will come in very handy.  Now if only I can find some matches to actually light it with.")
          showInformation("This will come in very handy.  Now if only I can find some matches to actually light it with.")
        self.inventory.append(item)
        self.currentRoom.removeItem(item)
        printNow("You are now holding: %s"%self.inventory)
        #showInformation("You are now holding: %s"%self.inventory)
        printNow("The room now contains: %s"%self.currentRoom.getItems())
        #showInformation("The room now contains: %s"%self.currentRoom.getItems())
      #If item is not in current room, print item not found
      else:
        printNow("Item not found")
        showInformation("Item not found")

  ###Drop Item Function###
  #step 1: If player is holding item, add the item to current room items and remove from player inventory
  #step 2: If player does not have item, print "you do not have that item"
  def dropItem(self, item):
    if item in self.inventory:
      self.currentRoom.addItem(item)
      self.inventory.remove(item)
      printNow("You are now holding: %s"%self.inventory)
      printNow("The room now contains: %s"%self.currentRoom.getItems())
    else:
      printNow("You do not have that item!")
      showInformation("You do not have that item!")

  #Returns the current inventory list of the user
  def getInventory(self):
    return self.inventory

  ###Move Player Functions###
  #step 1: Move the current player North,South,East, or West if there is a valid room in that direction.
  #step 2: If there is no room in that direction, alert the user
  def movePlayerNorth(self):
    if self.currentRoom.getNorth().getName() == "Living Room" and self.currentRoom.getNorth().isLocked():
      printNow("The door is locked.  You need a key.")
      showInformation("The door is locked.  You need a key.")
    else:
      if self.currentRoom.getNorth() != None:
        self.currentRoom = self.currentRoom.getNorth()
        printNow(self.currentRoom)
      else:
        printNow("There is no room to the North!")
        showInformation("There is no room to the North!")

  def movePlayerSouth(self):
    if self.currentRoom.getSouth() != None:
      self.currentRoom = self.currentRoom.getSouth()
      printNow(self.currentRoom)
    else:
      printNow("There is no room to the South!")
      showInformation("There is no room to the South!")

  def movePlayerEast(self):
    if self.currentRoom.getEast() != None:
      self.currentRoom = self.currentRoom.getEast()
      printNow(self.currentRoom)
    else:
      printNow("There is no room to the East!")
      showInformation("There is no room to the East!")

  def movePlayerWest(self):
    if self.currentRoom.getWest() != None:
      self.currentRoom = self.currentRoom.getWest()
      printNow(self.currentRoom)
    else:
      printNow("There is no room to the West!")
      showInformation("There is no room to the West!")

  def movePlayerUp(self):
    if self.currentRoom.getUp() != None:
      self.currentRoom = self.currentRoom.getUp()
      printNow(self.currentRoom)
    else:
      printNow("There is no room above you!")
      showInformation("There is no room above you!")

  ###Only used to enter basement so user must have lit lantern equipped to see###
  def movePlayerDown(self):
    if self.currentRoom.getDown() != None:
      self.currentRoom = self.currentRoom.getDown()
      if "Lit Lantern" in self.inventory:
        self.secretRoomFound = true
        self.currentRoom.setDescription("""The basement is littered with old AV equipment.  Broken projectors, cassette recorders, televisions, and more.  In the corner is a furnace.
        As your eyes adjust, you notice a poster for E.T. hanging on the wall.  That seems a little odd.""")
        #show(self.create_hud())
      else:
        self.currentRoom.setDescription("The basement is completely dark.  You cannot see anything.  It would not be safe to explore here unless you can find some sort of light source.")
        printNow(self.currentRoom)

        isDone = False
        while not isDone:
            ans = requestString("The room is completely dark. Do you explore anyway? (y/n)").lower()
            if ans == 'y':
                showInformation('You enter the room, stumbling around in the dark until you hear the sound of disembodied voices singing for you to \'go anywhere.\' Panicked, you run for home!')
                showInformation('You\'ve run home crying to your momma. You lose!')
                isDone = True
                return 'lost'
            elif ans == 'n':
                isDone = True

    else:
      printNow("There is no room below you!")
      showInformation("There is no room below you!")

  #Function that simulates one die being rolled
  #Uses random int generator from python library
  def rollDie():
    dieRoll = random.randint(0,6)
    return dieRoll

  #Function that simulates two die being rolled
  #Uses random int generator from python library
  def rollDice():
    diceRoll = rollDie() + rollDie()
    return diceRoll

  #Main function for craps game
  def craps():
    showInformation('Ready to Play Craps?')
    firstDiceRoll = rollDice()
    showInformation('You rolled a ' + str(firstDiceRoll) + '.')
    if firstDiceRoll == 7 or firstDiceRoll == 11:  #Compares initial dice roll to 7 or 11 for initial win condition
      showInformation('You Win!')
    elif firstDiceRoll == 2 or firstDiceRoll == 3 or firstDiceRoll == 12:  #Compares initial dice roll to 2, 3 or 12 for initial lose condition
      showInformation('You Lose!')
    else:
      showInformation('Roll Again?')
      point = firstDiceRoll  #Establishes point for secondary win condition
      showInformation('The point is ' + str(point) + '.')
      continueRoll = True
      while continueRoll == True:  #Keeps game going until player wins or loses
        diceRoll = rollDice()
        showInformation('You rolled a ' + str(diceRoll) + '.')
        if diceRoll == point:  #Compares all subsequent dice rolls to point value for secondary win condition
          showInformation('You Win!')
          continueRoll = False
        elif diceRoll == 7:  #Compares all subsequent dice rolls to 7 for secondary lose condition
          showInformation('You Lose!')
          continueRoll = False
        else:
          showInformation('Roll Again!')

  #Opens a message dialogue to the user.  Welcomes the user to the hangman game and gives the user some basic instructions for playing.
  def welcome():
    showInformation("\n H A N G M A N \n \n Welcome to Hangman! You need to guess the word. \n Enter a letter.  You have 6 chances to get it correct. \n If you fill in all the letter spaces before that point, then you win! \n Good luck! \n")

  #Game to play hangman.
  def hangman():
    welcome()
    #Secret word or phrase is hard-coded.
    secretWord = "Examine Nautilus"
    secretWord = secretWord.lower()
    #Game only allows for letters to be entered.
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    guesses = " "
    #User has 6 turns to complete the game.  Guessing letters already guessed does not count against the number of turns left.
    turns = 6
    while turns > 0:
      missingLetters = 0
      output = ""
      for char in secretWord:
        if char == str(" "):
          output = str(output) + str("   ")
        elif char in guesses:  #Outputs correctly guessed letter.
          output = str(output) + str(char) + str(" ")
        else:  #Outputs '_' for letters not yet guessed.
          output = str(output) + str("_ ")
          missingLetters += 1
      showInformation(output)
      showInformation("Your Guesses: " + str(guesses))  #Prints all letters that have been guessed so far.
      if missingLetters == 0:
        showInformation("You Won!")  #Opens dialogue message to tell the user that they won the game.
        break
      print
      guess = (requestString("Enter a letter:"))  #Reguests user to enter a letter as a guess.
      guess = guess.lower()  #Forces guessed letter to lowercase.
      if guess in guesses:  #Handles if user guesses a letter previously guessed.
        showWarning("You already guessed '" + str(guess) + "' . Please guess again.")
      elif guess not in alphabet:  #Handles is user guesses character that is not a letter.
        showError("You must enter a letter!")
      elif len(guess) > 1:  #Handles if user tries to guess more than 2 characters at a time.
        showError("You can only enter one letter at a time!")
      elif guess not in secretWord:  #Handles when a wrong guess is made.
        turns -= 1
        showInformation("Wrong!")  #Opens dialogue message to tell the user that their guess is wrong.
        showInformation("You have " + str(turns) + " turns left.")   #Opens dialogue message to tell the user how many turns they have remaining.
        guesses += guess
        if turns == 0:
          showInformation("You Lose!")  #Opens dialogue message to tell the user that they have lost the game.
      else:
        guesses += guess

  def appleII():
    showInformation("Welcome to Apple II Games!")
    choice = requestInteger("1: Craps\n2: Hangman\nPick a game (1 or 2): ")
    if choice == 1:
      craps()
    elif choice == 2:
      hangman()
    else:
      pass

  ###Use Item Functions###
  def useComputer(self):
    if self.currentRoom.getName() == "Study":
      printNow("""You attempt to turn on the Macintosh computer, but unfortunately it will not turn on.  You look over at the Apple II and chuckle.
      You walk over and hit the power button.  To your surprise it boots up.""")
      play(makeSound('assets\\audio\\MacBoot.wav'))
      showInformation("This is where you play hangman and craps")
      appleII()
    else:
      showInformation("There is no computer in this room. Try visiting the Study")

  #step 1: make sure user has shovel
  #step 2: make sure user is in graveyard
  #step 3: if user has shovel and is in graveyard allow them to dig to retrieve key and Page Piece
  #step 4: break the shovel so the user cannot continue digging for more keys/Page Pieces
  def useShovel(self):
    if "Shovel" not in self.inventory:
      printNow("You do not have a shovel to use!")
      showInformation("You do not have a shovel to use!")
    elif self.currentRoom.getName() != "Graveyard":
      printNow("You can't use the shovel here. Try using it somewhere outside.")
      showInformation("You can't use the shovel here. Try using it somewhere outside.")
    elif self.currentRoom.getName() == "Graveyard" and "Shovel" in self.inventory:
      printNow("""The old shovel creaks under your weight as you plunge it deep into the cold earth.  You try one spot and then another.
      Finally on your third attempt you feel the shovel make contact with something hard.  Unfortunately, the handle cracks in half at
      the same time.  So much for that.  You get down on your knees and dig around with your hands where you felt the shovel strike something hard.
      In the wet dirt you feel something small and metal.  You pull it up into the light and discover it is a key.  You found a key and a torn scrap of paper!""")
      play(makeSound('assets\\audio\\shovel.wav'))
      sleep(3.5)
      play(makeSound('assets\\audio\\shovel.wav'))
      sleep(3.5)
      play(makeSound('assets\\audio\\shovelBreaking.wav'))
      showInformation("""The old shovel creaks under your weight as you plunge it deep into the cold earth.  You try one spot and then another.
Finally on your third attempt you feel the shovel make contact with something hard.  Unfortunately, the handle cracks in half at
the same time.  So much for that.  You get down on your knees and dig around with your hands where you felt the shovel strike something hard.
In the wet dirt you feel something small and metal.  You pull it up into the light and discover it is a key.  You found a torn scrap of paper!""")
      self.inventory.remove('Shovel')
      self.inventory.append('Broken Shovel')
      self.currentRoom.addItem('Key')
      self.currentRoom.addItem('Page Piece 1')
      printNow(self.currentRoom)
  #step 1: make sure user has the key in inventory
  #step 2: make sure user is on porch trying to get into mansion
  #unlock the door
  def useKey(self):
    if 'Key' not in self.inventory:
      printNow("You do not have a key!")
      showInformation("You do not have a key!")
    else:
      if self.currentRoom.getName() == "Porch":
        if self.currentRoom.getNorth().isLocked():
          self.currentRoom.getNorth().setLocked(false)
          self.inventory.remove('Key')
          printNow("You hear the sweet sound of the front door unlocking. The key gets stuck in the lock, though, and you leave it in there.")
          showInformation("You hear the sweet sound of the front door unlocking. The key gets stuck in the lock, though, and you leave it in there.")
          play(makeSound('assets\\audio\\doorCreaking.wav'))
        else:
           self.currentRoom.getNorth().setLocked(true)
           printNow("The lock clicks in place as the door is secured.")
           showInformation("The lock clicks in place as the door is secured.")
      else:
        printNow("You cannot use the key here!")
        showInformation("You cannot use the key here!")
  #step 1: Make sure user is holding the matches and lantern
  #step 2: if user has matches but not the lantern, tell user they don't have anything to use matches on
  #step 3: Else: user doesn't have matches to use
  def useMatches(self):
    if "Matches" in self.inventory and "Lantern" in self.inventory:
      printNow("You use the matches to light the lantern")
      play(makeSound('assets\\audio\\match.wav'))
      showInformation("You use the matches to light the lantern")
      self.inventory.remove("Matches")
      self.inventory.remove("Lantern")
      self.inventory.append("Lit Lantern")
      printNow(self.inventory)
    elif "Matches" in self.inventory and "Lantern" not in self.inventory:
      printNow("You do not have anything to use the matches on!")
      showInformation("You do not have anything to use the matches on!")
    else:
      printNow("You do not have any matches!")
      showInformation("You do not have any matches!")

  def useCouch(self):
    if self.currentRoom.getName() == "Living Room":
      printNow("Aaahhhh.  A well deserved break.  Well, time to get back to what you came here for.")
      showInformation("Aaahhhh.  A well deserved break.  Well, time to get back to what you came here for.")
    else:
      printNow("There is no couch in this room.  Try going to the living room.")
      showInformation("There is no couch in this room.  Try going to the living room.")

  def useTelevision(self):
    if self.currentRoom.getName() == "Living Room":
      printNow("Broken!  Oh well, you didn\'t come here to watch TV.")
      showInformation("Broken!  Oh well, you didn\'t come here to watch TV.")
    else:
      printNow("There is no television in this room.  Try going to the living room.")
      showInformation("There is no television in this room.  Try going to the living room.")

  def useSafe(self):
    if self.currentRoom.getName() == "Hidden Basement":
      code = requestString("Please enter the 7 digit code:")
      if code == "8675309":
        printNow("Success!  As you enter the last digit, you hear a click as the safe door pops open.")
        showInformation("Success!  As you enter the last digit, you hear a click as the safe door pops open.")
        self.safeLocked = false
      else:
        printNow("Nothing!  You must have the wrong code.")
        showInformation("Nothing!  You must have the wrong code.")
    else:
      printNow("There is no safe in here.")
      showInformation("There is no safe in here.")

  def useChair(self):
    if self.currentRoom.getName() == "Porch":
      play(makeSound('assets\\audio\\rockingChair.wav'))
      printNow("""Not too bad; pretty comfy in fact.  As you slowly rock back and forth you begin to understand a little more of the appeal of a slower lifestyle.
      Oh, well.  Enough sitting.  Time to get back to it.""")
      showInformation("""Not too bad; pretty comfy in fact.  As you slowly rock back and forth you begin to understand a little more of the appeal of a slower lifestyle.
      Oh, well.  Enough sitting.  Time to get back to it.""")
    elif self.currentRoom.getName() == "Library":
      printNow("Aahhh.  Now I just need a good book to read.  Which one to pick?")
      showInformation("Aahhh.  Now I just need a good book to read.  Which one to pick?")
    else:
      printNow("There is no chair in here.")
      showInformation("There is no chair in here.")

  def useWalkman(self):
    if "Walkman" in self.inventory:
      play(makeSound('assets\\audio\\readingRainbow.wav'))
      sleep(31)
      play(makeSound('assets\\audio\\rewindRainbow.wav'))
      sleep(7)
    else:
      printNow("You do not have a walkman in your inventory!")
      showInformation("You do not have a walkman in your inventory!")

  def drinkRedPotion(self):
    if "Red Potion" in self.inventory:
      self.hasDrunkRed = True
      play(makeSound('assets\\audio\\chug.wav'))
      if self.hasDrunkGreen:
          self.hasDrunkGreen = False
      self.inventory.remove('Red Potion')
      showInformation("You become irrationally enraged!")
    else:
      printNow("You are not carrying this item")
      showInformation("You are not carrying this item")

  def drinkGreenPotion(self):
    if "Green Potion" in self.inventory:
        self.hasDrunkGreen = True
        play(makeSound('assets\\audio\\chug.wav'))
        if self.hasDrunkRed:
            hasDrunkRed = False
        self.inventory.remove('Green Potion')
        showInformation("You become envious of everyone and everything!")
    else:
      printNow("You are not carrying this item")
      showInformation("You are not carrying this item")

  def examine(self, item):
    if item == "bookshelf" and self.currentRoom.getName() == "Library":
      printNow("You look closely at the bookshelf.  It is filled with many great novels.  You notice several of your favorites.  Doug had good taste in literature.")
      showInformation("You look closely at the bookshelf.  It is filled with many great novels.  You notice several of your favorites.  Doug had good taste in literature.")
    elif item == "nautilus" and self.currentRoom.getName() == "Library":
      printNow("""You realize that Doug has several Jules Verne novels.  You reach for \"20,000 Leagues Under the Sea\" from the shelf.
      As you attempt to pull the novel off the shelf the novel suddenly stops halfway out and one of the bookshelves pops open a few inches.
      A hidden door.  Brilliant!""")
      showInformation("""You realize that Doug has several Jules Verne novels.  You reach for \"20,000 Leagues Under the Sea\" from the shelf.
        As you attempt to pull the novel off the shelf the novel suddenly stops halfway out and one of the bookshelves pops open a few inches.
        A hidden door.  Brilliant!""")
      #Basement initially set to "It is too dark to see anything
      #User must first find matches and lantern then use matches to light lantern
      #With lit lantern equipped, description changes to reveal contents of basement
      basement = Room("Hidden Basement", "This room is too dark to see anything! Try to find something to help you see.", [],(958,138))
      self.currentRoom.setDown(basement)
      printNow(self.currentRoom)
      basement.setUp(self.currentRoom)
    elif item == 'tombstone' and self.currentRoom.getName() == "Graveyard":# and not self.secretRoomFound:
      printNow("""You examine the tombstone and read the name \"Douglas Adams\".  Underneath it says, \"Digital Killed the Analog Star!\" You notice that some crabgrass has grown up and blocked the bottom part of the tombstone.
You pull back the grass and notice several numbers printed in small font along the base.  It reads, \"100001000101111111101101\".""")
      showInformation("""You examine the tombstone and read the name \"Douglas Adams\".  Underneath it says, \"Digital Killed the Analog Star!\" You notice that some crabgrass has grown up and blocked the bottom part of the tombstone.
You pull back the grass and notice several numbers printed in small font along the base.  It reads, \"100001000101111111101101\".""")
    elif item == 'couch' and self.currentRoom.getName() == "Living Room":
      if self.couchDone == false:
        printNow("""You find some stale Cheez-Its and spare change in the couch cushions.  You take a look underneath and notice a small piece of parchment.
        It appears to be a torn scrap of paper.""")
        showInformation("""You find some stale Cheez-Its and spare change in the couch cushions.  You take a look underneath and notice a small piece of parchment.
        It appears to be a torn scrap of paper.""")
        #self.inventory.append("Page Piece 4")
        try:
            self.pickupItem('Page Piece 4')
        except:
            pass
        self.couchDone = true
        printNow(self.inventory)
      else:
        printNow("You already raided the couch!")
        showInformation("You already raided the couch!")
    elif item == 'television' and self.currentRoom.getName() == "Living Room":
      printNow("An old wood grained RCA.  A classic.  You look closer at the betamax tapes.  Hmm.  It looks like the old Adam West Batman series.")
      showInformation("An old wood grained RCA.  A classic.  You look closer at the betamax tapes.  Hmm.  It looks like the old Adam West Batman series.")
    elif item == "cabinets" and self.currentRoom.getName() == "Kitchen":
      printNow("""You root through the cabinets and find a small bottle that reads, Vision en Rouge.
      Sounds fancy.  Wonder how it tastes? You place the potion in your inventory.""")
      play(makeSound('assets\\audio\\checkCabinet.wav'))
      showInformation("""You root through the cabinets and find a small bottle that reads, Vision en Rouge.
Sounds fancy.  Wonder how it tastes? You place the potion in your inventory.""")
      self.inventory.append("Red Potion")
      printNow(self.inventory)
    elif item == "floor mat" and self.currentRoom.getName() == "Kitchen":
      if self.floorMatDone == false:
        printNow("You look under the floor mat and discover a torn scrap of paper!")
        showInformation("You look under the floor mat and discover a torn scrap of paper!")
        try:
            self.pickupItem('Page Piece 2')
        except:
            pass
        self.floorMatDone = true
        printNow(self.inventory)
      else:
        printNow("You already looked under the floor mat!")
        showInformation("You already looked under the floor mat!")
    elif item == 'portrait' and self.currentRoom.getName() == "Dining Room":
      if self.portraitDone == false:
        printNow("""The name underneath reads \"Wilfred Adams\".  You notice a small piece of paper sticking out from behind the back.
        You tug on it and you find yourself holding a torn scrap of paper.""")
        showInformation("""The name underneath reads \"Wilfred Adams\".  You notice a small piece of paper sticking out from behind the back.
        You tug on it and you find yourself holding a torn scrap of paper.""")
        #self.inventory.append("Page Piece 3")
        self.pickupItem('Page Piece 3')
        self.portraitDone = true
        printNow(self.inventory)
      else:
        printNow("You already examined the portrait!")
        showInformation("You already examined the portrait!")
    elif item == 'mirror' and self.currentRoom.getName() == "Dining Room":
      printNow("The mirror distorts your reflection. It looks almost like you're in the depths of the sea.")
      showInformation("The mirror distorts your reflection. It looks almost like you're in the depths of the sea.")
    elif item == 'furnace' and self.currentRoom.getName() == "Hidden Basement":
      printNow("This has not been lit in years.  Better not chance it.")
      showInformation("This has not been lit in years.  Better not chance it.")
    elif item == 'poster' and self.currentRoom.getName() == "Hidden Basement":
      printNow("""You look closely at the poster.  It looks genuine.  You notice one corner is not completely held down.
      You give a gentle tug and notice there is something behind the poster.  You pull a little harder, careful not to damage the poster.
      You pull the poster completely off the wall to reveal a safe hidden behind it.  You are close.  You can feel it.""")
      showInformation("You look closely at the poster.  It looks genuine.  You notice one corner is not completely held down. You give a gentle tug and notice there is something behind the poster.  You pull a little harder, careful not to damage the poster.  You pull the poster completely off the wall to reveal a safe hidden behind it.  You are close.  You can feel it.")
      self.currentRoom.addItem('safe')
    elif item == 'safe' and self.currentRoom.getName() == "Hidden Basement" and self.safeLocked:
      printNow("The safe is locked.")
      showInformation("The safe is locked.")
    elif item == 'safe' and self.currentRoom.getName() == "Hidden Basement" and not self.safeLocked:
      printNow("""You open the safe to reveal its contents.  You pull out a 1978 comic book, "Batman versus Muhammad Ali".  It appears the comic book has been autographed.
      You place the comic book in your backpack.""")
      showInformation("You open the safe to reveal its contents.  You pull out a 1978 comic book, \"Batman versus Muhammad Ali\".  It appears the comic book has been autographed. You place the comic book in your backpack.")
      self.inventory.append("Comic Book")
      printNow(self.inventory)
    elif item == 'comic book' and "Comic Book" in self.inventory:
      printNow("""You look closely at the comic book to read the inscription.
      ?To my dear son, Douglas.  Whether you grow up to be Batman or Bruce, I\'ll always be proud of you.  I love you.  Dad.?
      You notice that the cover art to the comic book was by Neal Adams.
      Neal Adams was Douglas Adams father!  Amazing!
      But that still doesn\'t solve the mystery.
      Where is Doug?
      ********************
      Batman or Bruce?
      Batman or Bruce?
      OMG!  I had the answer right in front of me from the very beginning.
      I need to get back to town right away.""")
      showInformation("""You look closely at the comic book to read the inscription.
To my dear son, Douglas.  Whether you grow up to be Batman or Bruce, I\'ll always be proud of you.  I love you.  Dad.?
You notice that the cover art to the comic book was by Neal Adams.
Neal Adams was Douglas Adams father!  Amazing!
But that still doesn\'t solve the mystery.
Where is Doug?
********************
Batman or Bruce?
Batman or Bruce?
OMG!  I had the answer right in front of me from the very beginning.
I need to get back to town right away.""")
    elif item == 'walkman' and 'Walkman' in self.inventory:
      printNow("Wow! Talk about old school.  It looks like it has a mix tape in it.  Wonder if it works?")
      showInformation("Wow! Talk about old school.  It looks like it has a mix tape in it.  Wonder if it works?")
    else:
      printNow("You can't do that!")
      showInformation("You can't do that!")

  def talkToBoy(self):
    printNow("""
    Hey!  How goes it?
    It goes fine.  <eyes you skeptically>  Where you from cause it ain\'t from around here?
    How do you know I\'m not from around here?
    First off, e\'ryone knows e\'ryone \'round here.
    Second, you talks funny.
    I talks funny?
    Anyway, I\'m in town visiting my grandparent\'s for a few weeks.  I just came from the diner and was look for something to do.  I heard this is where the young folks hang out.
    Well, that\'s true.  Unfortunately, I\'m the only young folk around these here parts.  Name\'s Opie.
    <under your breath>  Figures.
    Do you know where I could find Bruce then?
    Bruce?  Whatcha want with Bruce?  You need something fixed?  Bruce can fix anything.
    He\'s a mechanical genius.  Cars.  TVs.  Radios.  You name it.
    No, nothing like that.  I wanted to ask him about the Mystery at the Mansion.
    <boy goes pale>
    Whatcha wanna go and do that for?  That place is haunted.
    It\'s the old Adams mansion.  The oldest place in all of Plainsfield.
    It was passed down from Adams to Adams for centuries.  The last known descendant was Douglas Adams.  He was a fancy media engineer.  Worked with film and audio like they do in Hollywood and stuff.
    Story goes that Douglas Adams went mad crazy after e\'rythang started going from analog to digital.  Couldn\'t take it no more.
    <silence>
    And then what?
    And then nothing.  Ol\' Doug just up and disappeared.  Place has been abandoned ever since.  Although if you ask me, he ne\'er left.  He haunts that place to this day.
    How does someone just disappear in a town this size?  No one has ever seen him since.
    Well, that\'s kind of the problem too.  No one really knows what Doug looks like.  He was pretty much a recluse when he did live in that there mansion.
    Can you tell me where the mansion is located?
    I don\'t know for sure.  Bruce does though.  He is at the gas station just a little ways from here.
    Okay, thanks.""")

    showInformation("""
Hey!  How goes it?
It goes fine.  <eyes you skeptically>
Where you from cause it ain\'t from around here?
How do you know I\'m not from around here?
First off, e\'ryone knows e\'ryone \'round here.
Second, you talks funny.
I talks funny?
Anyway, I\'m in town visiting my grandparent\'s for a few weeks.
I just came from the diner and was look for something to do.  I heard this is where the young folks hang out.
Well, that\'s true.  Unfortunately, I\'m the only young folk around these here parts.  Name\'s Opie.
<under your breath>  Figures.
Do you know where I could find Bruce then?
Bruce?  Whatcha want with Bruce?  You need something fixed?  Bruce can fix anything.
He\'s a mechanical genius.  Cars.  TVs.  Radios.  You name it.
No, nothing like that.  I wanted to ask him about the Mystery at the Mansion.
<boy goes pale>
Whatcha wanna go and do that for?  That place is haunted.
It\'s the old Adams mansion.  The oldest place in all of Plainsfield.
It was passed down from Adams to Adams for centuries.  The last known descendant was Douglas Adams.  He was a fancy media engineer.  Worked with film and audio like they do in Hollywood and stuff.
Story goes that Douglas Adams went mad crazy after e\'rythang started going from analog to digital.  Couldn\'t take it no more.
<silence>
And then what?
And then nothing.  Ol\' Doug just up and disappeared.  Place has been abandoned ever since.  Although if you ask me, he ne\'er left.  He haunts that place to this day.
How does someone just disappear in a town this size?  No one has ever seen him since.
Well, that\'s kind of the problem too.  No one really knows what Doug looks like.  He was pretty much a recluse when he did live in that there mansion.
Can you tell me where the mansion is located?
I don\'t know for sure.  Bruce does though.  He is at the gas station just a little ways from here.
Okay, thanks.""")

  def talkToEdith(self):
    printNow("""
    \'Hey Edith.
    <cough, cough> <raspy voice>  Hey!  You\'re not from around here.
    I\'m new in town; visiting my grandparents.  I just wondered what there is to do around here?\'
    You\'re doing it.  Other than hanging out at the diner, you could wander over to the church.  There is a rec room there where some of the local young folks like to hang out.\'
    You could also go find Bruce and talk to him.  He is always working on some contraption or willing to tell some tall tale.  His favorite is the mystery of the mansion.
    Mystery of the Mansion?
    Just a bunch of nonsense if you ask me.
    \'Okay thanks.\'
    Hmmm.  Mystery of the Mansion?  There might be something exciting in this town after all.
    I wonder where this Bruce guy is?  Oh well, I guess I\'ll go check out this church in the meantime.""")
    showInformation("""
Hey Edith.
<cough, cough> <raspy voice>  Hey!  You\'re not from around here.
I\'m new in town; visiting my grandparents.  I just wondered what there is to do around here?\'
You\'re doing it.  Other than hanging out at the diner, you could wander over to the church.  There is a rec room there where some of the local young folks like to hang out.\'
You could also go find Bruce and talk to him.  He is always working on some contraption or willing to tell some tall tale. His favorite is the mystery of the mansion.
Mystery of the Mansion?
Just a bunch of nonsense if you ask me.
\'Okay thanks.\'
Hmmm.  Mystery of the Mansion?  There might be something exciting in this town after all. I wonder where this Bruce guy is? Oh well, I guess I\'ll go check out this church in the meantime.""")

  def talkToBruce(self):
    if "Comic Book" in self.inventory:
      printNow("""
          Hi Bruce!
          Hi.  Back from your trip to the mansion?  Find anything interesting?
          A whole lot in fact.  I have something for you.
          <gives Bruce the comic book>
          <long pause>
          I gotta give you credit.  I never thought anyone would ever figure it out.  How\'d you figure it out?
          It was the message your dad wrote.  He told you could be either Bruce or Batman.
          And I obviously chose to be Bruce.
          No!  You chose to be Batman.  You gave up the mansion and wealth so that you could silently help the folks here in Plainsfield.  You fix things in the night and keep things running with hardly any recognition for it.
          You are Batman.  You took the name Bruce to hide the fact that you are really Douglas Adams.
          Well, let me congratulate you again.  You really have solved the Mystery of the Adam\'s Mansion.  Well, I guess the jig\'s up for me.  Time to be Douglas Adams again.
          No it\'s not.  You should always be yourself, unless you can be Batman, then be Batman.
          You chose to be Batman, and I\'m the last person who will ever turn Bruce Wayne in as being Batman.  Your secret\'s safe with me.
          You\'re all right.  Hey, I never did catch your name.
          <grins>
          Just call me Robin.""")
      showInformation("""
        Hi Bruce!
        Hi.  Back from your trip to the mansion?  Find anything interesting?
        A whole lot in fact.  I have something for you.
        <gives Bruce the comic book>
        <long pause>
        I gotta give you credit.  I never thought anyone would ever figure it out.  How\'d you figure it out?
        It was the message your dad wrote.  He told you could be either Bruce or Batman.
        And I obviously chose to be Bruce.
        No!  You chose to be Batman.  You gave up the mansion and wealth so that you could silently help the folks here in Plainsfield.  You fix things in the night and keep things running with hardly any recognition for it.
        You are Batman.  You took the name Bruce to hide the fact that you are really Douglas Adams.
        Well, let me congratulate you again.  You really have solved the Mystery of the Adam\'s Mansion.  Well, I guess the jig\'s up for me.  Time to be Douglas Adams again.
        No it\'s not.  You should always be yourself, unless you can be Batman, then be Batman.
        You chose to be Batman, and I\'m the last person who will ever turn Bruce Wayne in as being Batman.  Your secret\'s safe with me.
        You\'re all right.  Hey, I never did catch your name.
        <grins>
        Just call me Robin.""")
      showInformation('You are Batman. You win!')
      return 'lost'
    else:
        printNow("""
        You walk over closer to the man in the faded overalls.  You notice he appears to be working on an old Atari 2600.  Hmm, interesting.
        Hi, are you Bruce.
        Who\'s asking?
        I am.  I was hoping you could help me out?
        Maybe.  You\'re not from \'round here.
        That\'s what I\'m told.  I was interested in the Adams mansion.
        Adams mansion?  Sounds like you\'ve been talking to Opie.
        Why\'s that?
        That boy\'s always spinning tales about that mansion up on the hill.  Thinks it\'s haunted.
        <chuckles>
        You don\'t?
        The mansion was abandoned years ago.  Plain and simple.  Everyone wants to say its haunted or that there is some sort of great mystery to it.
        But not you?
        What\'s the mystery?  Doug took off one day and the mansion has been abandoned ever since.
        But no one saw him leave?  And he left everything behind, including the car.  How does someone leave this town without a car and without anyone seeing them?
        <grunts>
        Now you sound like Opie too.  That boy\'s always looking for a mystery to solve.
        Can you tell me where to find the mansion?
        Sure, its located over there yonder on that hill.  Be careful snooping around there though.
        If the guy\'s really gone, what\'s the harm?
        Just be careful.  Some things are best left alone if you ask me.""")
        showInformation("""
        You walk over closer to the man in the faded overalls.  You notice he appears to be working on an old Atari 2600.  Hmm, interesting.
        Hi, are you Bruce.
        Who\'s asking?
        I am.  I was hoping you could help me out?
        Maybe.  You\'re not from \'round here.
        That\'s what I\'m told.  I was interested in the Adams mansion.
        Adams mansion?  Sounds like you\'ve been talking to Opie.
        Why\'s that?
        That boy\'s always spinning tales about that mansion up on the hill.  Thinks it\'s haunted.
        <chuckles>
        You don\'t?
        The mansion was abandoned years ago.  Plain and simple.  Everyone wants to say its haunted or that there is some sort of great mystery to it.
        But not you?
        What\'s the mystery?  Doug took off one day and the mansion has been abandoned ever since.
        But no one saw him leave?  And he left everything behind, including the car.  How does someone leave this town without a car and without anyone seeing them?
        <grunts>
        Now you sound like Opie too.  That boy\'s always looking for a mystery to solve.
        Can you tell me where to find the mansion?
        Sure, its located over there yonder on that hill.  Be careful snooping around there though.
        If the guy\'s really gone, what\'s the harm?
        Just be careful.  Some things are best left alone if you ask me.""")

  #Returns current room of player
  def getCurrentRoom(self):
    return self.currentRoom

  def __str__(self):
    return ("Name: %s\nCurrent Location: %s\nPlayer Inventory: %s\n")%(self.name, self.currentRoom, self.inventory)

  def create_hud(self,mustRemake = False):
    ########################################
    """
        This is where we create the hud.

        JES's image processing and memory
        management is God-awful inefficient
        so we prefabricated the HUD images
        and load them as needed.
    """
    ########################################
    if mustRemake:
      self.currentRoom.make_huds() #Reload HUDS from folder

    if self.hasDrunkRed: #Handle red potion
        self.currentRoom.add_hud_description(str(self.currentRoom),'red')
        if not (self.currentRoom.coords[0] == 0 and self.currentRoom.coords[0] == 0):
            addOvalFilled(self.currentRoom.get_hud('red'),self.currentRoom.coords[0],self.currentRoom.coords[1],25,25,green)
        if len(self.inventory) > 0:#Print the items in player inventory
            for i in range(len(self.inventory)):
                self.add_hud_item(self.currentRoom.get_hud('red'),i,self.inventory[i])
        return self.currentRoom.get_hud('red')
    elif self.hasDrunkGreen: #Handle green potion
        self.currentRoom.add_hud_description(str(self.currentRoom),'green')
        if not (self.currentRoom.coords[0] == 0 and self.currentRoom.coords[0] == 0):
            addOvalFilled(self.currentRoom.get_hud('green'),self.currentRoom.coords[0],self.currentRoom.coords[1],25,25,green)
        if len(self.inventory) > 0:#Print the items in player inventory
            for i in range(len(self.inventory)):
                self.add_hud_item(self.currentRoom.get_hud('green'),i,self.inventory[i])
        return self.currentRoom.get_hud('green')
    else: #Add room description and then put player map pin
        self.currentRoom.add_hud_description(str(self.currentRoom),'normal')
        if not (self.currentRoom.coords[0] == 0 and self.currentRoom.coords[0] == 0):
            addOvalFilled(self.currentRoom.get_hud('normal'),self.currentRoom.coords[0],self.currentRoom.coords[1],25,25,green)
        if len(self.inventory) > 0:#Print the items in player inventory
            for i in range(len(self.inventory)):
                self.add_hud_item(self.currentRoom.get_hud('normal'),i,self.inventory[i])
        return self.currentRoom.get_hud('normal')

  def add_hud_item(self,hud,index,item):
      """
      This function adds an inventory item to the HUD in one of
      six inventory slots detailed below.

      Inventory Items:
          |1|2|3|
          |4|5|6|
          1: width (x): 903-1028; height (y): 602-726 [125x124]
          2: width (x): 1062-1187; height (y): 602-726 [125x124]
          3: width (x): 1220-1345; height (y): 602-726 [125x124]
          4: width (x): 903-1028; height (y): 740-864 [125x124]
          5: width (x): 1062-1187; height (y): 740-864 [125x124]
          6: width (x): 1220-1345; height (y): 740-864 [125x124]
      """
      i_path = {
        'Red Potion': 'assets\\images\\item_icons\\potion_red.jpg',
        'Green Potion': 'assets\\images\\item_icons\\Green-Potion.jpg',
        'Page Piece 1': 'assets\\images\\item_icons\\map_piece_1.jpg',
        'Page Piece 2': 'assets\\images\\item_icons\\map_piece_2.jpg',
        'Page Piece 3': 'assets\\images\\item_icons\\map_piece_3.jpg',
        'Page Piece 4': 'assets\\images\\item_icons\\map_piece_4.jpg',
        'Key': 'assets\\images\\item_icons\\key.jpg',
        'Small Key': 'assets\\images\\item_icons\\small_key.jpg',
        'Shovel': 'assets\\images\\item_icons\\shovel.jpg',
        'Broken Shovel': 'assets\\images\\item_icons\\broken_shovel.jpg',
        'Tape': 'assets\\images\\item_icons\\Tape.jpg',
        'Lantern': 'assets\\images\\item_icons\\Lantern.jpg',
        'Matches': 'assets\\images\\item_icons\\Matches.jpg',
        'Lit Lantern': 'assets\\images\\item_icons\\lit_lantern.jpg',
        'Walkman': 'assets\\images\\item_icons\\Walkman.jpg',
        'Comic Book': 'assets\\images\\item_icons\\ComicBook.jpg',
          }
      origins = [(903,602),(1062,602),(1220,602),(903,740),(1062,740),(1220,740)]
      pyCopyEx(makePicture(i_path[item]),hud,origins[index][0],origins[index][1],getColor(getPixel(makePicture(i_path[item]),0,0)))

#Mystery Mansion prologue
def story_prologue():
  prologue = """
  SEA BEACH, CA

  'CORN!'
  'All there is for miles is corn!'

  'Don't be ridiculous,' replied your mother.  'I am sure there is more than corn where you are headed.'

  'I did a Google street view and do you know what it showed?'

  'Corn?' your father tentatively chimed in.

  'No!  It showed nothing, because even Google won't visit there.
  But if they had, it would have been just miles and miles of corn.'

  'There won't be many more opportunities to visit your grandparents in Indiana.
  You're going and that's that,' retorted your mother.

  'Fine!  I'll be in the car.'

  'Bring me back a souvenir!' shouted your father as you walked out.

  'I hope you like corn!'
  """
  showInformation(prologue)

#Mystery Mansion intro
def story_intro():
  intro = """
  PLAINSFIELD, IN

  Plainsfield, Indiana was about as boring of a place as you could imagine.

  The town has a population of 480.  There was one gas station
  and surprise, surprise, miles and miles of corn.  A month was gonna be a long time
  to kill in a town without wifi.  Your grandparents had told you to get out and explore,
  but explore where?  Oh well, being outside was better than being stuck inside all day.

  There weren't many places to explore in Plainsfield.  You spotted a local diner,
  on your way in.  Guess you could figure out what there is to eat around here.
  """
  showInformation(intro)

def mysteryMansion():
  global isPathSet
  if not isPathSet:
      showInformation("Welcome to Mystery Mansion! At any time you may quit the game by typing exit or quit. As you explore Plainsfield you will have several options for interacting with your environment. Commands include: print, pickup, drop, move, use, drink, examine, and talk to. If you are stuck, the help command will print out detailed command information. Thanks for playing!")
      showInformation("Please Choose the game folder.")
      setMediaFolder()
      isPathSet = True
  #Is game over?
  done = false

  #Flavor to set up the backdrop for the game
  story_prologue()
  story_intro()

  #Description of living room
  livingRoomDescription = """The living room is one of the largest rooms in the old mansion.  The interior is dark as most of the curtains and shades are drawn.
  In the middle is a \'couch\' with two end tables on each side.  One end table has a lamp on it, while the other has a lantern.  To the left is a large overstuffed arm chair.
  There is a coffee table in front of the couch and an old wood grained RCA \'television\' sitting on the floor in front of the coffee table.  On top of the television was a betamax player
  and several betamax tapes.  Framed pictures decorate the walls on every side."""
  #Description of kitchen
  kitchenDescription = """The kitchen was surprisingly one of the cleaner rooms in the mansion.  I guess the owner was not much of a cook?  The interior was vintage 70s.  Wood \'cabinets\' with old ivory pull knobs.
  There was an oven, range top stove, and refrigerator...all avocado green.  The sink still has a few glasses in it, but nothing else seemed to be out of place.
  The floor was linoleum and there was an old \'floor mat\' in front of the kitchen sink.  The dirtiest thing in the whole room was an old microwave sitting on the counter.
  This was obviously the owner\'s appliance of choice, lol.  By the far wall under the window was a small table with a single solitary chair.  Guess he didn\'t entertain too many guests?"""
  #Description of Porch
  porchDescription = """The porch is big and expansive as was the style in the midwest.  The floor boards and rails are showing their age.  The whole thing is in desperate need of being refinished.
  On the left side of the porch is an old rocking \'chair\' with a small table next to it.  On the table is an ashtray and a coaster.  To the right of the rocking chair is the front door of the mansion painted a bright red color.
  Beneath the door is a mat that says \"Welcome\"."""
  #Description of Graveyard
  graveyardDescription = """The graveyard is small and sits on a hill adjacent to the mansion.  The \'tombstone\'s are laid out in a haphazard manner.  It appears to be a family cemetery for the Adam\'s family.
  Some of the dates go back to the 1700s.   The cemetery suffers from obvious years of neglect as many of the headstones are in disrepair and the weeds and ivy are overgrown.
  In the middle of the graveyard is an old oak tree that stretches far above the entire cemetery."""
  #Description of Shed
  shedDescription = """The shed is an old dilapidated shed halfway between the graveyard and the mansion.  It appears it was probably used to store tools and such, although it could contain anything.
  The shed has a small padlock on the outside."""
  #Description of Library
  libraryDescription = """You are immediately confronted with the smell of musty books.  The library contains a \'bookshelf\' for every wall.  Each shelf is stuffed with books of every shape and size.
  In the middle of the library is an old leather arm \'chair\' and an end table.  On the end table you notice a walkman."""
  #Description of Study
  studyDescription = """The study was the messiest of all the rooms.  There was a desk in the middle with an old Macintosh \'computer\'.  Papers were piled up in an organization that could only be guessed at.
  In the right corner was a smaller desk with an old Apple II computer on it.  In the left corner was a grandfather clock that appeared to still be keeping time."""
  #Description of Dining Room
  diningRoomDescription = """The dining room is very ornate.  In the center is a large dining table with candles.  The table has place settings for 12 people although it appears that it was rarely used.
  Towards the back of the room is a large \'mirror\' that stretches from floor to ceiling.  Above the dining table was a large glass chandelier.  Opposite the mirror is a large \'portrait\' of a man."""
  #Description of Gas Station
  gasStationDescription = """You arrive at the gas station.  The main building is made of wood.  There is a window to the left that has been broken.  Outside the gas station on the deck is a simple wooden chair and a small wooden table.
  Above the gas station is a faded metal Texaco sign.  Next to that is a sign that reads: Route 66 Cafe.  On the right side of the porch deck is a vintage Coca-Cola vending machine.
  You spy an old man rustling around the mechanics bay to the right side of the station."""
  #Description of Diner
  dinerDescription = """You arrive at the diner.  It\'s the typical Hollywood portrayal of a rundown midwest diner.  The building itself is a large rectangular piece with metal siding.  Weeds are overgrown all along the outside.
  A large sign stands above the building with giant letters spelling out D-I-N-E-R.  You wonder if the place is even in business.  Oh, well.  Only one way to find out.  You head inside.
  The appearance inside the diner is only slightly more upkept than the outside.  The plastic material on the booths and barstools is cracked.  The paint on the walls is faded and peeling in places.
  Behind the counter is an older woman with Edith on her nametag.  You approach the counter."""
  #Description of church
  churchDescription = """The local church is a small brightly painted red chapel with a large steeple with a bell in it.  It is obvious the locals care about this building as it seems to be the best upkept building in the whole town.
  You look around to see if there is anyone to talk to or anything to do.  You spy a young boy sitting near the steps of the church."""
  #Create all the rooms in the mansion
  kitchen = Room("Kitchen",kitchenDescription,[],(1143,162))
  porch = Room("Porch", porchDescription, [],(1130,338))
  graveyard = Room("Graveyard", graveyardDescription, [],(1324,256))
  shed = Room("Shed", shedDescription, ["Shovel"],(1321,191))
  library = Room("Library", libraryDescription, ["Walkman"],(1042,166))
  study = Room("Study", studyDescription, ["Matches", "Tape"],(1034,283))
  livingRoom = Room("Living Room", livingRoomDescription, ["Lantern"],(1132,294))
  ###Lock front door of living room###
  livingRoom.setLocked(true)
  diningRoom = Room("Dining Room", diningRoomDescription, [],(1224,295))
  church = Room("Church", churchDescription, [],(0,0))
  gasStation = Room("Gas Station", gasStationDescription, [],(0,0))
  diner = Room("Diner", dinerDescription, [],(0,0))


  ###Build the mansion/room relationships###
  porch.setNorth(livingRoom)
  porch.setEast(graveyard)
  graveyard.setWest(porch)
  graveyard.setNorth(shed)
  shed.setSouth(graveyard)
  livingRoom.setSouth(porch)
  livingRoom.setWest(study)
  livingRoom.setNorth(library)
  livingRoom.setEast(diningRoom)
  diningRoom.setWest(livingRoom)
  study.setEast(livingRoom)
  library.setSouth(livingRoom)
  library.setEast(kitchen)
  #library.setDown(basement)
  kitchen.setWest(library)
  diner.setNorth(church)
  church.setSouth(diner)
  church.setEast(gasStation)
  gasStation.setWest(church)
  gasStation.setEast(porch)
  porch.setWest(gasStation)

  ##get character name##
  playerName = requestString("Please enter your character's name:")
  #create player object
  player = Player(playerName, diner)
  #Print player details
  printNow(player)
  show(player.create_hud())
  #All the possible actions a user may enter and the corresponding function to call
  actions = {
    ###Print Functions###
    'print room': 'printNow(player.getCurrentRoom())',
    'print inventory': 'printNow(player.inventory)',
    'print player': 'printNow(player)',
    ###Pickup Functions###
    'pickup red potion': "player.pickupItem('Red Potion')",
    'pickup green potion': "player.pickupItem('Green Potion')",
    'pickup page piece 1': "player.pickupItem('Page Piece 1')",
    'pickup page piece 2': "player.pickupItem('Page Piece 2')",
    'pickup page piece 3': "player.pickupItem('Page Piece 3')",
    'pickup page piece 4': "player.pickupItem('Page Piece 4')",
    'pickup key': "player.pickupItem('Key')",
    'pickup shovel': "player.pickupItem('Shovel')",
    'pickup tape': "player.pickupItem('Tape')",
    'pickup lantern': "player.pickupItem('Lantern')",
    'pickup matches': "player.pickupItem('Matches')",
    'pickup lit lantern': "player.pickupItem('Lit Lantern')",
    'pickup walkman': "player.pickupItem('Walkman')",
    ###Drop Functions###
    'drop red potion': "player.dropItem('Red Potion')",
    'drop green potion': "player.dropItem('Green Potion')",
    'drop key': "player.dropItem('Key')",
    'drop shovel': "player.dropItem('Shovel')",
    'drop tape': "player.dropItem('Tape')",
    'drop lantern': "player.dropItem('Lantern')",
    'drop matches': "player.dropItem('Matches')",
    'drop broken shovel': "player.dropItem('Broken Shovel')",
    'drop lit lantern': "player.dropItem('Lit Lantern')",
    'drop walkman': "player.dropItem('Walkman')",
    ###Move Functions###
    'move north': 'player.movePlayerNorth()',
    'move south': 'player.movePlayerSouth()',
    'move east': 'player.movePlayerEast()',
    'move west': 'player.movePlayerWest()',
    'move up': 'player.movePlayerUp()',
    'move down': 'player.movePlayerDown()',
    ###Use Functions###
    'use computer': 'player.useComputer()',
    'use shovel': 'player.useShovel()',
    'use key': 'player.useKey()',
    'use matches': 'player.useMatches()',
    'use lantern': 'player.useLantern()',
    'use television': 'player.useTelevision()',
    'use couch': 'player.useCouch()',
    'use safe': 'player.useSafe()',
    'use chair': 'player.useChair()',
    'use walkman': 'player.useWalkman()',
    #Drink Function###
    'drink red potion': "player.drinkRedPotion()",
    'drink green potion': "player.drinkGreenPotion()",
    #Examine Functions###
    'examine bookshelf': "player.examine('bookshelf')",
    'examine nautilus': "player.examine('nautilus')",
    'examine tombstone': "player.examine('tombstone')",
    'examine couch': "player.examine('couch')",
    'examine television': "player.examine('television')",
    'examine cabinets': "player.examine('cabinets')",
    'examine floor mat': "player.examine('floor mat')",
    'examine portrait': "player.examine('portrait')",
    'examine mirror': "player.examine('mirror')",
    'examine furnace': "player.examine('furnace')",
    'examine poster': "player.examine('poster')",
    'examine safe': "player.examine('safe')",
    'examine comic book': "player.examine('comic book')",
    'examine walkman': "player.examine('walkman')",
    #Talk to Functions#
    'talk to edith': "player.talkToEdith()",
    'talk to bruce': "player.talkToBruce()",
    'talk to boy': "player.talkToBoy()",
  }

  #Continue requesting next move until game ends, or user types exit/quit
  while not done:
    #get next action from user
    action = requestString("Please enter next move").lower()
    #Get help screen
    if action == "help":
      showInformation("""List of commands:
        Print - prints your name, inventory, or current room.
        Pickup - picks up items you find in rooms.
        Drop - drops items from your inventory.
        Move - moves to the next room. Directions are given in North, South, East, and West.
        Use - most inventory items and some objects and furniture in a room can be used.
        Drink - drinks any delicious beverages you might find.
        Examine - many of the items in a room's description can be examined.
        Talk to - talk to the denizens of Plainsfield.
        Quit/Exit - ends the game
        Objects you are able to interact with can be identified by the \' \' around it.""")
    #End game if user types 'exit' or 'quit'
    elif action == "exit" or action == "quit":
      done = true
      break
    #Attempt to evaluate the action entered by user.
    else:
      try:
        result = eval(actions[action])
        if result == 'lost':
            done = True
        elif 'pickup' in actions[action] or 'drop' in actions[action] or 'use' in action or 'drink' in action:
            show(player.create_hud(True))
        else:
            if not player.currentRoom.isPainted:
                show(player.create_hud(False))
                player.currentRoom.isPainted = True
            else:
                repaint(player.create_hud(False))

      #Handles error from an invalid action
      except:
        printNow("Not a valid move")
        showInformation("Not a valid move")


#################Working on Images################

def img_scramble(pic,scramble_level):
  pix = getPixels(pic)
  scramble_level = int(scramble_level)
  original = pix[:]
  indices = range(len(pix))
  random.shuffle(indices)
  if scramble_level == 1:
      return 0
  for i in range(len(indices)):
    if scramble_level == 0: #full scramble
        setColor(pix[indices[i]],getColor(original[i]))
    elif random.randint(1,scramble_level) != 1:
      setColor(pix[indices[i]],getColor(original[i]))

def pyCopyEx(pic,target, targetX, targetY,exclude = None):
    for x in range (0, getWidth(pic)):
        for y in range (0, getHeight(pic)):
            if x+targetX < getWidth(target) and y+targetY < getHeight(target):
                src_color = getColor(getPixel(pic, x, y))
                if exclude == None:
                    setColor(getPixel(target, x+targetX, y+targetY), src_color)
                    #1:1 copy. Just need to set mypic's pixel to the color of pic's pixel,
                    #only with an offset for x of targetX and y of targetY. Excluding
                    #pixels of a preselected color.
                elif distance(src_color,exclude) > 90:
                    setColor(getPixel(target, x+targetX, y+targetY), src_color)
                    #1:1 copy. Just need to set mypic's pixel to the color of pic's pixel,
                    #only with an offset for x of targetX and y of targetY. Excluding
                    #pixels of a preselected color.
    return target

def find_last_space(txt):
    try:
        return txt.rindex(' ')
    except:
        return 0

def txt_to_lines(txt,font_size,isLong = False):
    """This function takes a blob of txt
    and tries to format it into lines that
    will fit on the HUD"""
    ret = []
    isEoF = False
    index = 0
    while not isEoF:
        if isLong:
            max_index = index+int(6.75*font_size)#empirically derived constant
        else:
            max_index = index+int(2.75*font_size)#empirically derived constant
        if max_index < len(txt):
            end_index = index + find_last_space(txt[index:max_index])
            ret.append(txt[index:end_index])
            index = end_index
        else:
            ret.append(txt[index:len(txt)])
            isEoF = True

    return ret


##################Functions left over from development#################
def green_tint(p):#red tinting map function
    color = getColor(p)
    setColor(p,makeColor(color.getRed(),min(255,int(color.getGreen()*2)),color.getBlue()))
def red_tint(p):#green tinting map function
    color = getColor(p)
    setColor(p,makeColor(min(255,int(color.getRed()*2)),color.getGreen(),color.getBlue()))

def make_screens():

    """This is the function I used to make the HUDs with their specific images"""

    setMediaFolder('C:\\Users\\callen\\Google Drive\\CSUMB\\final_project\\assets\\images\\')

    rooms = {
        'Church': 'Church.jpg',
        'Diner': 'Diner.jpg',
        'Gas Station': 'GasStation.jpg',
        'Porch': 'Porch.jpg',
        'Kitchen': 'Kitchen.jpg',
        'Porch': 'Porch.jpg',
        'Shed': 'Shed.jpg',
        'Study': 'Study.jpg',
        'Dining Room': 'DiningRoom.jpg',
        #'Graveyard': 'Graveyard.jpg',
        #'Graveyard Green': 'greenGraveyard.jpg',
        #'Graveyard Red': 'redGraveyard.jpg',
        #'Living Room': 'LivingRoom.jpg',
        #'Living Room Green': 'greenLivingRoom.jpg',
        #'Living Room_Red': 'redLivingRoom.jpg',
        #'Library': 'Library.jpg',
        #'Library Green': 'greenLibrary.jpg',
        #'Library Red': 'redLibrary.jpg',
    }

    for key in rooms:
        pic_reg = makePicture(rooms[key])
        pic_grn = makePicture(rooms[key])
        pic_red = makePicture(rooms[key])
        pix_grn = getPixels(pic_grn)
        pix_red = getPixels(pic_red)
        map(green_tint,pix_grn)
        map(red_tint,pix_red)
        hud_reg = makePicture('huds\\hud.jpg')
        hud_grn = makePicture('huds\\hud.jpg')
        hud_red = makePicture('huds\\hud.jpg')
        pyCopyEx(pic_reg,hud_reg,26,100)
        pyCopyEx(pic_grn,hud_grn,26,100)
        pyCopyEx(pic_red,hud_red,26,100)
        writePictureTo(hud_reg,'huds\\%s HUD.jpg'%key)
        writePictureTo(hud_red,'huds\\%s Red HUD.jpg'%key)
        writePictureTo(hud_grn,'huds\\%s Green HUD.jpg'%key)

def add_screen_maps():
    """This is the function I used to add the maps to the
    HUD images"""

    town_files = ['Church Green HUD.jpg',
    'Church HUD.jpg',
    'Church Red HUD.jpg',
    'Diner Green HUD.jpg',
    'Diner HUD.jpg',
    'Diner Red HUD.jpg',
    'Gas Station Green HUD.jpg',
    'Gas Station HUD.jpg',
    'Gas Station Red HUD.jpg',]

    mansion_files = ['Graveyard Green HUD.jpg',
    'Graveyard HUD.jpg',
    'Graveyard Red HUD.jpg',
    'Kitchen Green HUD.jpg',
    'Kitchen HUD.jpg',
    'Kitchen Red HUD.jpg',
    'Library Green HUD.jpg',
    'Library HUD.jpg',
    'Library Red HUD.jpg',
    'Living Room Green HUD.jpg',
    'Living Room HUD.jpg',
    'Living Room Red HUD.jpg',
    'Porch Green HUD.jpg',
    'Porch HUD.jpg',
    'Porch Red HUD.jpg',
    'Shed Green HUD.jpg',
    'Shed HUD.jpg',
    'Shed Red HUD.jpg',
    'Study Green HUD.jpg',
    'Study HUD.jpg',
    'Study Red HUD.jpg',
    'Dining Room Green HUD.jpg',
    'Dining Room HUD.jpg',
    'Dining Room Red HUD.jpg',]

    for path in town_files:
        town_map = makePicture('\\assets\\images\\maps\\Plainsfeild.jpg')
        pic = makePicture('\\assets\\images\\huds\\%s'%path)
        pyCopyEx(town_map,pic, 891, 16)
        writePictureTo(pic,'\\assets\\images\\huds_with_maps\\%s'%path)

    for path in mansion_files:
        man_map = makePicture('\\assets\\images\\maps\\OverallMap.jpg')
        pic = makePicture('\\assets\\images\\huds\\%s'%path)
        pyCopyEx(man_map,pic, 891, 16)
        writePictureTo(pic,'\\assets\\images\\huds_with_maps\\%s'%path)

def tester():
    #function for testing inventory items.

    gasStation = Room("Gas Station", "gasStationDescription", ['Comic Book'],(932,228))
    joe = Player('joe', gasStation)
    joe.pickupItem('Comic Book')
    joe.talkToBruce()
    #joe.pickupItem('Key')
    #joe.pickupItem('Shovel')
    #joe.pickupItem('Walkman')
    #joe.pickupItem('Tape')
    #joe.pickupItem('Matches')
    show(joe.create_hud())
