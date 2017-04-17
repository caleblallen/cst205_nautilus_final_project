import random

def img_scramble(pic,scramble_level):
  pix = getPixels(pic)
  scramble_level = int(scramble_level)
  original = pix[:]
  indices = range(len(pix))
  random.shuffle(indices)
  for i in range(len(indices)):
    if random.randint(1,scramble_level) != 1:
      setColor(pix[indices[i]],getColor(original[i]))
    