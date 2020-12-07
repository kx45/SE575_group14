import hashlib
import json
from time import time

class Blockchain(object):
    chain = []
    current_transactions = []
    address_spend = {}

    def __init__(self):
        #initializing a single block to start with
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
       
        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    #Edits a block of the chain
    #NOTE: Editing a block of chain's proof will result in wrong value of proof for all the following blocks.
    def editchain(self,proof,index):
        for i in self.chain:
            if i["index"] == index:
                # if sender != None:
                #     if len(i["transactions"]) != 0:
                #         i["transactions"][0]['sender'] = sender
                if proof != None:
                    i["proof"] = proof
                # if recipient != None:
                #     if len(i["transactions"]) != 0:
                #         i["transactions"][0]['recipient'] = recipient
                i["timestamp"] = time()    

    def new_transaction(self, sender, recipient,amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        #Edits to the address_spend which keeps track of balance for each address
        if sender != "0" and sender in self.address_spend:
            self.address_spend[sender] -= amount
        elif sender != "0":
            self.address_spend[sender] = amount
                
        if recipient in self.address_spend:
            self.address_spend[recipient] += amount
        else:
            self.address_spend[recipient] = amount
        print(self.address_spend)

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]

    #helper for the Proof of Work test
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    def helper_transaction(self,sender, send_amount):
        amount = 0
        for i in blockchain.current_transactions:
            if i["recipient"] == sender:
                amount += i["amount"]
            if i["sender"] == sender:
                amount -= i["amount"]
        if amount >= send_amount:
            return True
        else:
            return False

from flask import Flask, jsonify, request, render_template
from textwrap import dedent
from uuid import uuid4

app = Flask(__name__, static_folder='public', static_url_path='')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

#Example code for connecting it with front-end html
@app.route('/')
def homepage():
    return render_template('index.html', data = node_identifier)



#TODO: Delete this before submitting, temp method to get values
@app.route('/spend',methods=['GET'])
def getspend():
    return jsonify(blockchain.address_spend)
        
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    sender = "0"
    recipient = node_identifier
    
    blockchain.new_transaction(
        sender=sender,
        recipient=recipient,
        amount = 1
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# TODO: error check in front-end any values missing 
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    values = request.get_json(force=True)

    sender = values["sender"]
    recipient = values["recipient"]
    amount = values["amount"]
    
    #Added to take care of double spend
    #Checks that the sender has sufficient balance to even send
        
    if sender in blockchain.address_spend and blockchain.address_spend[sender] >= amount:
        index = blockchain.new_transaction(
            sender=sender,
            recipient=recipient,
            amount = amount
        )
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response), 201
    else:
        return 'Recipient does not have sufficient amount to make transaction, recipient has either already sent all the currency or it is in process'

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

#TODO: add error check in front-end to make sure that blockno and one other parameter is provided
@app.route('/edit',methods=['POST'])
def edit_chain():
    values = request.get_json(force=True)
    block_no = values['blockno']
    if block_no > len(blockchain):
        return 'Block number does not exist'
    #Need to think a better way to edit transaction cases.
    # if "sender" in values:
    #     sender = values['sender']
    # else:
    #     sender = None

    proof = values['proof']
    # if "recipient" in values:
    #     recipient = values['recipient']
    # else:
    #     recipient = None
    blockchain.editchain(proof,block_no)
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 201


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)