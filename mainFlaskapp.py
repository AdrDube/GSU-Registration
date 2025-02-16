from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('chatmain.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    selected_class = data.get('class')
    selected_time = data.get('time')
    return jsonify({"message": "Class scheduled successfully", "class": selected_class, "time": selected_time})

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True,port=5001)