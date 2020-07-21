from flask import Flask, send_file, make_response, request
from matplotlib import pyplot as plt 
from datetime import datetime
import numpy as np  
import matplotlib 
import random
import io

# Sets the background to non-interactive, ensuring that the library doesn't initialize GUI
# https://github.com/matplotlib/matplotlib/issues/14304/
matplotlib.use('agg')
app = Flask(__name__)

DOUBLE_ZERO = '00'
BLACK = 'BLACK'
RED = 'RED'
ZERO = '0'



class roulette_martingale:
    def __init__(self, bet_target=BLACK, starting_amount=1000, min_bet=5, max_bet=5000):
        self.starting_amount = starting_amount
        self.current_amount = starting_amount
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.bet_target = bet_target
        self.spin_count = 0
        self.history = []

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
            return True  # Win
        return False  # Lose

    def reset(self):
        self.spin_count = 0
        self.current_amount = self.starting_amount

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
        self.history.append(self.spin_count)
        self.reset()
    
    def play_x_sessions(self, x):
        for _ in range(x):
            self.play_to_bust()

    def get_plot(self):
        a = np.array(self.history)
        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle('Roulette Martingale Strategy - %s Sessions\n$%s Bank Roll\n\$%s Min Bet / $%s Max Bet' % (len(self.history), self.starting_amount, self.min_bet, self.max_bet))
        
        ax1.set_title('Busts per Spin Number')
        bins = []
        for i in range(0, 1000, 10):
            bins.append(i)
        ax1.hist(a, bins = bins)
        ax1.set_xlabel('Spin #')
        ax1.set_ylabel('Bust Frequency')

        ax2.set_title('Bust Percentage for Spin Count Range')
        ranges = [25, 50, 100, 150]
        range_counts = [0, 0, 0, 0, 0]
        for val in self.history:
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
        return plt
        
    def get_result_png_buffer(self):
        plot = self.get_plot()
        buf = io.BytesIO()
        plot.savefig(buf, format='png')
        buf.seek(0)
        return buf


@app.route('/result', methods=['GET'])
def serve_image():
    # Number of Martingale sessions - A session ends when the player can no longer win back their losses
    sample_size = request.args.get('sample', default=1000, type=int)
    martingale = roulette_martingale()
    martingale.play_x_sessions(sample_size)
    buf = martingale.get_result_png_buffer()
    return send_file(buf, attachment_filename='result.png', mimetype='image/png')
    
    
app.run(debug=False)
