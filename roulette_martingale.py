from datetime import datetime
import random
import io

DOUBLE_ZERO = '00'
BLACK = 'BLACK'
RED = 'RED'
ZERO = '0'


class roulette_martingale:
    def __init__(self, starting_amount, min_bet, max_bet, bet_target=BLACK):
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

    def get_spins_history(self):
        return self.history['spins']
    
    def get_winnings_history(self):
        return self.history['winnings']

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

    def get_bullets(self):
        bullets = []
        leftover_bankroll = self.starting_amount
        next_bullet = self.min_bet
        while leftover_bankroll >= next_bullet:
            bullets.append(next_bullet)
            leftover_bankroll -= next_bullet
            next_bullet = min(next_bullet * 2, self.max_bet)
        if leftover_bankroll > 0: bullets.append(leftover_bankroll)
        return bullets

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
