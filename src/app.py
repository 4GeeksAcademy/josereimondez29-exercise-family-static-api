"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

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

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

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
    print(body)
    return jsonify("add member completed"), 200

#### GET 1 ####
@app.route('/members/<int:member_id>', methods=['GET'])
def get_specific_member(member_id): #whatever we put as id after the endpoint we need to also pass it as a parameter here
    single_member = jackson_family.get_member(member_id) # this is the method for getting a particular family member from the list. 
    if single_member:
        response_body = {"message": "family member found",
                        "results": single_member }
        return jsonify(response_body), 200
    response_body = {"message": "family member not found",
                            "results": [] }
    return jsonify(response_body), 404
    
#### DELETE ####
@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):   #whatever we put as id after the endpoint we need to also pass it as a parameter here   
    deleted_member = jackson_family.delete_member(member_id) # this is the method for deleting a family member from the list. 
    if deleted_member:
        response_body = {"message": "family member deleted",
                        "results": deleted_member }
        return jsonify(response_body), 200
    response_body = {"message": "family member not found",
                    }
    return jsonify(response_body), 404

    
#### PUT ####
@app.route('/members/<int:member_id>', methods=['PUT'])
def handle_update_member(member_id):   #whatever we put as id after the endpoint we need to also pass it as a parameter here   
      # Get the updated member data from the request body
    updated_member_data = request.json
    updated_member = jackson_family.update_member(member_id, updated_member_data) # this is the method for updating a family member from the list. 
    if updated_member:
        response_body = {"message": "family member updated",
                        "results": updated_member }
        return jsonify(response_body), 200
    response_body = {"message": "family member not found",
                    }
    return jsonify(response_body), 404
# REMEMBER: When sending a PUT request with JSON data, make sure to set the in Postman headers the "Content-Type" (key) as "application/json" (value)!

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
