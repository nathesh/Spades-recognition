from cardrecognition import get_cards
from helper import letter_to_suit, letter_to_number, card_value
# from collections import namedtuple
# Note that 1 and 3 are a team and 2 and 4 are team


class Round:

    used_cards = {}
    unavailable_suits = {1: [], 2: [], 3: [], 4: []}  # assume this for the each player...
    spades_broken = False
    bids = []

    def __init__(self):
        self.round_cards = {}
        self.round_suit = None

    def start(self, player_num, first_round):

        if first_round == 1:
            self._get_bids()

        cards_played = []
        for i in range(4):

            player_num = (player_num + i) % 4 if (player_num + i) != 4 else 4
            print "Player {0} please play your card".format(player_num)

            #case if more than necessary cards played or (*, *) is returned
            while len(cards_played) <= (i + 1):
                cards_played = get_cards()

            card = self._get_new_card(cards_played)

            if card.suit == '*' or card.num == '*':
                print "can't recognize card, restarting round"
                return 0
            elif self._invalid_play(card, player_num, self.round_suit is None):
                    print "Invalid Move, 40pt Penalty, Ending play"
                    return 0
            else:
                self.round_cards[card] = player_num
                if not self.round_suit:
                    self.round_suit = card.suit
                    print "The suit of the Round is ", letter_to_suit[card.suit]
                if card.suit == "S" and not Round.spades_broken:
                    print "Spades is Broken!"
                if self.round_suit != card.suit:
                    print "Player {0} doesn't have {1}".format(player_num, letter_to_suit(self.round_suit))
                    Round.unavailable_suits[player_num].append(card.suit)
                Round.used_cards[card] = True
                print "Player {0} played {1} of {2}".format(
                    player_num, letter_to_suit[card.suit],
                    letter_to_number[card.number])

        return self._round_winner(cards_played)

    def _get_new_card(self, cards_played):
        for i in len(cards_played):
            if not self.round_cards.containsKey(cards_played[i]):
                return cards_played[i]

    def _invalid_play(self, card, player_num, check_spades):
        # Check if player played a valid suit ?! Can't check this he might not have suit.
        # Check if the first player played spades when spades was not broken
        # Check if a used card was played
        if card.suit in Round.unavailable_suits[player_num]:
            return True
        elif check_spades and card.suit == "S" and not Round.spades_broken:
            print "Played Spades"
            return True
        elif Round.used_cards[card]:
            return True
        return False

    def _round_winner(self):
        #use variable round_suit to determine who one
        #return player numer
        maxcard = self.round_cards.keys()[0]
        for card in self.round_cards:
            if card.suit == "S":
                if maxcard.suit == "S":
                    if card_value(card) > card_value(maxcard):
                        maxcard = card
                else:
                    maxcard = card
            elif card.suit == self.round_suit and maxcard.suit != "S":
                if card_value(card) > card_value(maxcard):
                    maxcard = card
        return self.round_cards[maxcard]

    def _get_bids(self):
        for i in range(4):
            print 'Player {0} enter bid'.format(i + 1)
            bid = raw_input()
            while not bid.isdigit():
                print 'Please enter a number'
                bid = raw_input()
            Round.bids.append(bid)

if __name__ == '__main__':
    Rounds = Round()
    wins = {1: 0, 2: 0, 3: 0, 4: 0}
    points_A = 0
    points_B = 0
    bags_A = 0
    bags_B = 0
    while(points_A or points_B < 500):
        for Hand in range(13):
            player_num = Hand % 4 + 1
            winner = Round.start(player_num, Hand + 1)
            wins[winner] = wins[winner] + 1
        combined_bid_A = Rounds.bids[0] + Rounds.bids[2]
        combined_bid_B = Rounds.bids[1] + Rounds.bids[3]
        combined_tricks_A = wins[0] + wins[2]
        combined_tricks_B = wins[1] + wins[3]

        # For Team A Calculation
        if combined_bid_A > combined_tricks_A:
            points_A -= combined_bid_A * 10
        if combined_bid_A <= combined_tricks_A:
            points_A += combined_bid_A * 10 + (combined_tricks_A - combined_bid_A)
            bags_A = (combined_tricks_A - combined_bid_A)
        if Rounds.bids[0] == 0:
            points_A = points_A + 100 if wins[0] == 0 else points_A - 100
        if Rounds.bids[2] == 0:
            points_A = points_A + 100 if wins[2] == 0 else points_A - 100
        if bags_A >= 10:
            points_A -= 100
            bags_A -= 10

        # For Team B Calculation
        if combined_bid_B > combined_tricks_B:
            points_B -= combined_bid_B * 10
        if combined_bid_B <= combined_tricks_B:
            points_B += combined_bid_B * 10 + (combined_tricks_B - combined_bid_B)
            bags_B = combined_tricks_B - combined_bid_B
        if Rounds.bids[0] == 0:
            points_B = points_B + 100 if wins[1] == 0 else points_B - 100
        if Rounds.bids[2] == 0:
            points_B = points_B + 100 if wins[3] == 0 else points_B - 100
        if bags_B >= 10:
            points_B -= 100
            bags_B -= 10
