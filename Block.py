from hashlib import sha256

class Block:
    def __init__(self, index, transactions, prevHash):
        self.index = index
        self.transactions = transactions
        self.prevHash = prevHash
        self.nonce = 0

    def genHash(self):
        allDataCombined = str(self.index) + str(self.nonce) + self.prevHash + str(self.transactions)
        return sha256(allDataCombined.encode()).hexdigest()
    
    def addT(self, t):
        self.transactions.append(t)
