from time import time 
import json
import hashlib

difficultRate = 1

class blockChain(object):
    def __init__(self):
        self.chain = []
        self.currentTransaction = []

        self.newBlock(previousHash = 1, proof = 100)

    def newBlock(self, proof, previousHash = None):
        block = {
            'index': len(self.chain) + 1,
            'timeStamp': time(),
            'transaction': self.currentTransaction,
            'proof': proof,
            'previousHash': previousHash,
        }
        self.currentTransaction = []
        self.chain.append(block)
        return block
    
    def newTransaction(self, sender, recipient, amount):
        self.currentTransaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.lastBlock['index'] + 1 

    @staticmethod
    def hash(block):
        blockString = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(blockString).hexdigest()
    
    @property
    def lastBlock(self):
        return self.chain[-1]

    def poW(self, lastProof):
        proof = 0
        while self.validProof(proof, lastProof) is False:
            proof += 1

        return proof

    @staticmethod
    def validProof(proof, lastProof):
        temp = (str(lastProof) + str(proof)).encode()
        tempHash = hashlib.sha256(temp).hexdigest()

        ans = ""
        for i in range(difficultRate):
            ans += "0"
        return tempHash[:difficultRate] == ans
