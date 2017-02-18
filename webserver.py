#!/usr/bin/env python3
import argparse
import flask
import os

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--host', help='The host name or ip address to run on', type=str, default='localhost')
parser.add_argument('--port', help='The port number the web server will use', type=int, default=5000)
parser.add_argument('--cert', help='The SSL certificate', type=str)
parser.add_argument('--key', help='The SSL private key', type=str)
parser.add_argument('-d', '--debug', help='Enable debugging mode', action="store_true")
parser.add_argument('-v', '--verbose', help='Enable verbose mode', action="store_true")
args = parser.parse_args()

# Global variables
secure = bool(args.key) and bool(args.cert)

app = flask.Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                                     'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    # Display basic info based on command line arguments
    if args.verbose: print("Verbose mode activated")
    if args.debug: print("Debug mode activated")
    if bool(args.cert) != bool(args.key):
        print("ERROR! --cert and --key must be used together")
        exit(1)
    if args.verbose or args.debug:
        if secure:
            print("Using HTTPS on port %d" % args.port)
        else:
            print("Using HTTP on port %d" % args.port)
    if secure:
        try:
            context = (args.cert, args.key)
            app.run(port=args.port, debug=args.debug, ssl_context=context, host=args.host)
        except Exception as e:
            if args.debug:
                print(e.message)
                exit(2)
            else:
                print("ERROR! Invalid certificate or key file")
                print("Use --debug for more info")
                exit(2)
    else:
        app.run(port=args.port, debug=args.debug, host=args.host)
