from app import create_app

app = create_app()

@app.route('/')
def home():
    return '@pedrobritobr'

if __name__ == "__main__":
    app.run(debug=True)
