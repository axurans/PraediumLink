from hashlib import sha3_512

class Block:
    def __init__(self, index, transactions, prevHash):
        self.index = index
        self.transactions = transactions
        self.prevHash = prevHash
        self.nonce = 0

    def genHash(self):
        allDataCombined = str(self.index) + str(self.nonce) + self.prevHash + str(self.transactions)
        return sha3_512(allDataCombined.encode()).hexdigest()
    
    def addT(self, t):
        self.transactions.append(t)
