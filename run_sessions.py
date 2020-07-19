
from matplotlib import pyplot as plt 
from datetime import datetime
import numpy as np  
import random

ZERO = '0'
DOUBLE_ZERO = '00'
BLACK = 'BLACK'
RED = 'RED'

class roulette_martinagle:
    def __init__(self,starting_units=100):
        self.starting_units = starting_units
        self.bet_target = BLACK
        self.current_units = starting_units
        self.spin_history = []

        # spinner initialization
        self.spinner_array = []
        for _ in range(49):
            self.spinner_array.append(BLACK)
            self.spinner_array.append(RED)
        self.spinner_array.append(ZERO)
        self.spinner_array.append(DOUBLE_ZERO)

    def spin(self):
        random.seed(datetime.now())
        random_num = random.randrange(0, 100)
        spin_value = self.spinner_array[random_num]
        result = []
        if spin_value in [ZERO, DOUBLE_ZERO]:
            result = spin_value
        result = [spin_value, random_num]
        self.spin_history.append(result)
        return result

    def bet(self,units_bet):
        self.current_units -= units_bet
        spin_outcome = self.spin()
        if self.bet_target in spin_outcome:
            units_won = 2 * units_bet
            self.current_units += units_won
            return True
        else:
            return False

    def reset(self):
        self.spin_history = []
        self.current_units = self.starting_units

    def play_to_bust(self):
        bet_units = 1
        while bet_units <= self.current_units:
            won_bet = self.bet(bet_units)
            if won_bet:
                bet_units = 1
            else:
                bet_units = (2 * bet_units)
        number_of_session_spins = len(self.spin_history)
        self.reset()
        return number_of_session_spins

history = []
martingale = roulette_martinagle()
for i in range(10000):
    number_of_spins = martingale.play_to_bust()
    history.append(number_of_spins)

a = np.array(history)
bins = []
for i in range(0, 500, 10):
    bins.append(i)
plt.hist(a, bins = bins) 
plt.title("Martingale - Spins to Bust") 
plt.show()
