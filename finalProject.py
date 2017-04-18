import os
import random
import time

isPathSet = False
total_iterations = 0

def progress_bar(current,total,time):
    #the collage takes so long I made this progress bar to keep me sane.
    fill = '#'
    empty = '~'
    output = ''
    fill_percent = (float(current)/float(total))*100
    if current != 0:
        time_remaining = int((time/fill_percent)*(100-fill_percent))
    for i in range(0,int(fill_percent/5)):
        output = output + fill
    for i in range(0,20-int(fill_percent/5)):
        output = output + empty
    if current != 0:
        printNow(output + " %.1f%% Complete - estimated %d minutes, %d seconds remaining."%(fill_percent,int(time_remaining/60),time_remaining%60))
    else:
        printNow(output + " %.1f%% Complete"%fill_percent)

class Room:
  #Initializes every room to have no surrounding rooms and to be in an unlocked state
  north = None
  east = None
  south = None
  west = None
  up = None
  down = None
  locked = false
  def __init__(self, name, description, items, img_path = None):
    self.name = name
    self.description = description
    self.items = items
    self.huds = []
    if img_path != None:
        self.make_huds(img_path)

  def make_huds(self,i_path):
        global total_iterations
        setMediaFolder('C:\\Users\\callen\\Google Drive\\CSUMB\\final_project\\')
        #global isPathSet
        #if not isPathSet:
        #    showInformation("Please Select the Root folder of our upload. The one that contains the *.py file.")
        #    setMediaFolder()
        #    isPathSet = True
        #font size for text
        font_size = 25
        """
        Hud Breakdown:
            Title: width (x): 30-842; height (y): 16-77
            Location Picture: width (x): 26-846; height (y): 100-559 [820x459]
            Text Area: width (x): 30-842; height (y): 602-863
            Map Area: width (x): 891-1359; height (y): 16-558 [468x542]
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
        path = 'assets\\images\\hud.jpg'
        hud_normal = makePicture(path)
        hud_red = makePicture(path)
        #if self.name == 'Mirror Room':
        #    hud_mirror = makePicture(path)
        #    hud_mirror_red = makePicture(path)
        title_font_size = 77-16
        sty = makeStyle(sansSerif,bold,title_font_size)
        addTextWithStyle(hud_normal,32+title_font_size,70,self.name,sty,black)
        addTextWithStyle(hud_red,32+title_font_size,70,self.name,sty,black)
        rm_img = makePicture(i_path)
        for x in range (0, getWidth(rm_img)):
            for y in range (0, getHeight(rm_img)):
                total_iterations = total_iterations + 1
                if x+26 < getWidth(hud_normal) and y+100 < getHeight(hud_normal):
                    src_color = getColor(getPixel(rm_img, x, y))
                    setColor(getPixel(hud_normal, x+26, y+100), src_color)
                    setColor(getPixel(hud_red, x+26, y+100), makeColor(min(int(src_color.getRed()*2),255),src_color.getGreen(),src_color.getBlue()))
        self.huds.append(hud_normal)
        self.huds.append(hud_red)


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
  #Holds the room that the current player is in
  currentRoom = None
  def __init__(self, name, room):
    self.name = name
    self.currentRoom = room
    self.hud = None
  #Returns name of current player
  def getName(self):
    return self.name

  #Heads Up Display set and get functions.
  def setHUD(self,hud_image):
    self.hud = hud_image

  def getHUD(self):
      return self.hud

  def print_hud(self):
      show(self.currentRoom.huds[0])
  ###Pickup Item Function###
  #step 1: Don't pickup if item is already in inventory
  #step 2: Make sure item is in current room
  #step 3: Print "Item not found" if item not in current room
  def pickupItem(self, item):
    #Check if player is already holding that item
    if item in self.inventory:
      printNow("You are already carrying that item")
    else:
      #Check if item is in the current room
      if item in self.currentRoom.getItems():
        if item == "Tape" or item == "Matches" or item == "CD":
          printNow("This might come in handy later")
        if item == "Lantern":
          printNow("This will come in very handy.  Now if only I can find some matches to actually light it with.")
        self.inventory.append(item)
        self.currentRoom.removeItem(item)
        printNow("You are now holding: %s"%self.inventory)
        printNow("The room now contains: %s"%self.currentRoom.getItems())
      #If item is not in current room, print item not found
      else:
        printNow("Item not found")

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

  #Returns the current inventory list of the user
  def getInventory(self):
    return self.inventory

  ###Move Player Functions###
  #step 1: Move the current player North,South,East, or West if there is a valid room in that direction.
  #step 2: If there is no room in that direction, alert the user
  def movePlayerNorth(self):
    if self.currentRoom.getNorth().getName() == "Living Room" and self.currentRoom.getNorth().isLocked():
      printNow("The door is locked.  You need a key.")
    else:
      if self.currentRoom.getNorth() != None:
        self.currentRoom = self.currentRoom.getNorth()
        printNow(self.currentRoom)
      else:
        printNow("There is no room to the North!")

  def movePlayerSouth(self):
    if self.currentRoom.getSouth() != None:
      self.currentRoom = self.currentRoom.getSouth()
      printNow(self.currentRoom)
    else:
      printNow("There is no room to the South!")

  def movePlayerEast(self):
    if self.currentRoom.getEast() != None:
      self.currentRoom = self.currentRoom.getEast()
      printNow(self.currentRoom)
    else:
      printNow("There is no room to the East!")

  def movePlayerWest(self):
    if self.currentRoom.getWest() != None:
      self.currentRoom = self.currentRoom.getWest()
      printNow(self.currentRoom)
    else:
      printNow("There is no room to the West!")

  def movePlayerUp(self):
    if self.currentRoom.getUp() != None:
      self.currentRoom = self.currentRoom.getUp()
      printNow(self.currentRoom)
    else:
      printNow("There is no room above you!")

  ###Only used to enter basement so user must have lit lantern equipped to see###
  def movePlayerDown(self):
    if self.currentRoom.getDown() != None:
      self.currentRoom = self.currentRoom.getDown()
      if "Lit Lantern" in self.inventory:
        self.secretRoomFound = true
        self.currentRoom.setDescription("""The basement is littered with old AV equipment.  Broken projectors, cassette recorders, televisions, and more.  In the corner is a furnace.  
        As your eyes adjust, you notice a poster for E.T. hanging on the wall.  That seems a little odd.""")
      else:
        self.currentRoom.setDescription("The basement is completely dark.  You cannot see anything.  It would not be safe to explore here unless you can find some sort of light source.")
      printNow(self.currentRoom)
    else:
      printNow("There is no room below you!")

  ###Use Item Functions###
  def useComputer(self):
    if self.currentRoom.getName() == "Study":
      printNow("""You attempt to turn on the Macintosh computer, but unfortunately it will not turn on.  You look over at the Apple II and chuckle.
      You walk over and hit the power button.  To your surprise it boots up.""")
      showInformation("This is where you play hangman and madlibs")
    else:
      showInformation("There is no computer in this room. Try visiting the Study")

  #step 1: make sure user has shovel
  #step 2: make sure user is in graveyard
  #step 3: if user has shovel and is in graveyard allow them to dig to retrieve key and map piece
  #step 4: break the shovel so the user cannot continue digging for more keys/map pieces
  def useShovel(self):
    if "Shovel" not in self.inventory:
      printNow("You do not have a shovel to use!")
    elif self.currentRoom.getName() != "Graveyard":
      printNow("You can't use the shovel here. Try using it somewhere outside.")
    elif self.currentRoom.getName() == "Graveyard" and "Shovel" in self.inventory:
      printNow("""The old shovel creaks under your weight as you plunge it deep into the cold earth.  You try one spot and then another.
      Finally on your third attempt you feel the shovel make contact with something hard.  Unfortunately, the handle cracks in half at 
      the same time.  So much for that.  You get down on your knees and dig around with your hands where you felt the shovel strike something hard.
      In the wet dirt you feel something small and metal.  You pull it up into the light and discover it is a key.  You found a key and a piece of the map!""")
      self.inventory.remove('Shovel')
      self.inventory.append('Broken Shovel')
      self.currentRoom.addItem('Key')
      self.currentRoom.addItem('Map Piece 1')
      printNow(self.currentRoom)
  #step 1: make sure user has the key in inventory
  #step 2: make sure user is on porch trying to get into mansion
  #unlock the door
  def useKey(self):
    if 'Key' not in self.inventory:
      printNow("You do not have a key!")
    else:
      if self.currentRoom.getName() == "Porch":
        if self.currentRoom.getNorth().isLocked():
          self.currentRoom.getNorth().setLocked(false)
          printNow("You hear the sweet sound of the front door unlocking.")
        else:
           self.currentRoom.getNorth().setLocked(true)
           printNow("The lock clicks in place as the door is secured.")
      else:
        printNow("You cannot use the key here!")
  #step 1: Make sure user is holding the matches and lantern
  #step 2: if user has matches but not the lantern, tell user they don't have anything to use matches on
  #step 3: Else: user doesn't have matches to use
  def useMatches(self):
    if "Matches" in self.inventory and "Lantern" in self.inventory:
      printNow("You use the matches to light the lantern")
      self.inventory.remove("Matches")
      self.inventory.remove("Lantern")
      self.inventory.append("Lit Lantern")
      printNow(self.inventory)
    elif "Matches" in self.inventory and "Lantern" not in self.inventory:
      printNow("You do not have anything to use the matches on!")
    else:
      printNow("You do not have any matches!")
<<<<<<< HEAD


  def search(self, item):
    if item == "cabinets" and self.currentRoom.getName() == "Kitchen":
      printNow("You search the cabinets and find a red potion. You place the potion in your inventory.")
      self.inventory.append("Red Potion")
      printNow(self.inventory)
    else:
      printNow("Error")

  def drinkRedPotion(self):
    showInformation("This is where we show the room image with moreRed function")

=======
      
  def useCouch(self):
    if self.currentRoom.getName() == "Living Room":
      printNow("Aaahhhh.  A well deserved break.  Well, time to get back to what you came here for.")
    else:
      printNow("There is no couch in this room.  Try going to the living room.")
      
  def useTelevision(self):
    if self.currentRoom.getName() == "Living Room":
      printNow("Broken!  Oh well, you didn’t come here to watch TV.")
    else:
      printNow("There is no television in this room.  Try going to the living room.")      
      
  def useSafe(self):
    if self.currentRoom.getName() == "Hidden Basement":
      code = requestString("Please enter the 7 digit code:")
      if code == "8675309":
        printNow("Success!  As you enter the last digit, you hear a click as the safe door pops open.")
        self.safeLocked = false
      else:
        printNow("Nothing!  You must have the wrong code.")
    else:
      printNow("There is no safe in here.")
        
  def useChair(self):
    if self.currentRoom.getName() == "Porch":
      printNow("""Not too bad; pretty comfy in fact.  As you slowly rock back and forth you begin to understand a little more of the appeal of a slower lifestyle.
      Oh, well.  Enough sitting.  Time to get back to it.""")
    elif self.currentRoom.getName() == "Library":
      printNow("Aahhh.  Now I just need a good book to read.  Which one to pick?")
    else:
      printNow("There is no chair in here.")
      
  def useWalkman(self):
    if "Walkman" in self.inventory:
      showInformation("This is where we play reading rainbow")
    else:
      printNow("You do not have a walkman in your inventory!")

  def drinkRedPotion(self):
    if "Red Potion" in self.inventory:
      showInformation("This is where we show the room image with moreRed function")
    else:
      printNow("You are not carrying this item")
    
>>>>>>> refs/remotes/origin/master
  def examine(self, item):
    if item == "bookshelf" and self.currentRoom.getName() == "Library":
      printNow("You look closely at the bookshelf.  It is filled with many great novels.  You notice several of your favorites.  Doug had good taste in literature.")
    elif item == "nautilus" and self.currentRoom.getName() == "Library":
<<<<<<< HEAD
      printNow("""You realize that Doug has several Jules Verne novels.  You reach for Â‘20,000 Leagues Under the SeaÂ’ from the shelf.
      As you attempt to pull the novel off the shelf the novel suddenly stops halfway out and one of the bookshelves pops open a few inches.
=======
      printNow("""You realize that Doug has several Jules Verne novels.  You reach for Â?20,000 Leagues Under the SeaÂ? from the shelf.  
      As you attempt to pull the novel off the shelf the novel suddenly stops halfway out and one of the bookshelves pops open a few inches.  
>>>>>>> refs/remotes/origin/master
      A hidden door.  Brilliant!""")
      #Basement initially set to "It is too dark to see anything
      #User must first find matches and lantern then use matches to light lantern
      #With lit lantern equipped, description changes to reveal contents of basement
      basement = Room("Hidden Basement", "This room is too dark to see anything! Try to find something to help you see.", [])
      self.currentRoom.setDown(basement)
      printNow(self.currentRoom)
      basement.setUp(self.currentRoom)
<<<<<<< HEAD


=======
    elif item == 'tombstone' and self.currentRoom.getName() == "Graveyard" and self.secretRoomFound:
      printNow("""You examine the tombstone again, but this time you lean closer.  You notice that some crabgrass has grown up and blocked the bottom part of the tombstone.
      You pull back the grass and notice several numbers in printed in small font along the base.  It reads, ‘100001000101111111101101’.""")
    elif item == 'tombstone' and self.currentRoom.getName() == "Graveyard" and not self.secretRoomFound:
      printNow("""You examine the tombstone and read the name ‘Douglas Adams’.  Underneath it says, ‘Digital Killed the Analog Star!’""")
    elif item == 'couch' and self.currentRoom.getName() == "Living Room":
      printNow("""You find some stale Cheez-Its and spare change in the couch cushions.  You take a look underneath and notice a small piece of parchment.
      It appears to be a piece to a map.""")
      self.inventory.append("Map Piece 4")
      printNow(self.inventory)
    elif item == 'television' and self.currentRoom.getName() == "Living Room":
      printNow("An old wood grained RCA.  A classic.  You look closer at the betamax tapes.  Hmm.  It looks like the old Adam West Batman series.")
    elif item == "cabinets" and self.currentRoom.getName() == "Kitchen":
      printNow("""You root through the cabinets and find a small bottle that reads, Vision en Rouge.
      Sounds fancy.  Wonder how it tastes? You place the potion in your inventory.""")
      self.inventory.append("Red Potion")
      printNow(self.inventory)
    elif item == "floor mat" and self.currentRoom.getName() == "Kitchen":
      printNow("You look under the floor mat and discover another piece to the map!")
      self.inventory.append("Map Piece 2")
      printNow(self.inventory)
    elif item == 'portrait' and self.currentRoom.getName() == "Dining Room":
      printNow("""The name underneath reads ‘Wilfred Adams’.  You notice a small piece of paper sticking out from behind the back.
      You tug on it and you find yourself holding another piece of the map.""")
      self.inventory.append("Map Piece 3")
      printNow(self.inventory)
    elif item == 'mirror' and self.currentRoom.getName() == "Dining Room":
      printNow("This mirror has some odd properties to it.")
      showInformation("Here we must implement mirrored image functionality")
    elif item == 'furnace' and self.currentRoom.getName() == "Hidden Basement":
      printNow("This has not been lit in years.  Better not chance it.")
    elif item == 'poster' and self.currentRoom.getName() == "Hidden Basement":
      printNow("""You look closely at the poster.  It looks genuine.  You notice one corner is not completely held down.
      You give a gentle tug and notice there is something behind the poster.  You pull a little harder, careful not to damage the poster.
      You pull the poster completely off the wall to reveal a safe hidden behind it.  You are close.  You can feel it.""")
    elif item == 'safe' and self.currentRoom.getName() == "Hidden Basement" and self.safeLocked:
      printNow("The safe is locked.")
    elif item == 'safe' and self.currentRoom.getName() == "Hidden Basement" and not self.safeLocked:
      printNow("""You open the safe to reveal its contents.  You pull out a 1978 comic book, ‘Batman versus Muhammad Ali’.  It appears the comic book has been autographed.
      You place the comic book in your backpack.""")
      self.inventory.append("Comic Book")
      printNow(self.inventory)
    elif item == 'comic book' and "Comic Book" in self.inventory:
      printNow("""You look closely at the comic book to read the inscription.
      “To my dear son, Douglas.  Whether you grow up to be Batman or Bruce, I’ll always be proud of you.  I love you.  Dad.”
      You notice that the cover art to the comic book was by Neal Adams.
      Neal Adams was Douglas Adams father!  Amazing!
      But that still doesn’t solve the mystery.
      Where is Doug?
      ********************
      Batman or Bruce?
      Batman or Bruce?
      OMG!  I had the answer right in front of me from the very beginning.
      I need to get back to town right away.""")
    elif item == 'walkman' and 'Walkman' in self.inventory:
      printNow("Wow! Talk about old school.  It looks like it has a mix tape in it.  Wonder if it works?")
  
>>>>>>> refs/remotes/origin/master

  #Returns current room of player
  def getCurrentRoom(self):
    return self.currentRoom

  def __str__(self):
    return ("Name: %s\nCurrent Location: %s\nPlayer Inventory: %s\n")%(self.name, self.currentRoom, self.inventory)

  def print_hud_item(self,hud,index,item):
      """
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
          'Key': 'assets\\images\\item_icons\\key.jpg',
          'Red Potion': 'assets\\images\\item_icons\\potion_red.jpg',
          'Purple Potion': 'assets\\images\\item_icons\\potion_purple.jpg',
          'Map': 'assets\\images\\item_icons\\Map.jpg',
          'Lantern': 'assets\\images\\item_icons\\lantern.jpg',
          'Broken Shovel': 'assets\\images\\item_icons\\broken_shovel.jpg',
          }
      origins = [(903,602),(1062,602),(1220,602),(903,740),(1062,740),(1220,740)]
      pyCopyEx(makePicture(i_path[item]),hud,origins[index][0],origins[index][1],getColor(getPixel(makePicture(i_path[item]),0,0)))

n_images = {
    'map': [],
}

def mysteryMansion():
  global total_iterations
  start_time = time.time()
  #Is game over?
  done = false
  #Description of living room
  livingRoomDescription = """The living room is one of the largest rooms in the old mansion.  It interior is dark as most of the curtains and shades are drawn.
  In the middle is a couch with two end tables on each side.  One end table has a lamp on it, while the other has a lantern.  To the left is a large overstuffed arm chair.
  There is a coffee table in front of the couch and an old wood grained RCA television sitting on the floor in front of the coffee table.  On top of the television was a betamax player
  and several betamax tapes.  Framed pictures decorate the walls on every side."""
  #Description of kitchen
  kitchenDescription = """The kitchen was surprisingly one of the cleaner rooms in the mansion.  ‘Guessing the owner was not much of a cook.’  The interior was vintage 70s.  Wood cabinets with old ivory pull knobs.
  There was an oven, range top stove, and refrigerator...all avocado green.  The sink still has a few glasses in it, but nothing else seemed to be out of place.
  The floor was linoleum and there was an old mat in front of the kitchen sink.  The dirtiest thing in the whole room was an old microwave sitting on the counter.
  This was obviously the owner’s appliance of choice, lol.  By the far wall under the window was a small table with a single solitary chair.  ‘Guess he didn’t entertain too many guests.’
  On the table was some sort of bar."""
  #Description of Porch
  porchDescription = """The porch is big and expansive as was the style in the midwest.  The floor boards and rails are showing their age.  The whole thing is in desperate need of being refinished.
  On the left side of the porch is an old rocking chair with a small table next to it.  On the table is an ashtray and a coaster.  To the right of the rocking chair is the front door to the mansion painted a bright red color.
  Beneath the door is a mat that says ‘Welcome’."""
  #Description of Graveyard
  graveyardDescription = """The graveyard is small and sits on a hill adjacent to the mansion.  The headstones are laid out in a haphazard manner.  It appears to be a family cemetery for the Adams’ family.
  Some of the dates go back to the 1700s.   The cemetery suffers from obvious years of neglect as many of the headstones are in disrepair and the weeds and ivy are overgrown.
  In the middle of the graveyard is an old oak tree that stretches far above the entire cemetery."""
  #Description of Shed
  shedDescription = """The shed is an old dilapidated shed halfway between the graveyard and the mansion.  It appears it was probably used to store tools and such, although it could contain anything.
  The shed has a small padlock on the outside."""
  #Description of Library
  libraryDescription = """You are immediately confronted with the smell of musty books.  The library is filled with bookshelves along every wall.  Each shelf is stuffed with books of every shape and size.
  In the middle of the library is an old leather arm chair and an end table.  On the end table appears to be a walkman."""
  #Description of Study
  studyDescription = """The study was the messiest of all the rooms.  There was a desk in the middle with an old Macintosh computer.  Papers were piled up in an organization that could only be guessed at.
  In the right corner was a smaller desk with an old Apple II computer on it.  In the left corner was a grandfather clock that appeared to still be keeping time."""
  #Description of Dining Room
  diningRoomDescription = """The dining room is very ornate.  In the center is a large dining table with candles.  The table has place settings for 12 people although it appears that it was rarely used.
  Towards the back of the room is a large mirror that stretches from floor to ceiling.  Above the dining table was a large glass chandelier.  Opposite the mirror is a large portrait of a man."""
  #Create all the rooms in the mansion
<<<<<<< HEAD
  kitchen = Room("Kitchen","A Place to cook meals",["Map Piece 2"],'\\assets\\images\Porch.jpg')
  progress_bar(total_iterations,3049686,time.time()-start_time)
  porch = Room("Porch", "Front porch", [], '\\assets\\images\Porch.jpg')
  progress_bar(total_iterations,3049686,time.time()-start_time)
  graveyard = Room("Graveyard", "A cemetery filled with ancient headstones", [], '\\assets\\images\Graveyard.jpg')
  progress_bar(total_iterations,3049686,time.time()-start_time)
  shed = Room("Shed", "An old shed full of cobwebs", ["Shovel"],'\\assets\\images\Porch.jpg')
  progress_bar(total_iterations,3049686,time.time()-start_time)
  library = Room("Library", "A room filled with old looking books", ["Book", "Map Piece 3"], '\\assets\\images\Library.jpg')
  progress_bar(total_iterations,3049686,time.time()-start_time)
  study = Room("Study", "A room filled with old papers and an ancient looking computer", ["CD", "Matches", "Tape"],'\\assets\\images\Porch.jpg')
  progress_bar(total_iterations,3049686,time.time()-start_time)
  livingRoom = Room("Living Room", "It looks like nobody has lived here for centuries", ["Lantern", "Map Piece 4"],'\\assets\\images\LivingRoom.jpg')
  progress_bar(total_iterations,3049686,time.time()-start_time)
=======
  kitchen = Room("Kitchen",kitchenDescription,[])
  porch = Room("Porch", porchDescription, [])
  graveyard = Room("Graveyard", graveyardDescription, [])
  shed = Room("Shed", shedDescription, ["Shovel"])
  library = Room("Library", libraryDescription, ["Walkman"])
  study = Room("Study", studyDescription, ["CD", "Matches", "Tape"])
  livingRoom = Room("Living Room", livingRoomDescription, ["Lantern"])
>>>>>>> refs/remotes/origin/master
  ###Lock front door of living room###
  #livingRoom.setLocked(true)
<<<<<<< HEAD



=======
  diningRoom = Room("Dining Room", diningRoomDescription, [])
  
  
>>>>>>> refs/remotes/origin/master
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

  ##get character name##
  playerName = requestString("Please enter your character's name:")
  #create player object
  player = Player(playerName, porch)
  #Print player details
  printNow(player)
  player.print_hud()
  #All the possible actions a user may enter and the corresponding function to call
  actions = {
    ###Print Functions###
    'print room': 'printNow(player.getCurrentRoom())',
    'print inventory': 'printNow(player.inventory)',
    'print player': 'printNow(player)',
    ###Pickup Functions###
    'pickup potion': "player.pickupItem('Potion')",
    'pickup map piece 1': "player.pickupItem('Map Piece 1')",
    'pickup map piece 2': "player.pickupItem('Map Piece 2')",
    'pickup map piece 3': "player.pickupItem('Map Piece 3')",
    'pickup map piece 4': "player.pickupItem('Map Piece 4')",
    'pickup key': "player.pickupItem('Key')",
    'pickup shovel': "player.pickupItem('Shovel')",
    'pickup cd': "player.pickupItem('CD')",
    'pickup tape': "player.pickupItem('Tape')",
    'pickup lantern': "player.pickupItem('Lantern')",
    'pickup matches': "player.pickupItem('Matches')",
    'pickup lit lantern': "player.pickupItem('Lit Lantern')",
    'pickup walkman': "player.pickupItem('Walkman')",
    ###Drop Functions###
    'drop potion': "player.pickupItem('Potion')",
    'drop map piece 1': "player.dropItem('Map Piece 1')",
    'drop map piece 2': "player.dropItem('Map Piece 2')",
    'drop map piece 3': "player.dropItem('Map Piece 3')",
    'drop map piece 4': "player.dropItem('Map Piece 4')",
    'drop key': "player.dropItem('Key')",
    'drop shovel': "player.dropItem('Shovel')",
    'drop cd': "player.dropItem('CD')",
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
  }

  #Continue requesting next move until game ends, or user types exit/quit
  while not done:
    #get next action from user
    action = requestString("Please enter next move").lower()
    #Get help screen
    if action == "help":
      showInformation("Help goes here....")
    #End game if user types 'exit' or 'quit'
    elif action == "exit" or action == "quit":
      done = true
      break
    #Attempt to evaluate the action entered by user.
    else:
      try:
        eval(actions[action])
      #Handles error from an invalid action
      except:
        printNow("Not a valid move")


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

def img_preload():
    #Handles all image scrambling at beginning
    path = 'C:\\Users\\caleb\\Google Drive\\CSUMB\\final_project\\Map.jpg'
    ##############Get unaltered image#############
    pic = makePicture(path)
    n_images['map'].append(pic)

    for i in range(1,3):
        pic = makePicture(path)
        img_scramble(pic,i*4)
        n_images['map'].append(pic)

    full_scram = makePicture(path)
    img_scramble(full_scram,0)
    n_images['map'].append(full_scram)

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

def txt_to_lines(txt,font_size):
    ret = []
    isEoF = False
    index = 0
    while not isEoF:
        max_index = index+int(3.75*font_size)
        if max_index < len(txt):
            end_index = index + find_last_space(txt[index:max_index])
            ret.append(txt[index:end_index])
            index = end_index
        else:
            ret.append(txt[index:len(txt)])
            isEoF = True

    return ret
def make_screen():
    path = 'C:\\Users\\caleb\\Google Drive\\CSUMB\\final_project\\assets\\images\\hud.jpg'

    desc = 'It looks like nobody has lived here for centuries'
    font_size = 25
    canvas = makeEmptyPicture(1200,900)
    setAllPixelsToAColor(canvas,black)
    pyCopyEx(makePicture(path),canvas,30,30)
    sty = makeStyle(sansSerif,bold,font_size)
    desc_lines = txt_to_lines(desc,font_size)
    for ln in range(len(desc_lines)):
        addTextWithStyle(canvas,30,720+(font_size*(1+ln)),desc_lines[ln],sty,red)
    show(canvas)

def tester():
    joe = Player('joe',Room("Living Room", "It looks like nobody has lived here for centuries", ["Lantern", "Map Piece 4"],'assets\\images\\LivingRoom.jpg'))
    printNow(str(joe))
    joe.make_hud()
