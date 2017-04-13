##Dustin Whittington
##Caleb Allen
import random
import calendar


def singleDieRoll():
  return random.randint(1,6)

def roll():
  dice1 = singleDieRoll()
  dice2 = singleDieRoll()
  sum = dice1 + dice2
  printNow("You rolled a %s and a %s.  The sum equals %s"%(dice1, dice2, sum))
  return sum
      
def playCraps():
  rollCount = 0
  gameOver = false
  point = None
  
  while not gameOver:
    rollCount += 1
    sum = roll()
    if rollCount == 1:
      if sum == 7 or sum == 11:
        printNow("You Win!")
        gameOver = true
      elif sum == 2 or sum == 3 or sum == 12:
        printNow("You Lose!")
        gameOver = true
      else:
        point = sum
        printNow("The point is now %s"%point)
        gameOver = false
    else:
      if sum == point:
        printNow("You rolled the point!\nYou Win!")
        gameOver = true
      elif sum == 7:
        printNow("You Lose!")
        gameOver = true
      else:
        gameOver = false
        
def printBirthMonth():
  month = requestString("What Month were you born in:").lower()
  dic = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12}
  year = requestInteger("What Year were you born in:")
  calendar.prmonth(year, dic[month], w=4, l=1)
  