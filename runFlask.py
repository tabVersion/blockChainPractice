import blockChain

from flask import Flask, jsonify, request
import json
from textwrap import dedent
from time import time 
from uuid import uuid4

# 实例化节点
app = Flask(__name__)

# 为此节点创建一个独一无二的地址
node_identifier = str(uuid4()).replace('-', '')

#实例化blockChain类
BlockChain = blockChain.blockChain()

@app.route('/mine', methods = ['GET'])
def mine():
    last_block = BlockChain.chain[-1]
    last_proof = last_block['proof']
    proof = BlockChain.poW(last_proof)

    # "0"代表系统发出的奖励
    BlockChain.newTransaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1,
    )

    # 将新生成的块加入本地的链
    block = BlockChain.newBlock(proof, None)

    response = {
        'message': "new block forged",
        'index': block['index'],
        'transaction': block['transaction'],
        'proof': block['proof'],
        'previousHash': block['previousHash'],
    }

    return jsonify(response), 200

@app.route('/transaction/new', methods = ['POST'])
def newTransaction():
    value = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in value for k in required):
        return 'missing values', 400

    index = BlockChain.newTransaction(
        value['sender'], value['recipient'], value['amount']
    )
    response = {
        'message': "transaction will be added to block"
    }

    return jsonify(response), 201


@app.route('/chain', methods = ['GET'])
def fullChain():
    # 返回整条链
    response = {
        'chain': BlockChain.chain,
        'length': len(BlockChain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
