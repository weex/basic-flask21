import os
import json
import random

from flask import Flask
from flask import request, send_from_directory, render_template

from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

# directory of the digital content we'd like to sell
dir_path = '/home/twenty/var/fee'

# endpoint to look up files to buy
@app.route('/')
@app.route('/info')
def info():
    return json.dumps(files)


@app.route('/files.html')
def html_file_lookup():
    files_arr = [] # files dict   
    for key in files.keys():
        entry = {}
        entry['id'] = key
        entry['name'] = files[key][0]
        entry['price'] = files[key][1]
        files_arr.append(entry)
    return render_template('files.html', files=files_arr)

# return the price of the selected file
def get_price_from_request(request):
    id = int(request.args.get('selection'))
    return files[id][1]

# machine-payable endpoint that returns selected file if payment made
@app.route('/buy')
@payment.required(get_price_from_request)
def buy_file():

    # extract selection from client request
    sel = int(request.args.get('selection'))

    # check if selection is valid
    if(sel < 1 or sel > len(file_list)):
        return 'Invalid selection.'
    else:
        return send_from_directory(dir_path, file_list[int(sel)-1])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
