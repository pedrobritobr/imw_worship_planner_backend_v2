import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from __init__ import create_app

app = create_app()

@app.route('/')
def home():
    print('Hello World')
    return '@pedrobritobr'

if __name__ == "__main__":
    app.run(debug=True)
