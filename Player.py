# B351 final project
# Author: Boqian Shi, Sophia Beneski, & Grant Dennany
# The class is the basic structure of player

class Player:
    def __init__(self):
        self.my_card=[]
        self.my_balance = 500

    # when player bet, decrease the balance
    def player_bet(self,bet):
        self.my_balance -= bet

    # send two cards to player
    def init_cards(self,card1,card2):
        self.my_card.append(card1)
        self.my_card.append(card2)

    # reset my_card to empty
    def reset_cards(self):
        self.my_card = []
