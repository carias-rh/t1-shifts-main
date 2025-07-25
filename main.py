from os import abort
import logging

from flask import Flask, render_template, request, jsonify
from random import shuffle

app = Flask(__name__)

team_members = [
    {"id": 1, "name": "Abdul Patel", "on_shift": False, "round_robin": False},
    {"id": 2, "name": "Abdur Rahman S", "on_shift": False, "round_robin": False},
    {"id": 3, "name": "Abhishek Kumar", "on_shift": False, "round_robin": False},
    {"id": 4, "name": "Bhawyya Mittal", "on_shift": False, "round_robin": False},
    {"id": 5, "name": "Jingyu Wang", "on_shift": False, "round_robin": False},
    {"id": 6, "name": "Neha Singh", "on_shift": False, "round_robin": False},
    {"id": 7, "name": "Nicol Castillo", "on_shift": False, "round_robin": False},
    {"id": 8, "name": "Satdal Maity", "on_shift": False, "round_robin": False},
    {"id": 9, "name": "Sunnykumar Choudhary", "on_shift": False, "round_robin": False},
    {"id": 10, "name": "Tianting Shi", "on_shift": False, "round_robin": False},
    {"id": 11, "name": "Veerabahu Thamizh Selvan V", "on_shift": False, "round_robin": False},
    {"id": 12, "name": "Vidyashree G", "on_shift": False, "round_robin": False},
    {"id": 13, "name": "Vikas Singh", "on_shift": False, "round_robin": False}
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sort_json_list(json_list):
    json_list.sort(key=lambda x: x['name'].lower())
    return json_list


@app.route('/')
def index():
    return render_template('index.html', team_members=team_members)


@app.route('/activate_shift', methods=['POST'])
def activate_shift():
    member_id = int(request.form['member_id'])
    for member in team_members:
        if member['id'] == member_id:
            member['on_shift'] = True
            logging.info(f"{member['name']} activated shift")
        else:
            member['on_shift'] = False
    return "Shift activated"


@app.route('/disable_shift', methods=['POST'])
def disable_shift():
    global team_members
    for member in team_members:
        if member['on_shift']:
            member['on_shift'] = False
            logging.info(f"{member['name']} disabled shift")
            break
    return "Shift disabled"


@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form['name']
    # Find the highest current ID and add 1 to it
    highest_id = max(member['id'] for member in team_members) if team_members else 0
    new_member = {"id": highest_id + 1, "name": name, "on_shift": False, "round_robin": False}
    team_members.append(new_member)
    sort_json_list(team_members)
    logging.info(f"{new_member['name']} added to the list")
    return "Member added"


@app.route('/delete_member', methods=['POST'])
def delete_member():
    member_id = int(request.form['member_id'])
    global team_members
    member_to_delete = next((member for member in team_members if member['id'] == member_id), None)
    team_members = [member for member in team_members if member['id'] != member_id]
    logging.info("{} deleted from the list".format(member_to_delete['name']))
    sort_json_list(team_members)
    return "Member deleted"


@app.route('/api/shift', methods=['GET'])
def get_current_shift():
    current_shift = next((member for member in team_members if member["on_shift"]), None)
    if current_shift:
        logging.info(f"{current_shift['name']} on shift")
    if not current_shift:
        current_shift = {"id": 0, "name": "None", "on_shift": True, "round_robin": False}
    return jsonify(current_shift)


@app.route('/api/round_robin', methods=['GET'])
def get_round_robin_shift():
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
        logging.info(f"{current_shift['name']} on shift - Round-robin")
    return jsonify(current_shift)


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
    logging.info(f"{member['name']} round robin updated to {round_robin}")
    return "Round Robin Updated"


@app.route('/activate_round_robin', methods=['POST'])
def activate_round_robin():
    for member in team_members:
        member['round_robin'] = True
    shuffle(team_members)
    logging.info("Round-robin activated")
    return "Round robin activated"


@app.route('/deactivate_round_robin', methods=['POST'])
def deactivate_round_robin():
    for member in team_members:
        member['round_robin'] = False
        member['on_shift'] = False
    sort_json_list(team_members)
    logging.info("Round-robin deactivated")
    return "Round robin deactivated"


@app.route('/api/members', methods=['GET'])
def get_members():
    return jsonify(team_members)


@app.route('/api/round_robin_status', methods=['GET'])
def get_round_robin_status():
    # Check if any member has round_robin set to True
    is_round_robin_enabled = any(member['round_robin'] for member in team_members)
    return jsonify({"round_robin_enabled": is_round_robin_enabled})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
