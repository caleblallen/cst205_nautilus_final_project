class Room:
  #Initializes every room to have no surrounding rooms and to be in an unlocked state
  north = None
  east = None
  south = None
  west = None
  up = None
  down = None
  locked = false
  def __init__(self, name, description, items):
    self.name = name
    self.description = description
    self.items = items
  
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
  #Prints the room object as a string
  def __str__(self):
    return ("%s: %s.  This room contains %s\n%s\n")%(self.name, self.description, self.items,self.getAdjacentRooms())
    
    
class Player:
  #The items the player is holding
  inventory = []
  #Holds the room that the current player is in
  currentRoom = None
  def __init__(self, name, room):
    self.name = name
    self.currentRoom = room
  #Returns name of current player  
  def getName(self):
    return self.name
  
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
      printNow("This door is locked!")
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
        self.currentRoom.setDescription("Why was this room hidden? In the corner you see an old decryption machine.")
      else:
        self.currentRoom.setDescription("It is too dark down here to see anything. Try finding something to help you see.")
      printNow(self.currentRoom)
    else:
      printNow("There is no room below you!")
      
  ###Use Item Functions###
  def useComputer(self):
    if self.currentRoom.getName() == "Study":
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
      printNow("You dig a hole in front of a large headstone.\nYou found a key and a piece of the map!")
      printNow("The old shovel breaks from digging and is no longer usable")
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
          printNow("You use the key to unlock the door")
        else:
           self.currentRoom.getNorth().setLocked(true)
           printNow("You use the key to lock the door")
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
  
  #Returns current room of player
  def getCurrentRoom(self):
    return self.currentRoom
    
  def __str__(self):
    return ("Name: %s\nCurrent Location: %s\nPlayer Inventory: %s\n")%(self.name, self.currentRoom, self.inventory)
    

def mysteryMansion():
  #Is game over?
  done = false
  
  #Create all the rooms in the mansion
  kitchen = Room("Kitchen","A Place to cook meals",["Potion","Map Piece 2"])
  porch = Room("Porch", "Front porch", [])
  graveyard = Room("Graveyard", "A cemetery filled with ancient headstones", [])
  shed = Room("Shed", "An old shed full of cobwebs", ["Shovel"])
  library = Room("Library", "A room filled with old looking books", ["Book", "Map Piece 3"])
  study = Room("Study", "A room filled with old papers and an ancient looking computer", ["CD", "Matches", "Tape"])
  livingRoom = Room("Living Room", "It looks like nobody has lived here for centuries", ["Lantern", "Map Piece 4"])
  ###Lock front door of living room###
  #livingRoom.setLocked(true)
  #Basement initially set to "It is too dark to see anything
  #User must first find matches and lantern then use matches to light lantern
  #With lit lantern equipped, description changes to reveal contents of basement
  basement = Room("Hidden Basement", "This room is too dark to see anything! Try to find something to help you see.", [])
  
  ###Build the mansion/room relationships###
  porch.setNorth(livingRoom)
  porch.setEast(graveyard)
  graveyard.setWest(porch)
  graveyard.setNorth(shed)
  shed.setSouth(graveyard)
  livingRoom.setSouth(porch)
  livingRoom.setWest(study)
  livingRoom.setNorth(library)
  study.setEast(livingRoom)
  library.setSouth(livingRoom)
  library.setEast(kitchen)
  library.setDown(basement)
  kitchen.setWest(library)
  basement.setUp(library)
  
  ##get character name##
  playerName = requestString("Please enter your character's name:")
  #create player object
  player = Player(playerName, porch)
  #Print player details
  printNow(player)
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
    'pickup book': "player.pickupItem('Book')",
    'pickup cd': "player.pickupItem('CD')",
    'pickup tape': "player.pickupItem('Tape')",
    'pickup lantern': "player.pickupItem('Lantern')",
    'pickup matches': "player.pickupItem('Matches')",
    'pickup lit lantern': "player.pickupItem('Lit Lantern')",
    ###Drop Functions###
    'drop potion': "player.pickupItem('Potion')",
    'drop map piece 1': "player.dropItem('Map Piece 1')",
    'drop map piece 2': "player.dropItem('Map Piece 2')",
    'drop map piece 3': "player.dropItem('Map Piece 3')",
    'drop map piece 4': "player.dropItem('Map Piece 4')",
    'drop key': "player.dropItem('Key')",
    'drop shovel': "player.dropItem('Shovel')",
    'drop book': "player.dropItem('Book')",
    'drop cd': "player.dropItem('CD')",
    'drop tape': "player.dropItem('Tape')",
    'drop lantern': "player.dropItem('Lantern')",
    'drop matches': "player.dropItem('Matches')",
    'drop broken shovel': "player.dropItem('Broken Shovel')",
    'drop lit lantern': "player.dropItem('Lit Lantern')",
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
      
      
    