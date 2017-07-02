"""
This code was writen by Liubchenko Yurii as a test task for Provectus company.

Requirements to run: python 3.6+

There are present:
main - method that start main endless program loop.
Card - model used to save and represent cards.
GameManager - base logic that include:
    * methods that check combination(is_straight_flush, is_full_house,
                                     is_flush is_straight, is_identical, is_two_pairs);
    * base analyzer - get_best_hand that analyze and return best hand;
    * get_cardsets - method that generate all posible card sets;
    * print_cardsets - method that represent all posible card sets (using for debugging).
========================================================================================================================

Used combinations for testing:

    TH JH QC QD QS QH KH AH 2S 6S
    2H 2S 3H 3S 3C 2D 3D 6C 9C TH
    2H 2S 3H 3S 3C 2D 9C 3D 6C TH
    2H AD 5H AC 7H AH 6H 9H 4H 3C
    AC 2D 9C 3S KD 5S 4D KS AS 4C
    KS AH 2H 3C 4H KC 2C TC 2D AS
    AH 2C 9S AD 3C QH KS JS JD KD
    6C 9C 8C 2D 7C 2H TC 4C 9S AH
    3D 5S 2H QD TD 6S KH 9H AD QH

Results:

Hand: TH JH QC QD QS Deck: QH KH AH 2S 6S Best hand: straight-flush
Hand: 2H 2S 3H 3S 3C Deck: 2D 3D 6C 9C TH Best hand: four-of-a-kind
Hand: 2H 2S 3H 3S 3C Deck: 2D 9C 3D 6C TH Best hand: full-house
Hand: 2H AD 5H AC 7H Deck: AH 6H 9H 4H 3C Best hand: flush
Hand: AC 2D 9C 3S KD Deck: 5S 4D KS AS 4C Best hand: straight
Hand: KS AH 2H 3C 4H Deck: KC 2C TC 2D AS Best hand: three-of-a-kind
Hand: AH 2C 9S AD 3C Deck: QH KS JS JD KD Best hand: two-pairs
Hand: 6C 9C 8C 2D 7C Deck: 2H TC 4C 9S AH Best hand: one-pairs
Hand: 3D 5S 2H QD TD Deck: 6S KH 9H AD QH Best hand: highest-card
"""


SUIT = {'C': 1, 'D': 2, 'H': 3, 'S': 4}
VALUE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


class Card:
    def __init__(self, string):
        self.v = VALUE[string[0]]  # set value from dictionary.
        self.s = SUIT[string[1]]

    def __str__(self):
        card_suit = dict((v, k) for k, v in SUIT.items())  # get key using value from dict
        card_value = dict((v, k) for k, v in VALUE.items())
        return f'{card_value[self.v]}{card_suit[self.s]}'


class GameManager:
    def __init__(self, string):
        string = string.split()
        self.hand = [Card(card) for card in string[:5]]  # get 5 first items from list of strings named string
        self.deck = [Card(card) for card in string[5:]]
        self.cardset = self.get_cardsets()  # generate list of card sets.

    def __str__(self):
        # generate string from all str(Card) in list named hand.
        hand = " ".join(map(str, self.hand))
        deck = " ".join(map(str, self.deck))
        return f'Hand: {hand} Deck: {deck}'

    def is_straight_flush(self, hand):
        """
        Checks do the hand has straight-flash.
        :param hand: list of Card.
        :return: bool: Is card set straight_flash.
        """
        if self.is_straight(hand) and self.is_flush(hand):
            return True

    def is_full_house(self, hand):
        """
        Checks do the hand has full-house.
        :param hand: list of Card.
        :return: bool: Is card set straight_flash.
        """
        pairs = self.is_identical(hand, 2)  # Check pair
        three_identical = self.is_identical(hand, 3)  # Check three identical
        # Check that in pair not same cards as in three identical.
        if len(pairs) >= 1 and len(three_identical) >= 1 and pairs[0] != three_identical[0]:
            return True

    def is_flush(self, hand):
        """
        Checks do the hand has flush.
        :param hand: list of Card.
        :return: bool: Is card set straight_flash.
        """
        for i in hand:
            if hand[0].s != i.s:
                return False
        return True

    def is_straight(self, hand):
        """
        Checks do the hand has straight.
        :param hand: list of Card.
        :return: bool: Is card set straight_flash.
        """
        hand = sorted(hand, key=lambda x: x.v)
        if [card.v for card in hand] ==[2, 3, 4, 5, 14]:
            return True
        # Check spacial combination Ace, 2, 3, 4, 5
        for i in range(len(hand)-1):
            if hand[i+1].v-hand[i].v != 1:
                return False
        return True

    def is_identical(self, hand, count):
        """
        Checks do the hand has some count of identical cards.
        :param hand: list of Card.
        :param count: how many cards of the same value needed.
        :return bool: Is card set straight_flash.
        """
        return [v for v in VALUE.values() if [card.v for card in hand].count(v) == count]

    def is_two_pairs(self, hand):
        """
        Checks do the hand has 2 pairs.
        :param hand: list of Card.
        :return bool: Is card set straight_flash.
        """
        pairs = self.is_identical(hand, 2)
        if len(pairs) >= 2:
            return pairs

    def get_cardsets(self):
        """
        Get all possible list of cards.
        :return: list of card set (list of possible lists of cards)
        """
        cardset = []
        for i in range(1, 33):
            cards = []
            if i % 2 == 0:
                cards.append(self.hand[4])
            if i % 4 == 0 or i % 4 == 3:
                cards.append(self.hand[3])
            if i % 8 > 4 or i % 8 == 0:
                cards.append(self.hand[2])
            if i in range(8, 16) or i > 24:
                cards.append(self.hand[1])
            if i > 16:
                cards.append(self.hand[0])
            deck = self.deck.copy()[::-1]
            while len(cards) < 5:
                cards.append(deck.pop())
            cardset.append(cards)
        return cardset

    def print_cardsets(self):
        """
        Print list of card set in string format.
        """
        print('\nCARD SETS:')
        suit = {1: 'C', 2: 'D', 3: 'H', 4: 'S'}
        value = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q', 13: 'K',
                 14: 'A'}
        for i in self.cardset:
             print(' '.join([k[0]+k[1] for k in [(value[j[0]], suit[j[1]]) for j in [(card.v, card.s) for card in i]]]))

    def get_best_hand(self):
        """
        Main analyze controller, that analyze card sets.
        :return: The best card set (list of objects Card) from list of possible list of card sets.
        """
        combinations = {8: (lambda hand: self.is_straight_flush(hand), 'straight-flush'),
                        7: (lambda hand: self.is_identical(hand, 4), 'four-of-a-kind'),
                        6: (lambda hand: self.is_full_house(hand), 'full-house'),
                        5: (lambda hand: self.is_flush(hand), 'flush'),
                        4: (lambda hand: self.is_straight(hand), 'straight'),
                        3: (lambda hand: self.is_identical(hand, 3), 'three-of-a-kind'),
                        2: (lambda hand: self.is_two_pairs(hand), 'two-pairs'),
                        1: (lambda hand: self.is_identical(hand, 2), 'one-pairs')}

        combination_id = 0

        # Get the best combination from all possible cardset and write combination id into variable.
        for cards in self.cardset:
            for k, v in combinations.items():
                if v[0](cards) and combination_id < k:
                    combination_id = k
                    break

        # If we haven't any combination, return highest-card.
        if combination_id == 0:
            return 'Best hand: highest-card'
        return f'Best hand: {combinations[combination_id][1]}'


def main():
    """
    Main program loop that input card set and output Hand, Deck, and Best hand.
    """
    while True:
        cards = input()

        # There we check our input, if it wrong - we output error massage, and continue running loop.
        try:
            gm = GameManager(cards)
        except KeyError:
            print('Wrong input!')
            continue
        print(f"{gm} {gm.get_best_hand()}")
        # gm.print_cardsets() # Use this for represent card sets.


if __name__ == "__main__":
    main()
