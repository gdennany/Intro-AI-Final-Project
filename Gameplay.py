# B351 final project
# Author: Boqian Shi, Sophia Beneski, & Grant Dennany
# The basic structure and interface for the whole game


from Card import *
from Player import *
from Deck import *
from AI import *
from Winner import *
import os
from time import sleep



# define our clear screen function
def clear():
    os.system('cls')


class Gameplay:
    def __init__(self, player, ai):
        self.rounds = 0
        self.deck = Deck()
        self.middle_cards = []
        self.pot = 0
        self.player = player
        self.ai = ai
        self.min_bet = 20
        self.end = False
        self.my_bet = 0

    def check_balance(self):
        # True means game over, false means not
        if self.rounds % 2 == 0:
            if self.player.my_balance < 10:
                print("Game Over, AI wins")
                return True
            elif self.ai.my_balance < 20:
                print("Game Over, You win")
                return True
            else:
                return False
        else:
            if self.player.my_balance < 20:
                print("Game Over, AI wins")
                return True
            elif self.ai.my_balance < 10:
                print("Game Over, You win")
                return True
            else:
                return False

    def record_winner(self):
        # True means game over, false means not
        if self.rounds % 2 == 0:
            if self.player.my_balance < 10:
                # print("Game Over, AI wins")
                return 1
            elif self.ai.my_balance < 20:
                # print("Game Over, You win")
                return 0
        else:
            if self.player.my_balance < 20:
                # print("Game Over, AI wins")
                return 1
            elif self.ai.my_balance < 10:
                # print("Game Over, You win")
                return 0

    # Function that starts a new round
    def start_round(self):
        # ai first
        self.my_bet = 0
        self.ai.fold = False
        self.middle_cards = []
        self.end = False
        self.rounds += 1
        self.player.reset_cards()
        self.ai.reset_cards()
        self.min_bet = 20
        print("\n" * 100)
        print(f"Begin round {self.rounds}!")
        print("----------------------------")
        if self.check_balance():
            return
        self.start_game()
        self.turn_one()
        print()
        if not self.end:
            self.turn_two()
        print()
        if not self.end:
            self.turn_three()
            self.end_game()

    # Helper function that prints the player's card
    def show_mycard(self, player):
        # show my cards
        string = ""
        for card in player.my_card:
            string += (card.convert() + card.get_number())
            string += " "

        print("Your cards:" + "[ " + string + "]")

    # Helper function that prints ai's card
    def show_aicard(self, ai):
        # show my cards
        string = ""
        for card in ai.my_card:
            string += (card.convert() + card.get_number())
            string += " "

        print("AI cards:" + "[ " + string + "]")

    # helper function that prints middle cards
    def show_middle_cards(self):
        # show middle cards
        string = ""
        for card in self.middle_cards:
            string += (card.convert() + card.get_number())
            string += " "

        print("Middle cards:" + "[ " + string + "]")

    # After the round starts, initalize the game by
    # placing blind bets
    # deal cards to player and ai
    # put money in pot
    # deal middle cards
    def start_game(self):
        # print("Turn one:")
        print("The dealer deals you and the AI your initial two cards.\n")
        # give two cards to people
        card1 = self.deck.dealer()
        card2 = self.deck.dealer()
        self.player.init_cards(card1, card2)
        # self.show_mycard(self.player)
        card3 = self.deck.dealer()
        card4 = self.deck.dealer()
        self.ai.init_cards(card3, card4)
        # blind bets
        if self.rounds % 2 == 0:
            print("Automatic Small Blind of $10 placed by you.")
            print("Automatic Big Blind of $20 placed by the AI.")
            self.player.player_bet(10)
            self.ai.ai_bet(20)
        else:
            print("Automatic Small Blind of $10 placed by the AI.")
            print("Automatic Big Blind of $20 placed by you.")
            self.player.player_bet(20)
            self.ai.ai_bet(10)
        self.pot = 30
        print("\nPot: $30")
        print("Your balance: $" + str(self.player.my_balance))
        print(f"AI balance: ${self.ai.my_balance}")
        # deal the middle cards
        for i in range(0, 3):
            card = self.deck.dealer()
            self.middle_cards.append(card)
        print("\nThe Flop:")
        print("--------")
        self.show_middle_cards()
        self.show_mycard(self.player)
        self.ai.known_cards(self.middle_cards)
        self.ai.known_cards(self.ai.my_card)
        # print("Deck:")
        # self.deck.show_deck()

    # Helper function that let user raise the bets6
    def raise_bet(self, turns):
        extra = 0
        print()
        print("The minimum bet is $" + str(self.min_bet))
        print("Your Balance: $" + str(self.player.my_balance))
        bet = input("How much would you like to bet? ")
        print()
        while not bet.isdigit():
            print("Please input a number!")
            bet = input("How much would you like to bet? ")
        if int(bet) <= self.min_bet:
            print("The raise must be greater than $" + str(self.min_bet) + "!")
            self.raise_bet(turns)
        elif int(bet) > self.player.my_balance:
            print("You don't have enough money")
            self.raise_bet(turns)
        elif int(bet) == self.player.my_balance:
            # all in
            return
        else:
            self.min_bet = int(bet)
            self.my_bet = int(bet)
            self.player.player_bet(int(bet))
            self.pot += int(bet)
            print("\nBet of $" + bet + " placed")
            self.ai.already_raise = False
            if self.rounds % 2 == 1:
                extra = self.ai.after_raise(turns, self.middle_cards, self.min_bet)
                ai_bets = self.ai.add_pot()
                self.min_bet = ai_bets
                self.pot += extra
            if self.rounds % 2 == 0:
                self.ai.after_raise_second(turns, self.middle_cards, self.min_bet)
                ai_bets = self.ai.add_pot()
                self.min_bet = ai_bets
                self.pot += ai_bets
                '''
                if turns == 1:
                    self.pot += ai_bets
                elif turns == 2:
                    self.pot += 2 * ai_bets
                else:
                    self.pot += ai_bets
                '''
            if self.ai.already_raise is True:
                print("The AI raised the bet, so you must match the raise (call), re-raise, or fold.")
                self.after_raise(turns)

    def after_raise(self, turns):
        print(f"Pot {self.pot}")
        print("\nWhat would you like to do?:")
        print("1: Raise")
        print(f"2: Call (${self.min_bet})")
        print("3: Fold")
        option = input("Input a number above to make your choice: ")
        if option == "1":
            print("Min bet now is " + str(self.min_bet))
            print("You have: " + str(self.player.my_balance) + " dollars")
            print("You already put $" + str(self.my_bet) + " into pot this turn!")
            bet = input("How much would you like to bet this time? ")
            while not bet.isdigit():
                print("Please input a number!")
                bet = input("How much would you like to bet? ")
            if int(bet) + self.my_bet <= self.min_bet:
                print("Bet must be greater than " + str(self.min_bet - self.my_bet))
                self.after_raise(turns)
            elif int(bet) > self.player.my_balance:
                print("You don't have enough money")
                self.after_raise(turns)
            elif int(bet) == self.player.my_balance:
                # all in
                return
            else:
                self.min_bet = int(bet) + self.my_bet
                self.my_bet = int(bet) + self.my_bet
                self.player.player_bet(int(bet))
                self.pot += int(bet)
                print("Bet of $" + bet + " placed")
                self.ai.already_raise = False
                self.ai.after_raise(turns, self.middle_cards, self.min_bet)
                ai_bets = self.ai.reraise
                sub = self.ai.add_pot()
                self.min_bet = ai_bets
                self.pot += sub
                if self.ai.already_raise is True:
                    print("Since AI raise the bet again, you have to make choice again!")
                    self.after_raise(turns)
        elif option == "2":
            diff = self.min_bet - self.my_bet
            self.player.player_bet(diff)
            self.pot += diff
            self.my_bet = self.min_bet
            print("Bet of $" + str(self.min_bet) + " placed")
            self.ai.already_raise = False
        elif option == "3":
            self.fold()
        else:
            print()
            print("Please input a valid option!")
            if turns == 1:
                self.after_raise(1)
            elif turns == 2:
                self.after_raise(2)
            elif turns == 3:
                self.after_raise(3)

    # Helper function when player call this round
    def call_bet(self):
        self.player.player_bet(self.min_bet)
        self.pot += self.min_bet
        self.my_bet = self.min_bet
        print("Bet of $" + str(self.min_bet) + " placed")

    # Helper function when player fold this round
    def fold(self):
        # fold, should call the end_game
        self.end_game_fold(1)

    # Helper function to let player make the choice
    def choice(self, turns):
        # true for recrusively call
        print(f"\nPot: ${self.pot}")
        print("What would you like to do?:")
        print("1: Raise")
        print(f"2: Call (${self.min_bet})")
        print("3: Fold")
        option = ""
        result = -1
        option = input("Input a number above to make your choice: ")
        if option == "1":
            # raise the bet
            self.raise_bet(turns)
            return 1
        elif option == "2":
            self.call_bet()
            return 2
        elif option == "3":
            self.fold()
            return 3
        else:
            print()
            print("Please input a valid option!")
            if turns == 1:
                self.choice(1)
            elif turns == 2:
                self.choice(2)
            elif turns == 3:
                self.choice(3)

    # Processing turn one
    def turn_one(self):
        self.ai.already_raise = False
        self.ai.bet = 0
        self.ai.reraise = 0

        if self.rounds % 2 == 1:
            print("\nThe AI bets first this round.")
            self.ai.ai_turn_one(self.middle_cards, self.min_bet)
            ai_bets = self.ai.add_pot()
            self.min_bet = ai_bets
            self.pot += ai_bets
            # print(f"Pot: ${self.pot}")
            if self.ai.fold_helper() is True:
                self.end_game_fold(0)
                return

        if self.rounds % 2 == 0:
            print("\nYou bet first this round.")
        result = self.choice(1)
        if self.rounds % 2 == 0:
            # print(f"AI balance: {self.ai.my_balance}")
            # print(f"Pot: {self.pot}")
            # if result != 1:
            if result == 2:
                self.ai.ai_turn_one(self.middle_cards, self.min_bet)
                ai_bets = self.ai.add_pot()
                self.min_bet = ai_bets
                self.pot += ai_bets
            #
            # print(f"AI balance: {self.ai.my_balance}")
            print(f"Pot: ${self.pot}")
            if self.ai.fold_helper() is True:
                self.end_game_fold(0)
                return

            if self.ai.already_raise is True:
                if not self.end:
                    print("The AI raised the bet, so you must match the raise (call), re-raise, or fold.")
                    self.after_raise(1)

        # print("AI score now:")
        # print(self.ai.ai_score(self.middle_cards,1))

    # Processing turn two
    def turn_two(self):
        self.ai.bet = 0
        self.ai.reraise = 0
        self.ai.already_raise = False
        card = self.deck.dealer()
        self.middle_cards.append(card)
        cardlist = []
        cardlist.append(card)
        self.ai.known_cards(cardlist)
        print("\nThe Turn:")
        print("--------")
        print(f"Pot: ${self.pot}")
        self.show_middle_cards()
        self.show_mycard(self.player)
        # self.show_aicard(self.ai)
        # print("Score now:")
        # print(self.ai.ai_score(self.middle_cards,2))
        # print("Player potential score now:")
        # print(self.ai.player_score(self.middle_cards,2))
        if self.rounds % 2 == 1:
            # print("The AI bets first this round.")
            self.ai.ai_turn_two(self.middle_cards, self.min_bet)
            ai_bets = self.ai.add_pot()
            self.min_bet = ai_bets
            self.pot += ai_bets

        if self.ai.fold_helper() is True:
            self.end_game_fold(0)
            return

        # if self.rounds % 2 == 0:
        #    print("You bet first in this round.")
        result = self.choice(2)
        if self.rounds % 2 == 0:
            ##
            if result == 2:
                self.ai.ai_turn_two(self.middle_cards, self.min_bet)
                ai_bets = self.ai.add_pot()
                self.min_bet = ai_bets
                self.pot += ai_bets
            ##
            # if result == 1:
            # self.ai.my_balance += self.min_bet
            # self.pot += self.min_bet
            if self.ai.fold_helper() is True:
                self.end_game_fold(0)
                return

            if self.ai.already_raise is True:
                if not self.end:
                    print("The AI raised the bet, so you must match the raise (call), re-raise, or fold.")
                    self.after_raise(2)

    # processing the third turn
    def turn_three(self):
        self.ai.bet = 0
        self.ai.reraise = 0
        self.ai.already_raise = False
        card = self.deck.dealer()
        self.middle_cards.append(card)
        cardlist = []
        cardlist.append(card)
        self.ai.known_cards(cardlist)
        print("\nThe River:")
        print("---------")
        print(f"Pot: ${self.pot}")
        self.show_middle_cards()
        self.show_mycard(self.player)
        # self.show_aicard(self.ai)
        # print("Winning possibilities of ai:")
        # print(self.ai.winrate(self.middle_cards))
        if self.rounds % 2 == 1:
            # print("AI bet first in this turn!")
            self.ai.ai_turn_three(self.middle_cards, self.min_bet)
            ai_bets = self.ai.add_pot()
            self.min_bet = ai_bets
            self.pot += ai_bets

        if self.ai.fold_helper() is True:
            self.end_game_fold(0)
            return
        # if self.rounds % 2 == 0:
        #    print("You'll bet first in this turn!")
        result = self.choice(3)
        if self.rounds % 2 == 0:
            ##
            if result == 2:
                self.ai.ai_turn_three(self.middle_cards, self.min_bet)
                ai_bets = self.ai.add_pot()
                self.min_bet = ai_bets
                self.pot += ai_bets
            ##
            # self.ai.ai_turn_three(self.middle_cards,self.min_bet)
            if self.ai.fold_helper() is True:
                self.end_game_fold(0)
                return
            if self.ai.already_raise is True:
                if not self.end:
                    print("The AI raised the bet, so you must match the raise (call), re-raise, or fold.")
                    self.after_raise(3)

    # deal with the situation that somebody fold during the game
    def end_game_fold(self, winner):
        self.end = True
        # when winner is 1, AI win. when it's 0, player win
        if winner == 1:
            print()
            print(f"Since you folded, the AI wins the ${self.pot} pot in round {self.rounds}!")
            self.ai.my_balance += self.pot
            print(f"Your new balance: ${self.player.my_balance}.")
            print(f"AI's new balance ${self.ai.my_balance}.")
            self.pot = 0
        elif winner == 0:
            print()
            print(f"The AI folds, so you win the ${self.pot} pot in round {self.rounds}.")
            self.player.my_balance += self.pot
            print(f"Your new balance: ${self.player.my_balance}.")
            print(f"AI's new balance ${self.ai.my_balance}.")
            self.pot = 0
        else:
            raise Exception

    # shuffle the deck
    # should call every 5 rounds since 6> 52/9 > 5
    def shuffle(self):
        self.deck = Deck()
        self.ai.reset_known()

    # deal with the normal end game function
    # which will find the winner
    def end_game(self):
        if self.end is False:
            print(f"\n\n\nRound {self.rounds} Showdown:")
            print("---------------------------")
            print(f"Final pot value: ${self.pot}.")
            self.show_middle_cards()
            self.show_mycard(self.player)
            self.show_aicard(self.ai)
            print()
            winner = Winner(self.player.my_card, self.ai.my_card, self.middle_cards)
            print(winner)
            winner.findWinner()
            print("---------------------------")
            print(f"\n\nRound {self.rounds} Showdown Results:")
            print("---------------------------")
            if winner.return_number == 1:
                print(f"The AI wins the ${self.pot} pot!")
                self.ai.my_balance += self.pot
                print(f"Your new balance: ${self.player.my_balance}.")
                print(f"AI's new balance ${self.ai.my_balance}.")
                self.pot = 0
            elif winner.return_number == 0:
                print(f"You win the ${self.pot} pot")
                self.player.my_balance += self.pot
                print(f"Your new balance: ${self.player.my_balance}.")
                print(f"AI's new balance ${self.ai.my_balance}.")
                self.pot = 0
            elif winner.return_number == 2:
                print(f"Tie round, you and AI split the ${self.pot}")
                self.player.my_balance += self.pot / 2
                self.ai.my_balance += self.pot / 2
                print(f"Your new balance: ${self.player.my_balance}.")
                print(f"AI's new balance ${self.ai.my_balance}.")
                self.pot = 0
            else:
                raise Exception
            print("---------------------------")


def benckmark():
    rounds = 0
    aiwin = 0
    # Benchmark against with random ai
    player = Player()
    ai = AI()
    game = Gameplay(player, ai)
    for i in range(0, 100):
        if i == 5:
            print("The Dealer is shuffling the deck.")
            game.shuffle()
        if game.check_balance():
            aiwin += game.record_winner()
            break
        game.start_round()
    print(aiwin)
def play():
    player = Player()
    ai = AI()
    game=Gameplay(player,ai)
    allRounds = False
    print("\n" * 100)
    print("Welcome to the Texas Holdem Solver!\nPress Enter to continue.")
    input()
    for i in range(0,10):
        # 5 rounds then shuffle
        if i == 5:
            print("The Dealer is shuffling the deck.")
            game.shuffle()
        # when somebody don't have money, game end
        if game.check_balance():
            break
        game.start_round()
        # after every round ends, stop 5 seconds
        #sleep(5)
        print("\nPress Enter to continue to the next round")
        input()
        print("\n" * 100)
        # clear screen function, not work for Pycharm console
        #clear()
        print("After 10 rounds:")
        print(f"Your final balance: ${player.my_balance}")
        print(f"AI final balance: ${ai.my_balance}")

# main
if __name__ == '__main__':
    #benckmark()
    play()


