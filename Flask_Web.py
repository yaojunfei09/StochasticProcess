import socket
import platform
from flask import Flask, render_template, jsonify

from apps.constants import *
from apps.BrownianMotion import BrownianStatistics
from apps.Martingale import MartingaleStatistics

app = Flask(__name__, template_folder='', static_folder='', static_url_path='')
assignment_list = list()

# brownian motion
brownian_statistics = BrownianStatistics()
brownian_statistics.generate_brownian_motion()

# martingale
martingale_statistics = MartingaleStatistics()
martingale_statistics.generate_martingale()


@app.route('/', methods=['get'])
def index():
    return render_template('templates/Index.html')


# Brownian Motion
@app.route('/brownian_motion', methods=['get'])
def brownian_motion():
    return render_template('templates/BM.html')


@app.route("/brownian_motion_printer", methods=['GET', 'POST'])
def brownian_motion_printer():
    # build index
    index_list = range(brownian_motion_length + 1)

    # get brownian motion
    brownian_motion_list = brownian_statistics.brownian_motion_list

    # build table
    table_html = brownian_statistics.build_statistics_table()

    return jsonify(index_list=index_list, brownian_motion_list=brownian_motion_list, table_html=table_html)


# Martingale
@app.route('/martingale', methods=['get'])
def martingale():
    return render_template('templates/MG.html')


@app.route("/martingale_printer", methods=['GET', 'POST'])
def martingale_printer():
    # build index
    index_list = range(martingale_length + 1)

    # get brownian motion
    martingale_list = martingale_statistics.avm_martingale_list

    # build table
    table_html = martingale_statistics.build_statistics_table()

    return jsonify(index_list=index_list, martingale_list=martingale_list, table_html=table_html)


if __name__ == '__main__':
    if platform.system() == "Windows":
        app.run(host=socket.gethostbyname(socket.gethostname()), port=8888, debug=False, threaded=True)
    else:
        app.run(host='0.0.0.0', port=8888, debug=False, threaded=True)
