from flask import Flask, request, Response
import dbhelpers
import json
import traceback
import sys

app = Flask(__name__)


@app.get("/api/villain")
def get_villains():
    villains = dbhelpers.run_select_statement(
        "SELECT name, description, image_url, id FROM villain", [])

    if(villains == None):
        return Response("Failed to GET villains", mimetype="text/plain", status=500)
    else:
        villain_json = json.dumps(villains, default=str)
        return Response(villain_json, mimetype="application/json", status=200)


@app.post("/api/villain")
def post_villain():
    try:
        villain_name = request.json['name']
        villain_desc = request.json['desc']
        villain_img = request.json['img']
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")
        return Response("Data Error", mimetype="text/plain", status=400)
    villain_id = dbhelpers.run_insert_statement("INSERT INTO villain(name, description, image_url) VALUES (?,?,?)",
                                                [villain_name, villain_desc, villain_img])
    if(villain_id == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        villain = [villain_name, villain_desc, villain_img, villain_id]
        villain_json = json.dumps(villain, default=str)
        return Response(villain_json, mimetype="application/json", status=201)


@app.delete("/api/villain")
def delete_villain():
    try:
        villain_id = int(request.json['id'])
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")
        return Response("Data Error", mimetype="text/plain", status=400)

    rows = dbhelpers.run_delete_statement(
        "DELETE FROM villain WHERE id=?", [villain_id, ])
    if(rows == 1):
        return Response("Villain Deleted", mimetype="text/plain", status=200)
    else:
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5015)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()
