import random
from Block import Block

class Blockchain:
    difficulty = 3
    
    def __init__(self):
        self.pending = []
        self.chain = []
        genBlock = Block(0, [], "0")
        genBlock.hash = genBlock.genHash()
        self.chain.append(genBlock)
  
    def addBlock(self, block, hashl):
        prevHash = self.lastBlock().hash
        if (prevHash == block.prevHash and self.isValid(block, hashl)):
            block.hash = hashl
            self.chain.append(block)
            return True
        else:
            return False

    def mine(self):
        if(len(self.pending) > 0):
            lastBlock = self.lastBlock()
            newBlock = Block(lastBlock.index + 1,self.pending,lastBlock.hash)
            hashl = self.p_o_w(newBlock)
            self.addBlock(newBlock, hashl)
            self.pending = []
            return newBlock.index
        else:
            return False

    def p_o_w(self, block):
        block.nonce = 0
        getHash = block.genHash()
        while not getHash.startswith("0" * Blockchain.difficulty):
            block.nonce = random.randint(0,99999999)
            getHash = block.genHash()
        return getHash

    def addPending(self, transaction):
        self.pending.append(transaction)
        
    def checkValidity(this, chain):
        result = True
        prevHash = "0"
        for block in chain:
            blockHash = block.hash
            if this.isValid(block, block.hash) and prevHash == block.prevHash:
                block.hash = blockHash
                prevHash = blockHash
            else:
                result = False
        return result

    def isValid(cls, block, blockHash):
        if(blockHash.startswith("0" * Blockchain.difficulty)):
            if(block.genHash() == blockHash):
                return True
            else:
                return False       
        else:
            return False

    def lastBlock(self):
        return self.chain[-1]
