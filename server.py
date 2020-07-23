from flask import Flask, send_file, request
from matplotlib import pyplot as plt 
from datetime import datetime
import numpy as np  
import matplotlib 
import random
import io

app = Flask(__name__)

DOUBLE_ZERO = '00'
BLACK = 'BLACK'
RED = 'RED'
ZERO = '0'


class roulette_martingale:
    def __init__(self, starting_amount, min_bet, max_bet, bet_target=BLACK,):
        self.amount_before_losing_streak = starting_amount
        self.starting_amount = starting_amount
        self.current_amount = starting_amount
        self.bet_target = bet_target
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.spin_count = 0
        self.history = {
            'spins': [],
            'winnings': []
        }

        self.spinner = []
        for _ in range(49):
            self.spinner.append(BLACK)
            self.spinner.append(RED)
        self.spinner.append(ZERO)
        self.spinner.append(DOUBLE_ZERO)

    def spin(self):
        self.spin_count += 1
        random.seed(datetime.now())
        random_num = random.randrange(0, 100)
        spin_value = self.spinner[random_num]
        if spin_value in [ZERO, DOUBLE_ZERO]:
            return spin_value
        return [spin_value, random_num]

    def bet(self,units_bet):
        self.current_amount -= units_bet
        spin_outcome = self.spin()
        if self.bet_target in spin_outcome:
            units_won = 2 * units_bet
            self.current_amount += units_won
            self.amount_before_losing_streak = self.current_amount
            return True  # Win
        return False  # Lose

    def reset(self):
        self.spin_count = 0
        self.current_amount = self.starting_amount
        self.amount_before_losing_streak = self.starting_amount

    def play_to_bust(self):
        bet_amount = self.min_bet
        while bet_amount <= self.current_amount and bet_amount <= self.max_bet:
            won_bet = self.bet(bet_amount)
            if won_bet:
                # Martingale strategy dictates that a bet after a win is the minimum bet value
                bet_amount = self.min_bet
            else:
                # Martingale strategy dictates that a bet after a loss is double the previous bet's value
                bet_amount = (2 * bet_amount)
        # Now the player has gone bust due to their inability to win back their losses
        self.history['spins'].append(self.spin_count)
        self.history['winnings'].append(self.amount_before_losing_streak)
        self.reset()
    
    def play_x_sessions(self, x):
        for _ in range(x):
            self.play_to_bust()

    def get_plot(self):
        a = np.array(self.history['spins'])
        fig, (ax1, ax2, ax3) = plt.subplots(3)
        fig.suptitle('Roulette Martingale Strategy - %s Sessions\n$%s Bank Roll\n\$%s Min Bet / $%s Max Bet\n' % (len(self.history['spins']), self.starting_amount, self.min_bet, self.max_bet))
        
        ax1.set_title('Busts per Spin Number')
        bins = []
        for i in range(0, 1000, 10):
            bins.append(i)
        ax1.hist(a, bins = bins)
        ax1.set_xlabel('Spin #\n')
        ax1.set_ylabel('Bust Count')

        ranges = [25, 50, 100, 150]
        range_bust_counts, range_average_winnings = self._get_range_stats(ranges)

        ax2.set_title('Spin Count Range Bust Frequency')
        labels = ['X<=25', '25<X<=50', '50<X<=100', '100<X<=150', 'X>150']
        ax2.pie(range_bust_counts, labels=labels, autopct='%1.1f%%', startangle=90)
        # plt.legend(patches, labels, bbox_to_anchor=(1,0.5), loc="center right", fontsize=8, bbox_transform=plt.gcf().transFigure)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.  

        ax3.plot(labels,range_average_winnings)
        ax3.set_title('Average Session Winnings (Pre Bust)')
        ax3.set_xlabel('Spin Count Range')
        ax3.set_ylabel('Bankroll')
        
        plt.tight_layout(pad=.5, w_pad=.5, h_pad=1)
        return plt
    
    def _get_range_stats(self, ranges):
        range_bust_counts = [0 for i in range(len(ranges) + 1)]
        range_average_winnings = [0 for i in range(len(ranges) + 1)]
        range_winnings_lists = [] # 2D list to store winnings earned in ranges for averaging. TODO: Optimize this for space
        for _ in range(len(ranges) + 1):
            range_winnings_lists.append([])

        for winnings_pre_bust, spin_count in zip(self.history['winnings'], self.history['spins']):
            found = False
            for i, range_val in enumerate(ranges):
                if spin_count <= range_val:
                    range_bust_counts[i] += 1
                    range_winnings_lists[i].append(winnings_pre_bust)
                    found = True
                    break
            if not found:
                range_bust_counts[-1] += 1
                range_winnings_lists[-1].append(winnings_pre_bust)
        
        for i, range_winnings in enumerate(range_winnings_lists):
            range_total = 0
            for winnings in range_winnings:
                range_total += winnings
            range_average_winnings[i] = range_total / len(range_winnings)
        return range_bust_counts, range_average_winnings
        
    def get_result_png_buffer(self):
        plot = self.get_plot()
        buf = io.BytesIO()
        plot.savefig(buf, format='png', dpi=1000)
        buf.seek(0)
        return buf


def configure_matplotlib():
    # Sets the background to non-interactive, ensuring the library doesn't initialize GUI
    # https://github.com/matplotlib/matplotlib/issues/14304/
    matplotlib.use('agg')

    plt.rc('font', size=5)          # controls default text sizes
    plt.rc('axes', titlesize=7)     # fontsize of the axes title
    plt.rc('axes', labelsize=5)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=4)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=4)    # fontsize of the tick labels
    plt.rc('legend', fontsize=5)    # legend fontsize
    plt.rc('figure', titlesize=8)  # fontsize of the figure title


@app.route('/api/v1/roulette/martingale', methods=['GET'])
def serve_image():
    # Number of Martingale sessions - A session ends when the player can no longer win back their losses
    sessions = request.args.get('sessions', default=1000, type=int)
    bankroll = request.args.get('bankroll', default=1000, type=int)
    max_bet = request.args.get('max', default=5000, type=int)
    min_bet = request.args.get('min', default=5, type=int)
    martingale = roulette_martingale(bankroll, min_bet, max_bet)
    martingale.play_x_sessions(sessions)
    buf = martingale.get_result_png_buffer()
    return send_file(buf, attachment_filename='result.png', mimetype='image/png')


if __name__ == '__main__':
    configure_matplotlib()
    app.run(debug=False)
