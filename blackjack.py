import random
import sys

class Player:
  def __init__(self):
    self.name = None
    self.hand = None
    self.chips = 0

  def name(self, n):
    self.name = n

  def hand(self, h):
    self.hand = h

  def chips(self, c):
    self.chips = c


def initialize():
  player = Player()
  dealer = Player()
  player.name = get_player_name()
  player.chips = 100
  dealer.name = 'Dealer'
  start_round(player, dealer)


def get_player_name():
  player_name = raw_input("\nWelcome to Manny's Casino! Please enter your name.\n")
  while player_name == '':
    player_name = raw_input("You did not enter a name! Please enter your name.\n")
  return player_name


def start_round(player, dealer):
  deck = get_new_deck()
  player_bet = receive_bet(player)
  [player.hand, dealer.hand] = deal(deck)
  display_hand_and_score(player)

  if not blackjack_exists(player, dealer, player_bet):
    stand = False

    while not is_busted(player.hand) and stand == False:
      next_step = hit_or_stand()

      if next_step == 'H':
        hit_player(deck, player, player_bet)
        if score(player.hand) == 21:
          stand = True
          keep_hitting_dealer(deck, dealer, player, player_bet)
          if not is_busted(dealer.hand):
            compare_scores(player, dealer, player_bet)

      elif next_step == 'S':
        stand = True
        keep_hitting_dealer(deck, dealer, player, player_bet)
        if not is_busted(dealer.hand):
          compare_scores(player, dealer, player_bet)

      else:
        print "Please enter H to hit, or S to stand."

  ask_to_deal_again(player, dealer)


def get_new_deck():
  suits = ('Hearts Spades Diamonds Clubs').split()
  ranks = ('2 3 4 5 6 7 8 9 10 J Q K A').split()
  deck = []
  for i in suits:
    for j in ranks:
      deck.append(j + ' of ' + i)
  random.shuffle(deck)
  return deck


def receive_bet(p):
  if p.chips > 0:
    print "You have " + str(p.chips) + " chips."
    bet = raw_input("Please enter the number of chips to bet. ")

    try:
      if int(bet) < 0:
        print "You did not enter a valid bet."
        receive_bet(p)
      elif int(bet) < 1:
        print "The minimum bet is 1 chip."
        receive_bet(p)
      elif int(bet) > p.chips:
        print "You do not have that many chips!"
        receive_bet(p)
      else:
        p.chips -= int(bet)
        return int(bet)
    except ValueError:
      print "You did not enter a valid bet."
      receive_bet(p)

  else:
    print "You have no more chips!"
    ask_to_play_again()


def deal(deck):
  print "\nDealing cards..."
  player = [deck.pop(), deck.pop()]
  dealer = [deck.pop(), deck.pop()]
  return [player, dealer]


def display_hand_and_score(player):
  print player.name + ' has: ' + str(player.hand) + ' (Score: ' + str(score(player.hand)) + ')'


def blackjack_exists(p, d, bet):
  if has_blackjack(p.hand) and has_blackjack(d.hand):
    print "Both have blackjack! Push!"
    display_hand_and_score(d)
    p.chips += bet
    return True
  elif has_blackjack(p.hand) and not has_blackjack(d.hand):
    print "You have blackjack!"
    display_hand_and_score(d)
    p.chips += 2*bet
    return True
  elif not has_blackjack(p.hand) and has_blackjack(d.hand):
    print "Dealer has blackjack. You lose."
    display_hand_and_score(d)
    return True
  else:
    return False


def has_blackjack(hand):
  return score(hand) == 21


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
    for i in range(number_of_aces, 0, -1):
      score -=10
      if score < 21:
        break

  return score


def hit_or_stand():
  response = raw_input("Hit (H) or Stand (S)? ")
  return response.upper()


def hit_player(deck, player, bet):
  hit(deck, player.hand)
  display_hand_and_score(player)
  if is_busted(player.hand):
    print "You have busted."


def keep_hitting_dealer(deck, dealer, player, bet):
  display_hand_and_score(dealer)
  while score(dealer.hand) < 17:
    hit(deck, dealer.hand)
    display_hand_and_score(dealer)
    if is_busted(dealer.hand):
      print "Dealer has busted. You win!"
      player.chips += 2*bet


def hit(deck, hand):
  hand.append(deck.pop())


def is_busted(hand):
  return score(hand) > 21


def compare_scores(player, dealer, bet):
  if score(player.hand) > score(dealer.hand):
    print "You win!"
    player.chips += 2*bet
  elif score(player.hand) == score(dealer.hand):
    print "Push!"
    player.chips += bet
  else:
    print "Dealer wins."


def ask_to_deal_again(player, dealer):
  response = raw_input("Deal again? (Y/N) ")
  if response.upper() == 'Y':
    start_round(player, dealer)
  elif response.upper() == 'N':
    sys.exit()
  else:
    print "Please enter Y to deal again, or N to exit."
    ask_to_deal_again(player, dealer)


def ask_to_play_again():
  response = raw_input("Play again? (Y/N) ")
  if response.upper() == 'Y':
    initialize()
  elif response.upper() == 'N':
    sys.exit()
  else:
    print "Please enter Y to play again, or N to exit."
    ask_to_play_again()


initialize()
