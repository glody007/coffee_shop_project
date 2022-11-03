import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Recycler
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
GET /recyclers
    it should be a public endpoint
    it should contain only the recycler.short() data representation
returns status code 200 and json {"success": True, "recyclers": recyclers} where recyclers is the list of recyclers
    or appropriate status code indicating reason for failure
'''
@app.route("/recyclers")
def retrieve_recyclers():
    recyclers = Recycler.query.all()

    return jsonify(
        {
            "success": True,
            "recyclers": [recycler.short() for recycler in recyclers],
        }
    )


'''
GET /recyclers-detail
    it should require the 'get:recyclers-detail' permission
    it should contain the recycler.long() data representation
returns status code 200 and json {"success": True, "recyclers": recyclers} where recyclers is the list of recyclers
    or appropriate status code indicating reason for failure
'''
@app.route("/recyclers-detail")
def retrieve_recyclers_detail():
    recyclers = Recycler.query.all()

    return jsonify(
        {
            "success": True,
            "recyclers": [recycler.long() for recycler in recyclers],
        }
    )


'''
POST /recyclers
    it should create a new row in the recyclers table
    it should require the 'post:recyclers' permission
    it should contain the recycler.long() data representation
returns status code 200 and json {"success": True, "recyclers": recycler} where recycler an array containing only the newly created recycler
    or appropriate status code indicating reason for failure
'''
@app.route("/recyclers", methods=["POST"])
def create_recycler():
    body = request.get_json()

    title = body.get("title", "")
    position = body.get("position", "")

    try:

        if (title == "" or position == ""):
            abort(422)

        recycler = Recycler(title=title, position=position)
        recycler.insert()

        return jsonify(
            {
                "success": True,
                "recyclers": [recycler.long()],
            }
        )

    except:
        abort(422)


'''
PATCH /recyclers/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should update the corresponding row for <id>
    it should require the 'patch:recyclers' permission
    it should contain the recycler.long() data representation
returns status code 200 and json {"success": True, "recyclers": recycler} where recycler an array containing only the updated recycler
    or appropriate status code indicating reason for failure
'''
@app.route("/recyclers/<int:recycler_id>", methods=["PATCH"])
def patch_recycler(recycler_id):
    try:
        body = request.get_json()

        title = body.get("title", "")
        position = body.get("position", "")

        recycler = Recycler.query.filter(Recycler.id == recycler_id).one_or_none()

        if recycler is None:
            abort(404)

        if title != "":
            recycler.title = title
        
        if position != "":
            recycler.position = position

        recycler.update()

        return jsonify(
            {
                "success": True,
                "recyclers": [recycler.long()],
            }
        )

    except:
        abort(422)


'''
DELETE /recyclers/<id>
    where <id> is the existing model id
    it should respond with a 404 error if <id> is not found
    it should delete the corresponding row for <id>
    it should require the 'delete:recyclers' permission
returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or appropriate status code indicating reason for failure
'''
@app.route("/recyclers/<int:recycler_id>", methods=["DELETE"])
def delete_recycler(recycler_id):
    try:
        recycler = Recycler.query.filter(Recycler.id == recycler_id).one_or_none()

        if recycler is None:
            abort(404)

        recycler.delete()

        return jsonify(
            {
                "success": True,
                "delete": recycler_id,
            }
        )

    except:
        abort(422)


# Error Handling
'''
error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
implement error handler for 404
error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )

@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )

@app.errorhandler(403)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": error.code, "message": error.description}),
        error.code,
    )

'''
implement error handler for AuthError
error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def unauthorized(error):
    return jsonify({"success": False, "error": error.args[1], "message": error.args[0]["description"]}), error.args[1]
