import secrets
import string
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("frontend.html")


@app.route("/generate", methods=["POST"])
def generate_password():
    data = request.get_json()

    length = int(data.get('length', 12))
    uppercase = data.get('uppercase', True)
    lowercase = data.get('lowercase', True)
    digit = data.get('digits', True)
    symbols = data.get('symbols', True)
    exclude_confusing = data.get('exclude_confusing', False)

    char_sets = []

    if uppercase:
        meechars = string.ascii_uppercase
        if exclude_confusing:
            meechars=meechars.replace("O","")
        char_sets.append(meechars)

    if lowercase:
        meechars = string.ascii_lowercase
        if exclude_confusing:
            meechars=meechars.replace("l","")
        char_sets.append(meechars)

    if digit:
        meechars=string.digits
        if exclude_confusing:
            meechars=meechars.replace("0","").replace("1","")
        char_sets.append(meechars)

    if symbols:
        meechars=string.punctuation
        char_sets.append(meechars)

    if not char_sets:
        return jsonify({"error":"Please select at least one character type !!"}),400
    

    all_chars = "".join(char_sets)
    meeword_chars= [secrets.choice(pool) for pool in char_sets]
    meeword_chars += [secrets.choice(all_chars) for _ in range(length - len(meeword_chars))]
        
    secrets.SystemRandom().shuffle(meeword_chars)

    meeword = "".join(meeword_chars)
    

    score = 0
    if any(c.islower() for c in meeword) :
           score +=1

    if any(c.isupper() for c in meeword):
           score +=1

    if any(c.isdigit() for c in meeword):
           score +=1

    if any(c in string.punctuation for c in meeword):
        score +=1

    if length >= 12:
        score +=1

    if score <= 2:
         strength = "Weak"     
    elif score == 3:
         strength = "Medium"
    else:
         strength = "Strong"

    return jsonify({"password": meeword, "strength" : strength})


@app.route("/check", methods = ["POST"])
def check_password():
    data = request.get_json()
    pwd = data.get("password","")

    has_upper=any(c.isupper() for c in pwd)
    has_lower=any(c.islower() for c in pwd)
    has_digit=any(c.isdigit() for c in pwd)
    has_symbol=any(c in string.punctuation for c in pwd)

    tips = []
    if len (pwd) < 10:
        tips.append("Use at least 10 characters")

    if not has_upper:
        tips.append("Add uppercase letters")

    if not has_lower:
        tips.append("Add lowercase letters")

    if not has_digit:
        tips.append("Add digits")

    if not has_symbol:
        tips.append("Add symbols")

    types_count = has_symbol + has_digit + has_lower + has_upper

    if len(pwd)<7 or types_count < 2:
        strength = "Weak"

    elif 2 <= types_count < 4:
        strength = "Medium"

    else:
        strength = "Strong"

    return jsonify({"strength":strength, "tips":tips})
     


if __name__ == "__main__":
    app.run(debug=True) 