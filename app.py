import random
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


    meeword_chars= [random.choice(meechars) for meechars in char_sets]

    all_chars = "".join(char_sets)
    remaining_length = length - len(meeword_chars)
    meeword_chars += [random.choice(all_chars) for _ in range(remaining_length)]
        
    random.shuffle(meeword_chars)

    meeword = "".join(meeword_chars)
    print("Password: ",meeword)


    has_upper=any(c.isupper() for c in meeword)
    has_lower=any(c.islower() for c in meeword)
    has_digit=any(c.isdigit() for c in meeword)
    has_symbol=any(c in string.punctuation for c in meeword)

    types_count = has_upper + has_digit + has_lower + has_symbol

    if length < 10 or types_count < 2 :
        strength = "Weak"

    elif types_count == 2 :
        strength = "Medium"

    else:
       strength = "Strong"     


    return jsonify({"password": meeword, "strength" : strength})


if __name__ == "__main__":
    app.run(debug=True)