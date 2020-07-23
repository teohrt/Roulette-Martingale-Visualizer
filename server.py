from roulette_martingale import roulette_martingale
from flask import Flask, send_file, request
from image_generation import generate_image, configure_matplotlib

app = Flask(__name__)


@app.route('/api/v1/roulette/martingale', methods=['GET'])
def serve_image():
    # Number of Martingale sessions - A session ends when the player can no longer win back their losses
    sessions = request.args.get('sessions', default=1000, type=int)
    bankroll = request.args.get('bankroll', default=1000, type=int)
    max_bet = request.args.get('max', default=5000, type=int)
    min_bet = request.args.get('min', default=5, type=int)
    martingale = roulette_martingale(bankroll, min_bet, max_bet)
    martingale.play_x_sessions(sessions)
    image_buf = generate_image(martingale.get_spins_history(), martingale.get_winnings_history(), bankroll, min_bet, max_bet)
    return send_file(image_buf, attachment_filename='result.png', mimetype='image/png')


if __name__ == '__main__':
    configure_matplotlib()
    app.run(debug=False)
