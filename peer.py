import json
from Blockchain import Blockchain
from Block import Block
from flask import Flask, request

app = Flask(__name__)
blockchain = Blockchain()
peers = []

@app.route("/newTransaction", methods=["POST"])
def newTransaction():
    fileData = request.get_json()
    requiredFields = ["user","aadhar", "timestamp", "v_file", "fileData", "fileSize"]
    for field in requiredFields:
        if not fileData.get(field):
            return "Transaction does not have valid fields!", 404
    blockchain.addPending(fileData)
    return "Success", 201

@app.route("/chain", methods=["GET"])
def getChain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    print("Chain Length: {0}".format(len(chain)))
    return json.dumps({"length" : len(chain), "chain" : chain})
        

@app.route("/mine", methods=["GET"])
def mineUncofirmed():
    result = blockchain.mine()
    if result:
        return "Block #{0} mined successfully.".format(result)
    else:
        return "No pending transactions."
    
@app.route("/pending_tx")
def getPending():
    return json.dumps(blockchain.pending)

@app.route("/addBlock", methods=["POST"])
def validateAndAdd():
    blockData = request.get_json()
    block = Block(blockData["index"],blockData["transactions"],blockData["prevHash"])
    hashl = blockData["hash"]
    added = blockchain.addBlock(block, hashl)
    if not added:
        return "The Block was discarded by the node.", 400
    return "The block was added to the chain.", 201

app.run(port=8800, debug=True)
