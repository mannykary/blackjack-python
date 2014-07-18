import random
import sys

class Player:
  def __init__(self):
    self.name = None
    self.hand = None

  def name(self, n):
    self.name = n

  def hand(self, h):
    self.hand = h

player = Player()
dealer = Player()

def initialize():
  player.name = get_player_name()
  dealer.name = 'Dealer'
  start_round()

def start_round():
  deck = get_new_deck()
  [player.hand, dealer.hand] = deal(deck)
  display_hand_and_score(player)

  if has_blackjack(player.hand):
    if has_blackjack(dealer.hand):
      print "Both have blackjack! Push!"
    else:
      print "You have blackjack!"

    display_hand_and_score(dealer)
    #ask_to_deal_again()

  else:
    stand = False

    while score(player.hand) < 21 and stand == False:
      next_step = hit_or_stand()

      if next_step == 'H':
        hit(deck, player.hand)
        display_hand_and_score(player)

        if is_busted(player.hand):
          print "You have busted."
          #ask_to_deal_again()
        elif score(player.hand) == 21:
          keep_hitting_dealer(deck, dealer.hand)
          if score(dealer.hand) == 21:
            print "Push!"
          else:
            print "You win!"
          #ask_to_deal_again()

      elif next_step == 'S':
        stand = True
        keep_hitting_dealer(deck, dealer.hand)
        if score(player.hand) > score(dealer.hand):
          print "You win!"
        elif score(player.hand) == score(dealer.hand):
          print "Push!"
        else:
          print "Dealer wins."
        #ask_to_deal_again()

      else:
        print "Please enter H to hit, or S to stand."

  ask_to_deal_again()

def hit_or_stand():
  response = raw_input("Hit (H) or Stand (S)? ")
  return response.upper()

def is_busted(hand):
  return score(hand) > 21

def keep_hitting_dealer(deck, hand):
  display_hand_and_score(dealer)

  while score(hand) < 17:

    hit(deck, hand)
    display_hand_and_score(dealer)

    if is_busted(dealer.hand):
      print "Dealer has busted. You win!"
      ask_to_deal_again()

def get_player_name():
  player_name = raw_input("Welcome to Manny's Casino! Please enter your name.\n")

  while player_name == '':
    player_name = raw_input("You did not enter a name! Please enter your name.\n")

  return player_name

def ask_to_deal_again():
  response = raw_input("Deal again? (Y/N) ")
  if response.upper() == 'Y':
    start_round()
  elif response.upper() == 'N':
    sys.exit()
  else:
    print "Please enter Y to deal again, or N to exit."
    ask_to_deal_again()

def deal(deck):
  print "\nDealing cards..."
  player = [deck.pop(), deck.pop()]
  dealer = [deck.pop(), deck.pop()]
  return [player, dealer]

def has_blackjack(hand):
  return score(hand) == 21

def hit(deck, hand):
  hand.append(deck.pop())

def display_hand_and_score(player_obj):
  print player_obj.name + ' has: ' + str(player_obj.hand) + ' (Score: ' + str(score(player_obj.hand)) + ')'

def get_new_deck():
  suits = ('Hearts Spades Diamonds Clubs').split()
  ranks = ('2 3 4 5 6 7 8 9 10 J Q K A').split()
  deck = []

  for i in suits:
    for j in ranks:
      deck.append(j + ' of ' + i)

  random.shuffle(deck)

  return deck

def score(hand):

  score = 0
  number_of_aces = 0

  for i in hand:
    rank = i.split(' of ')[0]
    if rank in ('J', 'Q', 'K'):
      score += 10
    elif rank == 'A':
        score += 11
        number_of_aces += 1
    else:
      score += int(rank)

  if score > 21 and number_of_aces > 0:
    i = number_of_aces
    while i > 0:
      score -= 10
      if score < 21:
        break
      else:
        i -= 1

  return score

initialize()
