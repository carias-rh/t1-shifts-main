from os import abort

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data - Replace this with your own data or a database later
team_members = [
    {"id": 1, "name": "Abhishek Kumar", "on_shift": False, "round_robin": False},
    {"id": 2, "name": "Bhawyya Mittal", "on_shift": False, "round_robin": False},
    {"id": 3, "name": "Mohammed Tahmeed", "on_shift": False, "round_robin": False},
    {"id": 4, "name": "Neha Singh", "on_shift": False, "round_robin": False},
    {"id": 5, "name": "Nicol Castillo (LX)", "on_shift": False, "round_robin": False},
    {"id": 6, "name": "Ranita Saha", "on_shift": False, "round_robin": False},
    {"id": 7, "name": "Roberto Casarrubios", "on_shift": False, "round_robin": False},
    {"id": 8, "name": "Shashi Singh", "on_shift": False, "round_robin": False},
    {"id": 9, "name": "Veerabahu Thamizh Selvan V", "on_shift": False, "round_robin": False},
    {"id": 10, "name": "Vidyashree G", "on_shift": False, "round_robin": False},
    {"id": 11, "name": "Vikas Singh", "on_shift": False, "round_robin": False},
    {"id": 12, "name": "Waseem Patel", "on_shift": False, "round_robin": False}
]


@app.route('/')
def index():
    return render_template('index.html', team_members=team_members)

@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form['name']
    new_member = {"id": len(team_members) + 1, "name": name, "on_shift": False, "round_robin": False}
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

@app.route('/disable_shift', methods=['POST'])
def disable_shift():
    global team_members
    for member in team_members:
        if member['on_shift']:
            member['on_shift'] = False
            break
    return "Shift disabled"


@app.route('/api/shift', methods=['GET'])
def get_current_shift():
    global team_members
    current_shift = next((member for member in team_members if member["on_shift"]), None)

    if not current_shift:
        # If no one is on shift, select the first member with round_robin = True
        current_shift = next((member for member in team_members if member["round_robin"]), None)
        if current_shift:
            current_shift['on_shift'] = True
        else:
            current_shift = {"id": 0, "name": "None", "on_shift": True, "round_robin": False}
    elif next((member for member in team_members if member["round_robin"]), None):
        # If round robin is enabled, shift to the next member
        current_index = team_members.index(current_shift)
        current_shift['on_shift'] = False
        next_member = None
        for i in range(current_index + 1, current_index + len(team_members)):
            if team_members[i % len(team_members)]['round_robin']:
                next_member = team_members[i % len(team_members)]
                break
        if next_member:
            next_member['on_shift'] = True
            current_shift = next_member
    return jsonify(current_shift)

    return jsonify(current_shift)

@app.route('/delete_member', methods=['POST'])
def delete_member():
    member_id = int(request.form['member_id'])
    global team_members
    team_members = [member for member in team_members if member['id'] != member_id]
    return "Member deleted"


@app.route('/update_round_robin', methods=['POST'])
def update_round_robin():
    if 'member_id' not in request.form or 'round_robin' not in request.form:
        abort(400)  # Bad request
    member_id = int(request.form['member_id'])
    round_robin = request.form['round_robin'] == 'true'
    for member in team_members:
        if member['id'] == member_id:
            member['round_robin'] = round_robin
            break
    return "Round Robin Updated"


@app.route('/deactivate_round_robin', methods=['POST'])
def deactivate_round_robin():
    for member in team_members:
        member['round_robin'] = False
    return "Round robin deactivated"



if __name__ == '__main__':
    app.run(host="0.0.0.0")
