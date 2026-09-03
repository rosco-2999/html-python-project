# https://flask.palletsprojects.com/en/stable/

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "any_random_string_here"

def initialize_combat_session():
    # Only initialize if stats don't exist
    if 'player_health' not in session:
        session['player_health'] = 100
        session['enemy_health'] = 50
        session['player_damage'] = 15 
        session['enemy_damage'] = 10
        session['combat_message'] = "A YEAR0001 Goon appears! Prepare to fight for Gluee!"
        session['roll_result'] = None
        session['defense_roll'] = None
        session.modified = True

# Homepage
@app.route("/")
def homepage():
    name = "greg"
    return render_template("index.html", friend_name = name)

@app.route("/start", methods = ["POST", "GET"])
def start():
    
    if request.method == "POST":
        character = request.form.get('character')
        weapon = request.form.get('weapon')
        session['weapon'] = weapon
        username = request.form.get('username')
        return render_template(
            "start.html",
            character=character,
            weapon=weapon,
            username=username,
        )
        #print("DEBUG: {character}{weapon_type}{health}")
        return render_template("start.html", character = character, weapon = weapon, username = username)
    # GET, so there was nothing submitted
    return render_template("start.html")


def start_fight():
    session['player_hp'] = 45
    session['enemy_hp'] = 45
    session['messages'] = []
    session['state'] = "awaiting_action"

def add(msg):
    if 'messages' not in session:
        session['messages'] = []
    session['messages'].append(msg)
    session.modified = True

@app.route("/stockholm")


def backtostockholm():
    return render_template("stockholm.html")

@app.route("/stockholm", methods=["GET", "POST"])
    
def stockholm():
    if "player_hp" not in session:
        start_fight()
        
    if request.method == "POST":
        action = request.form.get("decision")

        if action == "stagnate":
            session['messages'] = []
            add("You hesitate... the enemy attacks first!")
            enemy_attack()
            return render_template("stockholm.html",
                                   messages=session['messages'],
                                   player_hp=session['player_hp'],
                                   enemy_hp=session['enemy_hp'])
        if session['player_hp'] <= 0:
            session.clear()
            return redirect("/index")

        if action == "attack":
            session['messages'] = []
            required = random_int(1, 15)
            session['required_roll'] = required
            add(f"To hit the goon, you must roll **{required}** or higher!")
            session['state'] = "waiting_for_player_roll"
            return render_template("stockholm.html",
                                   messages=session['messages'],
                                   player_hp=session['player_hp'],
                                   enemy_hp=session['enemy_hp'],
                                   required_roll=required)

        if action == "player_roll":
            required = session.get("required_roll")
            roll = random_int(1, 15)
            add(f"You rolled a **{roll}**!")

            if roll >= required:
                dmg = random_int(5, 12)
                session['enemy_hp'] -= dmg
                add(f"Your {session['weapon']} hits! You deal **{dmg}** damage.")
            else:
                add(f"Your {session['weapon']} missed! Turn skipped.")

            if session['enemy_hp'] <= 0:
                add("🎉 You defeated the enemy!")
                return render_template("stockholm.html",
                                       messages=session['messages'],
                                       player_hp=session['player_hp'],
                                       enemy_hp=0)
            
            enemy_attack()
    return render_template("stockholm.html",
                           messages=session['messages'],
                           player_hp=session['player_hp'],
                           enemy_hp=session['enemy_hp'])

@app.route("/london", methods=["GET","POST"])
def london():
    if "player_hp" not in session:
        start_fight()

    if request.method == "POST":
        action = request.form.get("decision")

        if action == "stagnate":
            session['messages'] = []
            add("You hesitate... the enemy attacks first!")
            session['state'] = "enemy_turn"
            return render_template("london.html",
                                   messages=session['messages'],
                                   player_hp=session['player_hp'],
                                   enemy_hp=session['enemy_hp'])
        if session['player_hp'] <= 0:
            session.clear()
            return redirect("/index")

        if action == "attack":
            session['messages'] = []
            required = random_int(1, 15)
            session['required_roll'] = required
            add(f"To hit the goon, you must roll **{required}** or higher!")
            session['state'] = "waiting_for_player_roll"
            return render_template("london.html",
                                   messages=session['messages'],
                                   player_hp=session['player_hp'],
                                   enemy_hp=session['enemy_hp'],
                                   required_roll=required)

        if action == "player_roll":
            required = session.get("required_roll")
            roll = random_int(1, 15)
            add(f"You rolled a **{roll}**!")

            if roll >= required:
                dmg = random_int(5, 12)
                session['enemy_hp'] -= dmg
                add(f"Your {session['weapon']} hits! You deal **{dmg}** damage.")
            else:
                add(f"Your {session['weapon']} missed! Turn skipped.")

            if session['enemy_hp'] <= 0:
                add("🎉 You defeated the enemy!")
                return render_template("london.html",
                                       messages=session['messages'],
                                       player_hp=session['player_hp'],
                                       enemy_hp=0)
            
            enemy_attack()
    return render_template("london.html",
                           messages=session['messages'],
                           player_hp=session['player_hp'],
                           enemy_hp=session['enemy_hp'])
import random
def random_int(a, b):
    return random.randint(a, b)

def enemy_attack():
    add("Enemy is attacking!")
    required = random_int(1, 15)
    add(f"Enemy must roll **{required}** or higher to hit you.")
    roll = random_int(1, 15)
    add(f"Enemy rolled a **{roll}**.")
    if roll >= required:
        dmg = random_int(5, 10)
        session['player_hp'] -= dmg
        add(f"Enemy attack hits! You take **{dmg}** damage.")
    else:
        add("Enemy attack missed!")
    if session['player_hp'] <= 0:
        add("💀 You have been defeated...")
    enemy_defeated = session['enemy_hp'] <= 0

@app.route("/losangeles", methods=["POST", "GET"])
def losangeles():
    if "player_hp" not in session:
        start_fight()

    if request.method == "POST":
        action = request.form.get("decision")

        if action == "stagnate":
            session['messages'] = []
            add("You hesitate... the enemy attacks first!")
            enemy_attack()
            return render_template("losangeles.html",
                                   messages=session['messages'],
                                   player_hp=session['player_hp'],
                                   enemy_hp=session['enemy_hp'])
        if session['player_hp'] <= 0:
            session.clear()
            return redirect("/index")

        if action == "attack":
            session['messages'] = []
            required = random_int(1, 15)
            session['required_roll'] = required
            add(f"To hit the goon, you must roll **{required}** or higher!")
            session['state'] = "waiting_for_player_roll"
            return render_template("losangeles.html",
                                   messages=session['messages'],
                                   player_hp=session['player_hp'],
                                   enemy_hp=session['enemy_hp'],
                                   required_roll=required)

        if action == "player_roll":
            required = session.get("required_roll")
            roll = random_int(1, 15)
            add(f"You rolled a **{roll}**!")

            if roll >= required:
                dmg = random_int(5, 12)
                session['enemy_hp'] -= dmg
                add(f"Your {session['weapon']} hits! You deal **{dmg}** damage.")
            else:
                add(f"Your {session['weapon']} missed! Turn skipped.")

            if session['enemy_hp'] <= 0:
                ending_link = url_for('ending')
                add(f"🎉 You defeated the enemy! Click here to end the game!  ")
                return render_template("losangeles.html",
                                       messages=session['messages'],
                                       player_hp=session['player_hp'],
                                       enemy_hp=0, ending_link = ending_link)
            
            enemy_attack()
    return render_template("losangeles.html",
                           messages=session['messages'],
                           player_hp=session['player_hp'],
                           enemy_hp=session['enemy_hp'])
import random
def random_int(a, b):
    return random.randint(a, b)

def enemy_attack():
    add("Enemy is attacking!")
    required = random_int(1, 15)
    add(f"Enemy must roll **{required}** or higher to hit you.")
    roll = random_int(1, 15)
    add(f"Enemy rolled a **{roll}**.")
    if roll >= required:
        dmg = random_int(5, 10)
        session['player_hp'] -= dmg
        add(f"Enemy attack hits! You take **{dmg}** damage.")
    else:
        add("Enemy attack missed!")
    if session['player_hp'] <= 0:
        add("💀 You have been defeated...")


@app.route("/ending")
def ending():
    return render_template("ending.html")

# Run the program
if __name__ == "__main__":
    app.run(debug=True)