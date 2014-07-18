import random
import sys

class Player:
  def __init__(self):
    self.name = None
    self.hand = None
    self.chips = 0  #change to 100 in final version.

  def name(self, n):
    self.name = n

  def hand(self, h):
    self.hand = h

  def chips(self, c):
    self.chips = c

player = Player()
dealer = Player()

def initialize():
  player.name = get_player_name()
  player.chips = 100
  dealer.name = 'Dealer'
  start_round()

def start_round():
  deck = get_new_deck()

  if player.chips > 0:
    player_bet = receive_bet()
  else:
    print "You have no more chips!"
    ask_to_play_again()

  [player.hand, dealer.hand] = deal(deck)
  display_hand_and_score(player)

  if has_blackjack(player.hand):
    if has_blackjack(dealer.hand):
      print "Both have blackjack! Push!"
      player.chips += player_bet
    else:
      print "You have blackjack!"
      player.chips += 2*player_bet

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
          keep_hitting_dealer(deck, dealer.hand, player_bet)
          if score(dealer.hand) == 21:
            print "Push!"
            player.chips += player_bet
          else:
            print "You win!"
            player.chips += 2*player_bet
          #ask_to_deal_again()

      elif next_step == 'S':
        stand = True
        keep_hitting_dealer(deck, dealer.hand, player_bet)
        if score(player.hand) > score(dealer.hand):
          print "You win!"
          player.chips += 2*player_bet
        elif score(player.hand) == score(dealer.hand):
          print "Push!"
          player.chips += player_bet
        else:
          print "Dealer wins."
        #ask_to_deal_again()

      else:
        print "Please enter H to hit, or S to stand."

  ask_to_deal_again()

def receive_bet():
  print "You have " + str(player.chips) + " chips."

  bet = raw_input("Please enter the number of chips to bet. ")

  try:
    if int(bet) < 1:
      print "The minimum bet is 1 chip."
      receive_bet()
    elif int(bet) > player.chips:
      print "You do not have that many chips!"
      receive_bet()
    else:
      player.chips -= int(bet)
      return int(bet)

  except TypeError:
    print "You did not enter a valid bet."
    receive_bet()

def hit_or_stand():
  response = raw_input("Hit (H) or Stand (S)? ")
  return response.upper()

def is_busted(hand):
  return score(hand) > 21

def keep_hitting_dealer(deck, hand, bet):
  display_hand_and_score(dealer)

  while score(hand) < 17:

    hit(deck, hand)
    display_hand_and_score(dealer)

    if is_busted(dealer.hand):
      print "Dealer has busted. You win!"
      player.chips += 2*bet
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

def ask_to_play_again():
  response = raw_input("Play again? (Y/N) ")
  if response.upper() == 'Y':
    initialize()
  elif response.upper() == 'N':
    sys.exit()
  else:
    print "Please enter Y to play again, or N to exit."
    ask_to_play_again()

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

  # if score > 21 and number_of_aces > 0:
  #   i = number_of_aces
  #   while i > 0:
  #     score -= 10
  #     if score < 21:
  #       break
  #     else:
  #       i -= 1

  if score > 21 and number_of_aces > 0:
    for i in range(number_of_aces, 0, -1):
      score -=10
      if score < 21:
        break

  return score

initialize()
