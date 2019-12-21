# B351 final project
# Author: Boqian Shi, Sophia Beneski, & Grant Dennany
# The Deck is a list of card

from Card import *
import random


# comparing of cards
def same(c1, c2):
    if c1.get_number() == c2.get_number():
        if c1.get_suit() == c2.get_suit():
            return True
    return False


class Deck:
    # universal variable of numbers and suits
    numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']

    def __init__(self):
        self.deck = []
        # put all the combinations of suits and numbers into the deck
        for number in self.numbers:
            for suit in self.suits:
                card = Card(number, suit)
                self.deck.append(card)

    # randomly select a card from the deck
    def random(self):
        return random.choice(self.deck)

    # check the card is in the Deck or not
    def check(self, input_card):
        for i in self.deck:
            if same(input_card, i):
                return True
        return False

    # remove a card from the deck
    def remove(self, card):
        for i in self.deck:
            if same(card, i):
                self.deck.remove(i)

    # randomly pick and remove a card from the deck, then return it
    def dealer(self):
        card = self.random()
        self.remove(card)
        return card

    # print all the cards are still in the deck
    def show_deck(self):
        for card in self.deck:
            print(card.convert() + card.get_number())


'''
if __name__ == '__main__':
    d = Deck()
    card = Card('K', 'Diamonds')
    d.remove(card)
    d.show_deck()
'''
