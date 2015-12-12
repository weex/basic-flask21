import os
import json

from flask import Flask
from flask import request 

from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

@app.route('/')
@app.route('/info')
@app.route('/help')
def home():
    '''Document the API so that other services could consume automatically.'''
    home_obj = [{"name": "basic template",
                 "service_version": "1",
                 "api_version": "1",
                 "description": "Describe your service in a couple of sentences or less.",
                 "endpoints" : [
                                {"route": "/example",
                                 "args": [{"name": "first_arg",
                                           "description": "Describe the first argument to this endpoint."},
                                           ],  
                                 "per-req": PRICE,
                                 "description": "Briefly describe this endpoint.",
                                 "returns": [{"name": "first_return",
                                              "description": "Describe the first piece of data your service returns."},
                                            ],
                                },
                                {"route": "/info",
                                 "args": None,
                                 "per-req": 0,
                                 "description": "This listing of endpoints provided by this server. "\
                                    "Available at /info."
                                }],
                }
               ]

    body = json.dumps(home_obj, indent=2)

    return (body, 200, {'Content-length': len(body),
                        'Content-type': 'application/json',
                       }
           )

@payment.required(PRICE)
@app.route('/example')
def example_function():
    # do stuff
    return json.dumps({'first_return':'your data goes here'})

if __name__ == '__main__':
    if DEBUG:
        app.debug = True
    app.run(host='0.0.0.0')
