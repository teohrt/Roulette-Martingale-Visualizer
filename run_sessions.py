from matplotlib import pyplot as plt 
from datetime import datetime
import numpy as np  
import random

ZERO = '0'
DOUBLE_ZERO = '00'
BLACK = 'BLACK'
RED = 'RED'


class roulette_martinagle:
    def __init__(self,bet_target=BLACK,starting_units=200,max_bet=1000):
        # There are many roulette tables in Vegas that have $5 min and $5,000 max
        # These defaults account for a $1,000 bank roll in this situation
        self.starting_units = starting_units
        self.current_units = starting_units
        self.bet_target = bet_target
        self.max_bet = max_bet
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
        while bet_units <= self.current_units and bet_units < self.max_bet:
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
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Roulette\'s Martinagle Strategy - %s Sessions' % len(stats))
    
    ax1.set_title('Busts per Spin Number')
    bins = []
    for i in range(0, 1000, 10):
        bins.append(i)
    ax1.hist(a, bins = bins)

    ax2.set_title('Bust Percentage for Spin Count Range')
    ranges = [25, 50, 100, 150]
    range_counts = [0, 0, 0, 0, 0]
    for val in stats:
        if val <= ranges[0]:
            range_counts[0] += 1
        elif val <= ranges[1]:
            range_counts[1] += 1
        elif val <= ranges[2]:
            range_counts[2] += 1
        elif val <= ranges[3]:
            range_counts[3] += 1
        else:
            range_counts[4] += 1
    labels = ['X<=25', '25<X<=50', '50<X<=100', '100<X<=150', 'X>150']
    ax2.pie(range_counts, labels=labels, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.  

    plt.tight_layout()
    plt.show()


def main():
    sample_size = 10000  # Number of Martingale sessions - A session ends when the player can no longer win back their losses
    stats = get_stats(sample_size)
    visualize_stats(stats)


if __name__ == '__main__':
    main()
