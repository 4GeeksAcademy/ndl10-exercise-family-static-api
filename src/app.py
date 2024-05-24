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
print(jackson_family)

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
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200



@app.route('/members/<int:id_member>', methods=['GET'])
def handle_get_member(id_member):
    member = jackson_family.get_member(id_member)
    if member is None:
        return jsonify({ 'ERROR': 'member not found or does not exist'}),404
    response = member
    return jsonify(response),200

@app.route('/member', methods=['POST'])
def handle_post_member():
        body = request.json
        jackson_family.add_member(body)
        return jsonify(body), 200
    
    # {"id": Int,
    # "first_name": String,
    # "age": Int,
    # "lucky_numbers": []
    # }

@app.route('/members/<int:id_member>', methods=['DELETE'])
def handle_delete_member(id_member):
    deleted_member= jackson_family.delete_member(id_member)
    if deleted_member is None:
        return jsonify({"ERROR: not possible"}), 404
    else: return jsonify(deleted_member), 200
 

    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
