from flask import Flask, render_template, request, redirect, url_for
from hashlib import sha256
from datetime import datetime

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()
        
    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}".encode()
        return sha256(block_string).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        
    def create_genesis_block(self):
        genesis_block = Block(0, str(datetime.now()), "Genesis Block", "0")
        self.chain.append(genesis_block)
        
    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.now()), transactions, previous_block.hash)
        self.chain.append(new_block)
        
    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Create a blockchain instance
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    stock_name = request.form['stock_name']
    stock_price = request.form['stock_price']
    
    transactions = [{"stock": stock_name, "price": float(stock_price)}]
    blockchain.add_block(transactions)
    
    return redirect(url_for('index'))

@app.route('/chain')
def view_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        })
    return render_template('chain.html', chain=chain_data)

if __name__ == '__main__':
    app.run(debug=True)
