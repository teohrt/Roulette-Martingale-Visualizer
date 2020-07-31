from matplotlib import pyplot as plt 
import numpy as np
import matplotlib 
import io


def configure_matplotlib():
    # Sets the background to non-interactive, ensuring the library doesn't initialize GUI
    # https://github.com/matplotlib/matplotlib/issues/14304/
    matplotlib.use('agg')

    plt.rc('font', size=5)         # controls default text sizes
    plt.rc('axes', titlesize=7)    # fontsize of the axes title
    plt.rc('axes', labelsize=5)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=4)   # fontsize of the tick labels
    plt.rc('ytick', labelsize=4)   # fontsize of the tick labels
    plt.rc('legend', fontsize=5)   # legend fontsize
    plt.rc('figure', titlesize=8)  # fontsize of the figure title


def get_range_stats(ranges, winnings, spins):
    range_bust_counts = [0 for i in range(len(ranges) + 1)]
    range_average_winnings = [0 for i in range(len(ranges) + 1)]
    range_winnings_lists = [] # 2D list to store winnings earned in ranges for averaging. TODO: Optimize for space
    for _ in range(len(ranges) + 1):
        range_winnings_lists.append([])

    for winnings_pre_bust, spin_count in zip(winnings, spins):
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
        if len(range_winnings) > 0:
            range_average_winnings[i] = range_total / len(range_winnings)
        else:
            range_average_winnings[i] = 0
    return range_bust_counts, range_average_winnings


def get_plot(spins, winnings, starting_amount, min_bet, max_bet):
    a = np.array(spins)
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Roulette Martingale Strategy - %s Sessions\n$%s Bank Roll\n\$%s Min Bet / $%s Max Bet\n' % (len(spins), starting_amount, min_bet, max_bet))
    
    ax1.set_title('Busts per Spin Number')
    bins = []
    for i in range(0, 1000, 10):
        bins.append(i)
    ax1.hist(a, bins = bins)
    ax1.set_xlabel('Spin #\n')
    ax1.set_ylabel('Bust Count')

    ranges = [25, 50, 100, 150]
    range_bust_counts, range_average_winnings = get_range_stats(ranges, winnings, spins)

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
    

def generate_image(spins, winnings, starting_amount, min_bet, max_bet):
    plot = get_plot(spins, winnings, starting_amount, min_bet, max_bet)
    buf = io.BytesIO()
    plot.savefig(buf, format='png', dpi=1000)
    buf.seek(0)
    return buf
