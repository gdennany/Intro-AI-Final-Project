# B351 final project
# Author: Boqian Shi, Sophia Beneski, & Grant Dennany
# Test cases

from Card import *
from Deck import *
from Winner import *

class Tests:

    def test_check_royal_flush(self):
        testDeck = Deck()
        card1 = Card('A', 'Spades')
        card2 = Card('K', 'Spades')
        card3 = Card('Q', 'Spades')
        card4 = Card('J', 'Spades')
        card5 = Card('10', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)

    def test_check_straight_flush(self):
        testDeck = Deck()
        card1 = Card('J', 'Spades')
        card2 = Card('Q', 'Spades')
        card3 = Card('10', 'Spades')
        card4 = Card('K', 'Spades')
        card5 = Card('9', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)


    def test_check_four_of_kind(self):
        testDeck = Deck()
        card1 = Card('7', 'Spades')
        card2 = Card('7', 'Diamonds')
        card3 = Card('7', 'Clubs')
        card4 = Card('7', 'Hearts')
        card5 = Card('9', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)

    def test_check_full_house(self):
        testDeck = Deck()
        card1 = Card('A', 'Spades')
        card2 = Card('A', 'Clubs')
        card3 = Card('6', 'Clubs')
        card4 = Card('6', 'Spades')
        card5 = Card('6', 'Diamonds')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)
        print(winner)

    def test_check_flush(self):
        testDeck = Deck()
        card1 = Card('2', 'Spades')
        card2 = Card('K', 'Spades')
        card3 = Card('Q', 'Spades')
        card4 = Card('J', 'Spades')
        card5 = Card('10', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)
    
    def test_check_straight(self):
        testDeck = Deck()
        card1 = Card('2', 'Spades')
        card2 = Card('3', 'Hearts')
        card3 = Card('4', 'Diamonds')
        card4 = Card('5', 'Clubs')
        card5 = Card('6', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)

    def test_check_three_of_kind(self):
        testDeck = Deck()
        card1 = Card('2', 'Spades')
        card2 = Card('3', 'Hearts')
        card3 = Card('K', 'Diamonds')
        card4 = Card('K', 'Clubs')
        card5 = Card('K', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)
    
    def test_check_two_pair(self):
        testDeck = Deck()
        card1 = Card('A', 'Spades')
        card2 = Card('A', 'Hearts')
        card3 = Card('4', 'Diamonds')
        card4 = Card('4', 'Clubs')
        card5 = Card('6', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)
    
    def test_check_one_pair(self):
        testDeck = Deck()
        card1 = Card('A', 'Spades')
        card2 = Card('A', 'Hearts')
        card3 = Card('4', 'Diamonds')
        card4 = Card('5', 'Clubs')
        card5 = Card('6', 'Spades')
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5]
        winner = Winner(playerCards, AICards, middleCards)

    def test_check_high_card(self):
        testDeck = Deck()
        card1 = Card('K', 'Diamonds')
        card2 = Card('6', 'Hearts')
        card3 = Card('Q', 'Spades')
        card4 = Card('A', 'Hearts')
        card5 = Card('8', 'Hearts')
        card6 = Card('J', 'Hearts')
        card7 = Card('8', 'Spades')
        card8 = Card('5', 'Diamonds')
        card9 = Card('K', 'Hearts')
        #card6 = testDeck.dealer()
        #card7 = testDeck.dealer()
        #card8 = testDeck.dealer()
        #card9 = testDeck.dealer()

        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5, card8, card9]
        winner = Winner(playerCards, AICards, middleCards)
        print(winner)

    def test_random_cards(self):
        testDeck = Deck()
        card1 = testDeck.dealer()
        card2 = testDeck.dealer()
        card3 = testDeck.dealer()
        card4 = testDeck.dealer()
        card5 = testDeck.dealer()
        card6 = testDeck.dealer()
        card7 = testDeck.dealer()
        card8 = testDeck.dealer()
        card9 = testDeck.dealer()
        AICards = [card6, card7]
        playerCards = [card1, card2]
        middleCards = [card3, card4, card5, card8, card9]
        winner = Winner(playerCards, AICards, middleCards)
        #print(winner.findWinner())
        print(winner)

    def test_tie_breaker(self):
        testDeck = Deck()
        card1 = Card('4', 'Spades')
        card2 = Card('3', 'Hearts')
        card3 = Card('2', 'Diamonds')
        card4 = Card('3', 'Clubs')
        card5 = Card('7', 'Diamonds')
        card6 = Card('6', 'Clubs')
        card7 = Card('J', 'Spades')

        AICards = [card1, card2]
        playerCards = [card3, card4]
        middleCards = [card5, card6, card7]
        winner = Winner(playerCards, AICards, middleCards)
        print(winner)
        print('--------')
        for card in middleCards:
            AICards.append(card)
            playerCards.append(card)
        print(winner.tie_breaker(playerCards, AICards))




if __name__ == '__main__':
    
    d = Tests()

## Tests for Winner.py
    #d.test_check_royal_flush()
    #d.test_check_straight_flush()
    #d.test_check_four_of_kind()
    #d.test_check_full_house()
    #d.test_check_flush()
    #d.test_check_straight()
    #d.test_check_three_of_kind()
    #d.test_check_two_pair()
    #d.test_check_one_pair()
    d.test_check_high_card()
    #d.test_random_cards()
    #d.test_tie_breaker()