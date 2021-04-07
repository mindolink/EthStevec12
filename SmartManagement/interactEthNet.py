import json
from web3 import Web3, HTTPProvider
from web3.contract import Contract


class interactEthNet(object):
    
    def __init__(self, address, host, account):
        self.contractAddress = address
        self.web3 = Web3(HTTPProvider(host))
        self.account = account
        
        abiFile = open('sola.json')
        abi = json.load(abiFile)
        abiFile.close()
        self.contract_inst = self.web3.eth.contract(abi=abi,address=self.contractAddress)

        self.blockNumber = self.web3.eth.blockNumber


    def getValues(self):
        return self.contract_inst.functions.dataOutput().call({'from': self.web3.eth.accounts[self.account],'gas': 400000})

    def setValues1(self,vrednost):
        
        self.contract_inst.functions.dataInput1(vrednost).transact({'from': self.web3.eth.accounts[self.account], 'gas': 200000})

    def setValues2(self,vrednost):

        self.contract_inst.functions.dataInput2(vrednost).transact({'from': self.web3.eth.accounts[self.account], 'gas': 400000})


    def checkBlock(self):
        if self.web3.eth.blockNumber<=self.blockNumber:
            return False
        else:
            self.blockNumber=self.web3.eth.blockNumber
            return True
                   
    def getBlock(self):
        return self.blockNumber