from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

# adding this method
@app.route("/")
def show_counter():
    if not "random_num" in session:
        session['random_num'] = random.randint(1,100)
    if not 'number_of_guesses' in session:
        session['number_of_guesses'] = 0
    end_game = ''
    session['accuracy'] = ''
    accuracy = session['accuracy']
    color = ''

    if "guess" in session:
        print (accuracy, session['guess'])
        if session['guess'] > session['random_num']:
            color='red'
            accuracy = "Too High!"
        elif session['guess'] < session['random_num']:
            color='red'
            accuracy = "Too Low!"
        else:
            color= 'green'
            accuracy = "You got it! " + str(session['random_num']) + " was the number!"
            end_game = "Good Game!"
    if (session['number_of_guesses'] >= 5 and (accuracy == "Too High!" or accuracy == "Too Low!")):
        end_game = "Too many tries. You lose!"

    return render_template("index.html",accuracy = accuracy, random_num = session["random_num"],
    num_of_guesses = session['number_of_guesses'], color=color, end_game = end_game)

@app.route('/process', methods=['POST'])
def is_it_right():
    session['guess'] = int(request.form['guess'])
    session['number_of_guesses']+=1
    return redirect('/')

@app.route('/leaderboard', methods=['POST'])
def leaders():
    if not "leaderboard" in session:
        session['leaderboard'] = []
        print("creating leaderboard")
    name = request.form['name']
    number_of_guesses = session['number_of_guesses']
    lb = session['leaderboard']
    lb.append([name, number_of_guesses])
    session['leaderboard'] = lb
    print(session['leaderboard'])
    return render_template('leaderboard.html')

@app.route('/destroysession', methods=['POST'])
def destroy_session():
    session.pop('number_of_guesses')
    session.pop('random_num')
    session.pop('guess')
    # session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
