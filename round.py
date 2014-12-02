from cardrecognition import get_cards, Card
from helper import letter_to_suit, letter_to_number, card_value
# from collections import namedtuple
# Note that 1 and 3 are a team and 2 and 4 are team


class Round:

    def __init__(self):
        self.used_cards = []
        self.unavailable_suits = {1: [], 2: [], 3: [], 4: []}  # assume this for the each player...
        self.spades_broken = False
        self.bids = []
        self.round_cards = {}
        self.round_suit = None

    def start(self, player_num, first_round):

        if first_round == 1:
            self._get_bids()

        cards_played = []
        self.round_cards = {}
        self.round_suit = None
        for i in range(4):
            print "********************************"
            print "Player {0} please play your card".format(player_num)

            #case if more than necessary cards played or (*, *) is returned
            card = None
            while not card or card.suit == '*' or card.number == '*':
                cards_played = get_cards(i + 1)
                card = self._get_new_card(cards_played)

            if self._invalid_play(card, player_num, self.round_suit is None):
                    print "Invalid Move, 40pt Penalty, Ending play"
                    return player_num * -1
            else:
                self.round_cards[card] = player_num
                if not self.round_suit:
                    self.round_suit = card.suit
                    print "The suit of the Round is", letter_to_suit(card.suit)
                if card.suit == "S" and not self.spades_broken:
                    print "Spades is Broken!"
                    self.spades_broken = True
                if self.round_suit != card.suit:
                    print "Player {0} doesn't have {1}".format(player_num, letter_to_suit(self.round_suit))
                    self.unavailable_suits[player_num].append(self.round_suit)
                self.used_cards.append(card)
                print "Player {0} played {1} of {2}".format(
                    player_num, letter_to_number(card.number),
                    letter_to_suit(card.suit))

            player_num = (player_num + 1) % 4 if (player_num + 1) != 4 else 4

        winner = self._round_winner()
        print "Player {0} wins the trick".format(winner)

        #Print winning team
        # print "Team B won, Team A: {0}, Team B: {1}".format(points_A, points_B)

        #wait for players to remove cards from the table
        while cards_played and not (card.suit == '*' or card.number == '*'):
            cards_played = get_cards(1)

        return winner

    def _get_new_card(self, cards_played):
        for i in range(len(cards_played)):
            if cards_played[i] not in self.round_cards.keys():
                return cards_played[i]
        return None

    def _invalid_play(self, card, player_num, check_spades):
        # Check if player played a valid suit ?! Can't check this he might not have suit.
        # Check if the first player played spades when spades was not broken
        # Check if a used card was played
        if card.suit in self.unavailable_suits[player_num]:
            print "Player should not have any {0} remaining".format(card.suit)
            return True
        elif check_spades and card.suit == "S" and not self.spades_broken:
            print "Played Spades"
            return True
        elif card in self.used_cards:
            print "Played a used card"
            return True
        return False

    def _round_winner(self):
        #use variable round_suit to determine who one
        #return player numer
        maxcard = Card('0', self.round_suit)
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
            self.bids.append(bid)

if __name__ == '__main__':
    wins = {1: 0, 2: 0, 3: 0, 4: 0}
    points_A = 0
    points_B = 0
    bags_A = 0
    bags_B = 0
    winner = 1
    dealer = 0

    while(points_A < 50 or points_B < 50):
        dealer = (dealer + 1) % 4 if (dealer + 1) != 4 else 4
        winner = dealer
        r = Round()
        hand = 0
        while hand < 13:
            result = r.start(winner, hand + 1)
            if result == 0:  # error. re-play the round
                continue
            elif result < 0:  # penalty
                penalty = True
                break
            winner = result
            wins[winner] = wins[winner] + 1
            hand += 1

        if penalty:
            print result
            if result == -1 or result == -3:
                points_A += 40
            else:
                points_B += 40

            print "**********************************"
            print "End of round score:"
            print "\t TEAM A = {0}".format(points_A)
            print "\t TEAM B = {0}".format(points_B)
            print "**********************************"

            continue

        combined_bid_A = r.bids[0] + r.bids[2]
        combined_bid_B = r.bids[1] + r.bids[3]
        combined_tricks_A = wins[0] + wins[2]
        combined_tricks_B = wins[1] + wins[3]

        # For Team A Calculation
        if combined_bid_A > combined_tricks_A:
            points_A -= combined_bid_A * 10
        elif combined_bid_A <= combined_tricks_A:
            points_A += combined_bid_A * 10 + (combined_tricks_A - combined_bid_A)
            bags_A += (combined_tricks_A - combined_bid_A)
        if r.bids[0] == 0:
            points_A = points_A + 100 if wins[0] == 0 else points_A - 100
        if r.bids[2] == 0:
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
        if r.bids[0] == 0:
            points_B = points_B + 100 if wins[1] == 0 else points_B - 100
        if r.bids[2] == 0:
            points_B = points_B + 100 if wins[3] == 0 else points_B - 100
        if bags_B >= 10:
            points_B -= 100
            bags_B -= 10

        #Print end of round score
        print "**********************************"
        for i in range(4):
            print "Player {0} bid {1} and made {2} tricks".format(i + 1, r.bids[i], wins[i])
        print
        print "End of round score:"
        print "\t TEAM A = {0}".format(points_A)
        print "\t TEAM B = {0}".format(points_B)
        print "**********************************"

    #Print winning team
    if points_A > 500:
        print "Team B won, Team A: {0}, Team B: {1}".format(points_A, points_B)
    else:
        print "Team A won, Team A: {0}, Team B: {1}".format(points_A, points_B)
