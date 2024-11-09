from flask import Flask, render_template, request, jsonify
from chatbot import FrenchLearningBot

app = Flask(__name__)
bot = FrenchLearningBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response, running = bot.respond_to_user(user_input)
    return jsonify({'response': response, 'running': running})

if __name__ == '__main__':
    app.run(debug=True)
