from flask import Flask, jsonify, render_template, request, redirect, url_for

'''
It creates an instance of the Flask class, 
which will be your WSGI (Web Server Gateway Interface) application.

Learning Git
'''
app = Flask(__name__)

items = [
    {
        "id": 1, 
        "name": "Item 1", 
        "description": "This is the 1st item..."
    }, 
    {
        "id": 2, 
        "name": "Item 2", 
        "description": "This is the 2nd item..."
    }
]

@app.route("/")
def initializer():
    return "Welcome to the sample to-do list application."

@app.route("/items", methods = ["GET"])
def get_items():
    return jsonify(items)

@app.route("/items/<int:item_id>", methods = ['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"]==item_id), None)
    if item == None:
        return jsonify({"Error": "Item not found..."})
    return jsonify(item)

@app.route("/items", methods = ["POST"])
def create_item():
    if not request.json or not 'name' in request.json:
        return jsonify({"Error": "Item not found..."})
    new_item = {
        'id':items[-1]['id']+1 if items else 1, 
        'name': request.json['name'],
        'description': request.json['description'] 
    }
    items.append(new_item)
    return jsonify(new_item)

@app.route('/items/<int:item_id>', methods = ['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"]==item_id), None)
    if item is None:
        return jsonify({"Error": "Item not found..."})
    item['name'] = request.json.get('name', item['name'])
    item['description'] = request.json.get('description', item['description'])
    return jsonify(item)

@app.route('/items/<int:item_id>', methods = ['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    return jsonify({"Result": f"Item ID {item_id} has been deleted...."})

@app.route("/inside")
def inside():
    return "Inside the Flask Web App."

@app.route("/inline-html")
def inline_html():
    return "<html><h1>This is written using an inline HTML Script.</h1></html>"

@app.route("/html")
def html():
    return render_template('index.html')

##### GET-POST #####
@app.route("/get", methods = ['GET'])
def get():
    return render_template('index.html')

@app.route("/post-form", methods = ['GET', 'POST'])
def form():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        return f'<h1>Hello {name}, </h1> <h2>We have replied to your message stating - {message}.</h2>You can check the response in your inbox at {email}.'
    return render_template('form.html')

##### Variable Rule #####
@app.route("/result/<int:score>")
def result(score):
    res = ''
    if score>100:
        res = 'Invalid.'
    elif score>75:
        res = 'Good.'
    elif score>50:
        res = 'Average.'
    elif score>25:
        res = 'Bad.'
    else:
        res = 'Fail'
    return render_template('result.html', results = res)

@app.route("/result_score/<int:score>")
def result_score(score):
    res = ''
    if score>100 or score<0:
        res = 'Invalid.'
    elif score>75:
        res = 'Good.'
    elif score>50:
        res = 'Average.'
    elif score>25:
        res = 'Bad.'
    else:
        res = 'Fail'

    exp = {'Score':score, "Feedback": res}

    return render_template('result_score.html', results = exp)

@app.route("/submit_scores", methods = ['POST', 'GET'])
def submit_scores():
    total_score = 0
    if request.method == 'POST':
        sub1 = float(request.form['subject1'])
        sub2 = float(request.form['subject2'])
        sub3 = float(request.form['subject3'])
        sub4 = float(request.form['subject4'])
        sub5 = float(request.form['subject5'])
        total_score = (sub1+sub2+sub3+sub4+sub5)/5
    else:
        return render_template('submit_result.html')
    return redirect(url_for('result_conditional', score = total_score))

@app.route("/result_conditional/<int:score>")
def result_conditional(score):
    return render_template('result_conditional.html', results = score)

if __name__=='__main__':
    app.run(debug = True)