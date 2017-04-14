##Lab15
##Dustin Whittington
##Caleb Allen
import random
import calendar
import datetime

#Rolls a single dice and returns a random value between 1 and 6
def singleDieRoll():
  return random.randint(1,6)

def roll():
  #Roll both dice
  dice1 = singleDieRoll()
  dice2 = singleDieRoll()
  #Calculate sum of both dice
  sum = dice1 + dice2
  #Print the users roll
  printNow("You rolled a %s and a %s.  The sum equals %s"%(dice1, dice2, sum))
  return sum
      
def playCraps():
  #Number of times user has rolled
  rollCount = 0
  #Ends game is set to true
  gameOver = false
  #The Point
  point = None
  
  #Continue rolling until game ends
  while not gameOver:
    #Increase the roll count by 1
    rollCount += 1
    #Roll the dice
    sum = roll()
    #First roll rules
    if rollCount == 1:
      #Win conditions
      if sum == 7 or sum == 11:
        printNow("You Win!")
        gameOver = true
      #Lose conditions
      elif sum == 2 or sum == 3 or sum == 12:
        printNow("You Lose!")
        gameOver = true
      #If user rolls a value that is not 7,11,2,3, or 12
      else:
        point = sum
        printNow("The point is now %s"%point)
        gameOver = false
    #Rules for rolls after first roll
    else:
      #Win Condition
      if sum == point:
        printNow("You rolled the point!\nYou Win!")
        gameOver = true
      #Lose Condition
      elif sum == 7:
        printNow("You Lose!")
        gameOver = true
      #Else continue rolling
      else:
        gameOver = false
        
def printBirthMonth():
  #Get users birth month
  month = requestString("What Month were you born in:").lower()
  #Dictionary to convert month into an integer
  dic = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12}
  #Get users birth year
  year = requestInteger("What Year were you born in:")
  #Print the month of the corresponding month year
  calendar.prmonth(year, dic[month])
  
def daysUntilBirthday():
  #Get users birthday
  date = requestString("Please Enter Your Birthday mm-dd-yyyy:")
  #Split date into an array of values
  values = date.split("-")
  #Get todays date object
  today = datetime.date.today()
  #Create a date object of the users birthday this year
  nextBirthday = datetime.date(datetime.date.today().year,int(values[0]),int(values[1]))
  #Find the time between birthday and today
  daysUntil = nextBirthday - today
  #Check if user has already had their birthday this year
  if daysUntil < datetime.timedelta(0):
    nextBirthday = datetime.date(datetime.date.today().year + 1,int(values[0]),int(values[1]))
    daysUntil = nextBirthday - today
  #Print the days until next birthday
  print "There are %s days until your birthday!"%daysUntil.days
  
def ratifiedDOI():
  #calendar.weekday returns integer of the day of week (0 = Monday, 1 = Tuesday, etc.)
  #calendar.day_name holds the corresponding names of the days of the week
  print "The Declaration of Independence was ratified on a %s"%calendar.day_name[calendar.weekday(1776,7,4)]
  
  