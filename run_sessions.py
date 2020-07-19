from matplotlib import pyplot as plt 
from datetime import datetime
import numpy as np  
import random

ZERO = '0'
DOUBLE_ZERO = '00'
BLACK = 'BLACK'
RED = 'RED'


class roulette_martinagle:
    def __init__(self,bet_target=BLACK,starting_units=100):
        self.starting_units = starting_units
        self.bet_target = bet_target
        self.current_units = starting_units
        self.spin_count = 0

        self.spinner = []
        for _ in range(49):
            self.spinner.append(BLACK)
            self.spinner.append(RED)
        self.spinner.append(ZERO)
        self.spinner.append(DOUBLE_ZERO)

    def spin(self):
        random.seed(datetime.now())
        random_num = random.randrange(0, 100)
        spin_value = self.spinner[random_num]
        result = []
        if spin_value in [ZERO, DOUBLE_ZERO]:
            result = spin_value
        result = [spin_value, random_num]
        self.spin_count += 1
        return result

    def bet(self,units_bet):
        self.current_units -= units_bet
        spin_outcome = self.spin()
        if self.bet_target in spin_outcome:
            units_won = 2 * units_bet
            self.current_units += units_won
            return True  # Win
        return False  # Lose

    def reset(self):
        self.spin_count = 0
        self.current_units = self.starting_units

    def play_to_bust(self):
        bet_units = 1
        while bet_units <= self.current_units:
            won_bet = self.bet(bet_units)
            if won_bet:
                # Martingale strategy dictates that a bet after a win is the minimum bet value
                bet_units = 1
            else:
                # Martingale strategy dictates that a bet after a loss is double the previous bet's value
                bet_units = (2 * bet_units)
        # Now the player has gone bust due to their inability to win back their losses
        spin_count = self.spin_count
        self.reset()
        return spin_count


def get_stats(sample_size):
    stats = []
    martingale = roulette_martinagle()
    for _ in range(sample_size):
        number_of_spins = martingale.play_to_bust()
        stats.append(number_of_spins)
    return stats


def visualize_stats(stats):
    a = np.array(stats)
    bins = []
    for i in range(0, 1000, 10):
        bins.append(i)
    plt.hist(a, bins = bins) 
    plt.title("Martingale Roulette - Spin Number that Bust - %s Sessions" % len(stats)) 
    plt.show()


def main():
    SAMPLE_SIZE = 10000  # Number of Martingale sessions - A session ends when the player can no longer win back their losses
    stats = get_stats(SAMPLE_SIZE)
    visualize_stats(stats)


if __name__ == '__main__':
    main()
