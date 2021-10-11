import sys

def verify(guess):
  vals = [ 159,168,181,152,178,152,245,152,164,247,247,171,152,243,152,189,164,175,247,168,246]

  if len(guess) != 21:
    return False

  for i, c in enumerate(guess):
    if (ord(c) ^ 199) != vals[i]:
      return False 
  return True


if len(sys.argv) != 1:
  print "Usage: python2 rev1.py"
  exit(1)

guess = raw_input("Enter the flag: ");

if verify(guess):
  print "That's the correct flag!"
else:
  print "Wrong flag."
