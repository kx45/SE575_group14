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
    
    #NOTE: Editing a block of chain's proof will result in wrong value of proof for all the following blocks.
    def editchain(self,proof,index):
        for i in self.chain:
            if i["index"] == index:
                if proof != None:
                    i["proof"] = proof
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

@app.route('/')
def homepage():
    return render_template('index.html', data = node_identifier)

@app.route('/spend',methods=['GET'])
def getspend():
    return jsonify(blockchain.address_spend)
        
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # The sender is "0" to signify that this node has mined a new coin.
    sender = "0"
    recipient = node_identifier
    
    blockchain.new_transaction(
        sender=sender,
        recipient=recipient,
        amount = 1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response)

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    values = request.get_json(force=True)
    sender = values["sender"]
    recipient = values["recipient"]
    amount = int(values["amount"])
    #Added to take care of double spend
    #Checks that the sender has sufficient balance to even send
        
    if sender in blockchain.address_spend and blockchain.address_spend[sender] >= amount:
        index = blockchain.new_transaction(
            sender=sender,
            recipient=recipient,
            amount = amount
        )
        response = {'message': f'Transaction will be added to Block {index}'}
        return jsonify(response)
    else:
        response = {'message': 'Sender does not have sufficient balance to make transaction, sender has either already sent all the currency or it is in process'}
        return jsonify(response)

@app.route('/edit',methods=['POST'])
def edit_chain():
    values = request.get_json(force=True)
    block_no = int(values['blockno'])
    if block_no > len(blockchain.chain):
        return 'Block number does not exist'

    proof = int(values['proof'])

    blockchain.editchain(proof,block_no)
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)