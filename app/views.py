import json
import os
import requests
from flask import render_template, redirect, request, send_file
from werkzeug.utils import secure_filename
from app import app
from timeit import default_timer as timer

requestTx = []
files = {}
aadhar_name_mapping = {}
UPLOAD_FOLDER = "app/static/Uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ADDR = "http://127.0.0.1:8800"

def getTxReq():
    global requestTx
    chainAddr = "{0}/chain".format(ADDR)
    resp = requests.get(chainAddr)
    if resp.status_code == 200:
        content = []
        chain = json.loads(resp.content.decode())
        for block in chain["chain"]:
            for trans in block["transactions"]:
                trans["index"] = block["index"]
                trans["hash"] = block["prevHash"]
                content.append(trans)
        requestTx = sorted(content, key=lambda k: k["hash"], reverse=True)

@app.route("/")
def index():
    getTxReq()
    return render_template("index.html", title="RealEstateFileStorage", subtitle="A Blockchain Real Estate File Storage", node_address=ADDR, request_tx=requestTx)

@app.route("/submit", methods=["POST"])
def submit():
    start = timer()
    user = request.form["user"]
    aadhar = request.form["aadhar"]
    timestamp = request.form["timestamp"]
    upFile = request.files["v_file"]

    # Check if Aadhar card number or name has already been submitted
    if aadhar in aadhar_name_mapping:
        return "Aadhar card number already associated with a name."
    if user in aadhar_name_mapping.values():
        return "Name already associated with an Aadhar card number."

    aadhar_name_mapping[aadhar] = user

    upFile.save(os.path.join("app/static/Uploads/", secure_filename(upFile.filename)))
    files[upFile.filename] = os.path.join(app.root_path, "static", "Uploads", upFile.filename)
    file_states = os.stat(files[upFile.filename]).st_size
    post_object = {
        "user": user,
        "aadhar": aadhar,
        "timestamp": timestamp,
        "v_file": upFile.filename,
        "fileData": str(upFile.stream.read()),
        "fileSize": file_states
    }
   
    address = "{0}/newTransaction".format(ADDR)
    requests.post(address, json=post_object)
    end = timer()
    print(end - start)
    return redirect("/")

@app.route("/submit/<string:variable>", methods=["GET"])
def download_file(variable):
    p = files[variable]
    return send_file(p, as_attachment=True)
