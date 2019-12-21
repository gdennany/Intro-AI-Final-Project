# B351 final project
# Author: Boqian Shi, Sophia Beneski, & Grant Dennany
# The class is about the strategy of our ai

from Card import *
from Gameplay import *
from Deck import *
from Player import *
from Winner import *
# Basic algorithm of our ai is in this class
class AI:
    def __init__(self):
        self.my_card = []
        self.my_balance = 500
        # self.known is the list that store the cards already known by AI
        self.known = []
        # self.unknown is the unknown card list(which include cards never shown and cards in player's hand)
        self.unknown = Deck()
        self.bet = 0
        self.fold = False
        self.already_raise = False
        # self.confidence_bias = 0.75
        self.reraise = 0

    # when AI bet, decrease the balance
    def ai_bet(self, bet):
        self.my_balance -= bet

    # deal cards to ai
    def init_cards(self, card1, card2):
        self.my_card.append(card1)
        self.my_card.append(card2)

    # when ai know some card, delete it from the unknown list and add it to known list.
    def known_cards(self, card_list):
        for card in card_list:
            self.known.append(card)
            self.unknown.remove(card)

    # reset the list of known and unknown after 5 rounds are passed and shuffle the Deck.
    def reset_known(self):
        self.known = []
        self.unknown = Deck()

    # evaluating AI's winning score for first 2 turns
    # the score is the sum of
    # the score for each possible winning hands
    # multiply the possibility of get this hand based on the unknown list
    # Score = Score for each possible winning hands * P(hands | current cards)
    def ai_score(self, middle_cards, turns):
        hands = []
        total_score = 0

        number_of_unknown = len(self.unknown.deck)
        if turns == 1:
            for m in middle_cards:
                hands.append(m)
            for a in self.my_card:
                hands.append(a)
            for i in self.unknown.deck:
                for j in self.unknown.deck:
                    if i is j:
                        break
                    hands.append(i)
                    hands.append(j)
                    total_score = total_score + (self.score(hands) / ((number_of_unknown - 1) * number_of_unknown))
                    hands.remove(i)
                    hands.remove(j)
        if turns == 2:
            for m in middle_cards:
                hands.append(m)
            for a in self.my_card:
                hands.append(a)
            for unk in self.unknown.deck:
                hands.append(unk)
                total_score = total_score + self.score(hands) / number_of_unknown
                hands.remove(unk)
        return total_score

    # evaluating player's score
    # similar with the ai's score
    # only differences: simulating player's two cards in this part also
    # so it's 4 cards unknown for first round
    # 4 cards will take very long time, so we only use this for second round
    # 3 cards unknown for second round
    def player_score(self, middle_cards):
        hands = []
        total_score = 0
        dynamic_list = []
        n = 0
        for m in middle_cards:
            hands.append(m)
        for i in self.unknown.deck:
            for j in self.unknown.deck:
                if j != i:
                    for m in self.unknown.deck:
                        if m != i and m != j:
                            tu = (i, j, m)
                            bool = True
                            for ele in dynamic_list:
                                if i in ele and j in ele and m in ele:
                                    bool = False
                            if bool == True:
                                dynamic_list.append(tu)
                                n += 1
                            else:
                                break
                            hands.append(i)
                            hands.append(j)
                            hands.append(m)
                            total_score = total_score + self.score(hands)
                            hands.remove(i)
                            hands.remove(j)
                            hands.remove(m)
        total_score = total_score / len(dynamic_list)
        return total_score

    # return the score of hands by call the function in winner
    def score(self, cards):
        w = Winner([], [], [])
        best = w.GetBestHand(cards)[1]
        return w.evaluate_score(best)

    # For final round:
    # based on ai's card
    # evaluating the possibilities of win the game
    # will make decision based on this winrate
    # P(AI win) =
    # # of hands that AI win the game / # of all combinations of hands
    # **********Core Function***********
    def winrate(self, middle_cards):
        # most important part--ai's winning probabilities
        aiwin = 0
        playerwin = 0
        aihands = []
        playerhands = []
        for ai in self.my_card:
            aihands.append(ai)
        for m in middle_cards:
            playerhands.append(m)
            aihands.append(m)
        for i in self.unknown.deck:
            for j in self.unknown.deck:
                playerhands.append(i)
                playerhands.append(j)
                winner = Winner([], [], [])
                aiscore = winner.GetBestHand(aihands)[0]
                playerscore = winner.GetBestHand(playerhands)[0]
                AIBestCards = winner.GetBestHand(aihands)[1]
                playerBestCards = winner.GetBestHand(playerhands)[1]
                if aiscore > playerscore:
                    # print("aiwin!")
                    aiwin += 1
                elif aiscore == playerscore:
                    tieBreak = winner.tie_breaker(list(playerBestCards), list(AIBestCards),aiscore)
                    if tieBreak[1] == 1:
                        playerwin += 1
                    elif tieBreak[1] == 2:
                        aiwin += 1
                elif aiscore < playerscore:
                    # print("playerwin")
                    playerwin += 1
                playerhands.remove(i)
                playerhands.remove(j)
                # print(aiwin)
                # print(playerwin)
        return aiwin / (aiwin + playerwin)

    # reset the cards of ai
    def reset_cards(self):
        self.my_card = []

    # Helper function to let ai raise the bets
    def ai_raise(self, turns, min_bet):
        # when the min_bet now is higher than ai's balance
        # bet amount equals to balance
        if min_bet >= self.my_balance:
            min_bet = self.my_balance

        # Theoretically, ai shouldn't raise the bets on the first turn
        # But when the card is very good, it should be able to raise on the first turn
        if turns == 1:
            self.ai_bet(min_bet + 10)
            print(f"\nThe AI raised the bet to ${min_bet + 10}!")
            self.bet = min_bet + 10

        # for the second turn
        if turns == 2:
            self.ai_bet(min_bet + 10)
            print(f"\nThe AI raised the bet to ${min_bet + 10}!")
            self.bet = min_bet + 10

        if turns == 3:
            self.ai_bet(min_bet + 30)
            print(f"\nThe AI raised the bet to ${min_bet + 30}!")
            self.bet = min_bet + 30
        self.already_raise = True

    # A helper function deal with ai's raise after PLAYER raise the bets
    def raise_after_raise(self,turns,min_bet):
        if turns == 1:
            self.ai_bet(min_bet + 10 - self.bet)
            print(f"\nThe AI raised the bet to ${min_bet + 10},by putting ${min_bet + 10 - self.bet} more into the pot!")
            self.bet = min_bet + 10 - self.bet
            self.reraise = min_bet + 10

        # for the second turn
        if turns == 2:
            self.ai_bet(min_bet + 10 - self.bet)
            print(f"The AI raised the bet to ${min_bet + 10} by putting extra ${min_bet + 10 - self.bet}!")
            self.bet = min_bet + 10 - self.bet
            self.reraise = min_bet + 10

        if turns == 3:
            self.ai_bet(min_bet + 30 - self.bet)
            print(f"The AI raised the bet to ${min_bet + 30} by putting extra ${min_bet + 10 - self.bet}!")
            self.bet = min_bet + 30 - self.bet
            self.reraise = min_bet + 30
        self.already_raise = True

    # A helper function deal with ai's call after PLAYER raise the bets
    def call_after_raise(self,min_bet):
        self.ai_bet(min_bet-self.bet)
        print(f"AI matches the raise to ${min_bet}!") #(By putting ${min_bet-self.bet} more into the pot.)")
        sub = min_bet - self.bet
        #self.bet = min_bet-self.bet
        #self.bet = min_bet
        self.bet += sub
        return sub
        #self.add_pot(0 - sub + min_bet)
        #self.bet

    def call_after_raise_second(self, min_bet):
        self.ai_bet(min_bet - self.bet)
        print(f"AI matches the raise to ${min_bet}!")
        self.bet = min_bet
        return min_bet

    # A helper function deal with the situation after PLAYER raise the bets
    def after_raise(self,turns,middle,min_bet):
        extra = 0
        if turns == 1:
            score_ai = self.ai_score(middle, 1)
            #if score_ai >= 30:
            #    self.raise_after_raise(1,min_bet)
            if score_ai < 1.1:
                self.fold = True
            else:
                extra =  self.call_after_raise(min_bet)
        if turns == 2:
            score_ai = self.ai_score(middle, 2)
            score_player = self.player_score(middle)
            compare = score_ai / score_player
            #if compare >= 4:
            #    self.raise_after_raise(2, min_bet)
            if compare < .1:
                self.fold = True
            else:
                #self.call_after_raise(min_bet)
                extra =  self.call_after_raise(min_bet)
        if turns == 3:
            rate = self.winrate(middle)
            #if rate >= 0.8:
            #    self.raise_after_raise(3, min_bet)
            if rate < 0.45:
                self.fold = True
            else:
                extra =  self.call_after_raise(min_bet)
        return extra

    def after_raise_second(self, turns, middle, min_bet):
        extra = 0
        if turns == 1:
            score_ai = self.ai_score(middle, 1)
            #if score_ai >= 30:
            #    self.raise_after_raise(1,min_bet)
            if score_ai < 1.1:
                self.fold = True
            else:
                extra = self.call_after_raise(min_bet)
        if turns == 2:
            extra = 0
            score_ai = self.ai_score(middle, 2)
            score_player = self.player_score(middle)
            compare = score_ai / score_player
            #if compare >= 4:
            #    self.raise_after_raise(2, min_bet)
            if compare < .1:
                self.fold = True
            else:
                #self.call_after_raise(min_bet)
                extra = self.call_after_raise(min_bet)
        if turns == 3:
            rate = self.winrate(middle)
            #if rate >= 0.8:
            #    self.raise_after_raise(3, min_bet)
            if rate < 0.45:
                self.fold = True
            else:
                extra = self.call_after_raise(min_bet)
        return extra

    # Helper function to let ai call the bets
    def ai_call(self, turns, min_bet):
        self.ai_bet(min_bet)
        print(f"\nAI calls the bet. (${min_bet})")
        self.bet = min_bet

    # Helper function to let ai fold
    def fold_helper(self):
        # fold function
        return self.fold

    # A helper function to let ai's bets are going to pot
    def add_pot(self):
        return self.bet


    def ai_turn_one(self,middle,min_bet):
        score_ai = self.ai_score(middle, 1)
        if score_ai >= 30:
            self.ai_raise(1,min_bet)
        elif score_ai < 1.1:
            print("The AI folds.")
            self.fold = True
        else:
            self.ai_call(1, min_bet)

    def ai_turn_two(self,middle_cards, min_bet):
        print()
        print("AI is considering its cards...Please wait...")
        print()
        score_ai = self.ai_score(middle_cards, 2)
        score_player = self.player_score(middle_cards)
        compare = score_ai / score_player
        if compare >= 2:
            self.ai_raise(2, min_bet)
        elif compare < 0.1:
            print("The AI folds.")
            self.fold = True
        else:
            self.ai_call(2, min_bet)


    def ai_turn_three(self,middle_cards,min_bet):
        rate = self.winrate(middle_cards)
        if rate >= 0.79:
            self.ai_raise(3, min_bet)
        elif rate <= 0.35:
            print("The AI folds.")
            self.fold = True
        else:
            self.ai_call(3, min_bet)