"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#Post User
@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    new_member = {
            "id": jackson_family._generateId(),
            "first_name": body["first_name"],
            "last_name": jackson_family.last_name,
            "age": body["age"],
            "lucky_numbers": body["lucky_numbers"]
        }
    jackson_family.add_member(new_member)
    return jsonify("add member completed"), 200

#Get user by ID
@app.route('/member/<int:id>', methods=['GET'])
def get_specific_member(id):
    member = jackson_family.get_member(id)
    if member:
        member['name'] = member['first_name']  
        return jsonify(member), 200
    return jsonify({"message": "Member not found"}), 404

#Delete user by ID
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    deleted_member = jackson_family.delete_member(id)
    if deleted_member:
        return jsonify({"done": True}), 200  
    return jsonify({"message": "Member not found"}), 404

#Update member by ID
@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    updated_member_data = request.json
    updated_member = jackson_family.update_member(id, updated_member_data)
    if updated_member:
        return jsonify({"message": "Family member updated", "results": updated_member}), 200
    return jsonify({"message": "Family member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


