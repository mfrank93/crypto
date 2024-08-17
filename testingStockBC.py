# import sha256 hash and datetime
from hashlib import sha256
from datetime import datetime

# Class block will define index, timestamp, transations, previous_hash, self hash
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()
    # This class has a method called computer hash: creates a string and returns the encrypted part
    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}".encode()
        return sha256(block_string).hexdigest()

# Blockchain class begins the adding of the blocks
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    # first block- create a 0 block and fill in the block constrctor, then append
    def create_genesis_block(self):
        genesis_block = Block(0, str(datetime.now()), "Genesis Block", "0")
        self.chain.append(genesis_block)
    # add a block- find previous (self.chain -1), create a new block and append new block to chain
    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.now()), transactions, previous_block.hash)
        self.chain.append(new_block)
    # is the blockchain valid?- return true for every value
    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
# create a transaction input prompt
def create_transaction():
    transactions = []
    while True:
        stock_name = input("Enter stock name (or 'done' to finish): ")
        if stock_name.lower() == 'done':
            break
        stock_price = float(input("Enter stock price: "))
        transactions.append({"stock": stock_name, "price": stock_price})
    return transactions

# Create a blockchain instance which runs when the program starts
blockchain = Blockchain()

# Add transactions to the blockchain, if true, new transaction, add a block and print out
while True:
    transactions = create_transaction()
    if not transactions:
        break
    blockchain.add_block(transactions)
    print("Block added to the blockchain.")
    print("Blockchain valid?", blockchain.is_valid_chain())

    for block in blockchain.chain:
        print(vars(block))
    # add another block if Y
    another = input("Add another block? (y/n): ")
    if another.lower() != 'y':
        break

    