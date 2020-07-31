from image_generation import generate_image, configure_matplotlib
from roulette_martingale import roulette_martingale
from flask import Flask, send_file, request

app = Flask(__name__)


@app.route('/api/v1/roulette/martingale', methods=['GET'])
def serve_image():
    # Number of Martingale sessions - A session ends when the player can no longer win back their losses
    configure_matplotlib()
    sessions = request.args.get('sessions', default=1000, type=int)
    bankroll = request.args.get('bankroll', default=1000, type=int)
    modified = request.args.get('mod', default=False, type=bool)
    max_bet = request.args.get('max', default=5000, type=int)
    min_bet = request.args.get('min', default=5, type=int)
    martingale = roulette_martingale(bankroll, min_bet, max_bet, modified)
    martingale.play_x_sessions(sessions)
    image_buf = generate_image(martingale.get_spins_history(), martingale.get_winnings_history(), bankroll, min_bet, max_bet)
    return send_file(image_buf, attachment_filename='result.png', mimetype='image/png')


@app.route('/api/v2/simulation', methods=['GET'])
def get_simulation_json():
    sessions = request.args.get('sessions', default=1000, type=int)
    bankroll = request.args.get('bankroll', default=1000, type=int)
    modified = request.args.get('mod', default=False, type=bool)
    max_bet = request.args.get('max', default=5000, type=int)
    min_bet = request.args.get('min', default=5, type=int)
    martingale = roulette_martingale(bankroll, min_bet, max_bet, modified)
    martingale.play_x_sessions(sessions)
    return martingale.get_json_results()


@app.route('/api/v2/bullets', methods=['GET'])
def get_bullets():
    bankroll = request.args.get('bankroll', default=500, type=int)
    modified = request.args.get('mod', default=False, type=bool)
    max_bet = request.args.get('max', default=5000, type=int)
    min_bet = request.args.get('min', default=5, type=int)
    martingale = roulette_martingale(bankroll, min_bet, max_bet, modified)
    bullets = martingale.get_bullets()
    return str(bullets)


if __name__ == '__main__':
    app.run(debug=True)
