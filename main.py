from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data - Replace this with your own data or a database later
team_members = [{"id": 1, "name": "John Doe", "on_shift": False}, {"id": 2, "name": "Jane Doe", "on_shift": False}]

@app.route('/')
def index():
    return render_template('index.html', team_members=team_members)

@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form['name']
    new_member = {"id": len(team_members) + 1, "name": name, "on_shift": False}
    team_members.append(new_member)
    return "Member added"

@app.route('/activate_shift', methods=['POST'])
def activate_shift():
    member_id = int(request.form['member_id'])
    for member in team_members:
        if member['id'] == member_id:
            member['on_shift'] = True
        else:
            member['on_shift'] = False
    return "Shift activated"

@app.route('/api/shift', methods=['GET'])
def get_current_shift():
    current_shift = next((member for member in team_members if member["on_shift"]), None)
    return jsonify(current_shift)

@app.route('/delete_member', methods=['POST'])
def delete_member():
    member_id = int(request.form['member_id'])
    global team_members
    team_members = [member for member in team_members if member['id'] != member_id]
    return "Member deleted"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
