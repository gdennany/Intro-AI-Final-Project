# B351 final project
# Author: Boqian Shi, Sophia Beneski, & Grant Dennany
# This class is the structure of the card

class Card:

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    # return the number of this card
    def get_number(self):
        return self.number

    # return the suit of this card
    def get_suit(self):
        return self.suit

    # convert the card to the UTF-9 code
    def convert(self):
        s = self.get_suit()
        if (s == 'Diamonds'):
            return '\u2666'
        if (s == 'Hearts'):
            return '\u2665'
        if (s == 'Spades'):
            return '\u2660'
        if (s == 'Clubs'):
            return '\u2663'

    # edit: I added this so you can just call print(card) instead of (card.convert()+card.get_number()) every time
    def __str__(self):
        return (self.convert()+" "+self.get_number())
