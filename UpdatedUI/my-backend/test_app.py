from flask import Flask, request

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    print("123")

if __name__ == '__main__':
    app.run(debug=True)
