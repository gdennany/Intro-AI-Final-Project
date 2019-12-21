# B351 final project
# Author: Boqian Shi, Sophia Beneski, & Grant Dennany
# Basic game rules and the function find the winner
from itertools import combinations

class Winner:
    '''
    Takes 3 input lists: playerCards AICards, and middleCards and determines the winner
    example use: 
        winner = Winner(playerCards, AICards, middleCards)
        print(winner) -> prints who won and each players hand
        winner.findWinner() -> returns "Player" if the human won or "AI" if the ai won
    '''

    bestHands = {
        10 : "Royal Flush",
        9 : "Staight Flush",
        8 : "Four of a Kind",
        7 : "Full House",
        6 : "Flush",
        5 : "Straight",
        4 : "Three of a Kind",
        3 : "Two Pair",
        2 : "One Pair",
        1 : "High Card"
    }

    numbers = {'2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'J' : 11, 'Q' : 12, 'K' : 13, 'A' : 14}
    suits = {'Diamonds' : 1, 'Hearts' : 2, 'Spades' : 3, 'Clubs' : 4}

    def __init__(self, playerCards, AICards, middleCards):
        self.playerCards = playerCards
        self.AICards = AICards
        self.middleCards = middleCards
        self.return_number = -1
        
        for card in self.middleCards:
            playerCards.append(card)
            AICards.append(card)
        
        

    def findWinner(self):
        playerBestScore, playerBestCards = self.GetBestHand(self.playerCards)
        AIBestScore, AIBestCards = self.GetBestHand(self.AICards)
        winner = ""

        if (playerBestScore > AIBestScore):
            winner =  "Player"
            self.return_number = 0
        elif (AIBestScore > playerBestScore):
            winner = "AI"
            self.return_number = 1
        else: #tie case
            
            tieBreak = self.tie_breaker(list(playerBestCards), list(AIBestCards), AIBestScore)

            if tieBreak[1] == 1:
                winner = "Player"
                self.return_number = 0
            elif tieBreak[1] == 2:
                self.return_number = 1
                winner = "AI"
            else:
                winner = "tie"
                self.return_number = 2


        return winner, playerBestCards, playerBestScore, AIBestCards, AIBestScore


    def GetBestHand(self, cards):
    
        possibleCombinations = list(combinations(cards, 5))
        bestScore = 0
        bestCombo = possibleCombinations[0]
        #runs all possible five card combinations through evaluateCards to get possible hand from 2 cards in hand plus middle cards
        for combo in possibleCombinations:
            score = self.evaluateCards(combo)

            if score > bestScore:
                bestScore = score
                bestCombo = combo    
            elif score == bestScore:
                bestCombo = self.tie_breaker(list(bestCombo), list(combo), -1)[0]
                
        return bestScore, bestCombo

    def evaluateCards(self, cards):
        cardsConverted = []
        for card in cards:
            tup = (self.suits[card.get_suit()], self.numbers[card.get_number()])
            cardsConverted.append(tup)
        suits = [card[0] for card in cardsConverted]
        numbers = [card[1] for card in cardsConverted]
        if (self.check_royal_flush(suits, numbers)):
            return 10
        elif (self.check_straight_flush(suits, numbers)):
            return 9
        elif (self.check_four_of_kind(numbers)):
            return 8
        elif (self.check_full_house(numbers)):
            return 7
        elif (self.check_flush(suits)):
            return 6
        elif (self.check_straight(suits, numbers)):
            return 5
        elif (self.check_three_of_kind(suits, numbers)):
            return 4
        elif (self.check_pairs(suits, numbers) == 2):
            return 3
        elif (self.check_pairs(suits, numbers) == 1):
            return 2
        else:
            return 1

    def evaluate_score(self, cards):
        cardsConverted = []
        for card in cards:
            tup = (self.suits[card.get_suit()], self.numbers[card.get_number()])
            cardsConverted.append(tup)
        suits = [card[0] for card in cardsConverted]
        numbers = [card[1] for card in cardsConverted]
        if (self.check_royal_flush(suits, numbers)):
            return 649737
        elif (self.check_straight_flush(suits, numbers)):
            return 72193
        elif (self.check_four_of_kind(numbers)):
            return 4164
        elif (self.check_full_house(numbers)):
            return 693
        elif (self.check_flush(suits)):
            return 508
        elif (self.check_straight(suits, numbers)):
            return 253
        elif (self.check_three_of_kind(suits, numbers)):
            return 46
        elif (self.check_pairs(suits, numbers) == 2):
            return 20
        elif (self.check_pairs(suits, numbers) == 1):
            return 2
        else:
            return 1
    
    def check_royal_flush(self, suits, numbers):
        numbers.sort()
        
        if (self.check_flush(suits)):
            for i in range(0, 5):
                if not numbers[i] == 10 + i:
                    return False
            return True
        return False
    
    def check_straight_flush(self, suits, numbers):
        numbers.sort()

        if (self.check_flush(suits)):
            for i in range(0, 4):
                if not numbers[i] + 1 == numbers[i + 1]:
                    return False
            return True
        return False

    def check_four_of_kind(self, numbers):
        d = {number : numbers.count(number) for number in numbers}
        for i in d:
            if d[i] >= 4:
                return True
        return False

    def check_full_house(self, numbers):
        if (len(set(numbers)) == 2):
            return True
        return False


    def check_flush(self, suits):
        suits = set(suits)  #gets only unique elements in suits list

        if (len(set(suits)) == 1):
            return True
        else:
            return False

    def check_straight(self, suits, numbers):
        if (len(set(numbers)) == 5):
            for i in range(0, 4):
                if not numbers[i] + 1 == numbers[i + 1]:
                    return False
            return True

    def check_three_of_kind(self, suits, numbers):
        d = {number : numbers.count(number) for number in numbers}
        for i in d:
            if d[i] == 3:
                return True
        return False

    def check_pairs(self, suits, numbers):
        pairs = 0
        d = {number : numbers.count(number) for number in numbers}

        for i in d:
            if d[i] == 2:
                pairs += 1

        return pairs

    #this method handles tie cases and returns the tie-winning hand
    def tie_breaker(self, cards1, cards2, score):
        
        numbers1 = []
        numbers2 = []
        for i in range(0, 5):
            numbers1.append(cards1[i].get_number())
            numbers2.append(cards2[i].get_number())
        set(numbers1)
        set(numbers2)
        numbers1.sort(reverse = True)
        numbers2.sort(reverse = True)
        
        if score == 2:
            pair1 = 0
            pair2 = 0
            for i in range(0, len(numbers1) - 1):
                for j in range(i + 1, len(numbers1)):
                    if self.numbers[numbers1[i]] == self.numbers[numbers1[j]]:
                        pair1 = self.numbers[numbers1[i]]
                    elif self.numbers[numbers2[i]] == self.numbers[numbers2[j]]:
                        pair2 = self.numbers[numbers2[i]]
            if pair1 > pair2:
                return cards1, 1
            elif pair1 < pair2:
                return cards2, 2
            else:
                return cards1, -1
        
        else:
            for i in range(0, len(numbers1)):
                if self.numbers[numbers1[i]] > self.numbers[numbers2[i]]:
                    return cards1, 1
                elif self.numbers[numbers2[i]] > self.numbers[numbers1[i]]:
                    return cards2, 2

            return cards1, -1

    def __str__(self):
        results = self.findWinner()
        #out = "\n" * 100
        out = ""
        '''
        out += "Player:"
        for card in self.playerCards:
            out += " " + str(card)
        out += "\nAI:"
        for card in self.AICards:
            out += " " + str(card)
        out+= "\n\n\n"
        '''
        '''
        if results[0] == "Player":
            out += "Congratulations! You win this round.\n"
        elif results[0] == "AI":
            out += "You lose this round.\n"
        elif results[0] == "tie":
            out += "This round is a tie (both have identical best hands). \n"
        '''
        out += "Your best hand: " + str(self.bestHands[results[2]]) + ","
        for i in range(0, 5):
            out += " " + str(results[1][i])

        out += "\nThe AI's best hand: " + str(self.bestHands[results[4]]) + ","
        for i in range(0, 5):
            out += " " + str(results[3][i])
        
        return out