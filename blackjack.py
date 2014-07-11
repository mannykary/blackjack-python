import random
import sys

def main():
  suits = ('H S D C').split()
  ranks = ('2 3 4 5 6 7 8 9 10 J Q K A').split()
  deck = []

  for i in suits:
    for j in ranks:
      deck.append(j + ':' + i)

  random.shuffle(deck)
  print deck

  [p, d] = deal(deck)

  print "You have: " + str(p)
  print "Your score is " + str(score(p))

  if score(p) == 21:
    var = raw_input("You have won! Deal again? Y/N ")
    deal_again(var)

  stand = False

  while score(p) < 21 and stand == False:
    var = raw_input("Hit (H) or Stand (S)? ")

    if var.upper() == 'H':
      hit(deck, p)
      print "You have: " + str(p)
      print "Your score is " + str(score(p))

      if score(p) > 21:
        var = raw_input("You have busted. Deal again? Y/N ")
        deal_again(var)

      if score(p) == 21:
        var = raw_input("You have won! Deal again? Y/N ")
        deal_again(var)

    elif var.upper() == 'S':
      stand = True
      print "Dealer has: " + str(d) + " (score: " + str(score(d)) + ")"

      while score(d) < 17:
        hit(deck, d)
        print "Dealer hits, now has: " + str(d) + " (score: " + str(score(d)) + ")"

        if score(d) > 21:
          var = raw_input("Dealer has busted. You have won! Deal again? Y/N ")
          deal_again(var)
        elif score(d) >= 17:
          if score(d) == score(p):
            var = raw_input("You and dealer have same score. Push! Deal again? Y/N ")
            deal_again(var)
          elif score(p) > score(d):
            var = raw_input("You beat the dealer! Deal again? Y/N ")
            deal_again(var)
          elif score(p) < score(d):
            var = raw_input("You lost to the dealer. Deal again? Y/N ")
            deal_again(var)

    else:
      print "Please enter H to hit, or S to stand."

def deal_again(var):
  if var.upper() == 'Y':
    main()
  else:
    sys.exit()

def deal(deck):
  player = [deck.pop(), deck.pop()]
  dealer = [deck.pop(), deck.pop()]
  return [player, dealer]

def hit(deck, hand):
  hand.append(deck.pop())

def score(hand):

  score = 0
  num_aces = 0

  for i in hand:
    rank = i.split(':')[0]
    if rank in ('J', 'Q', 'K'):
      score += 10
    elif rank == 'A':
        score += 11  # need to add in logic to change ace value from 11 to 1 as needed.
        num_aces += 1
    else:
      score += int(rank)

  return score

main()
