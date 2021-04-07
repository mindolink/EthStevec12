import json
from web3 import Web3, HTTPProvider
from web3.contract import Contract


class systemControling(object):

    def __init__(self, address, host, account):
        self.contractAddress = address
        self.web3 = Web3(HTTPProvider(host))
        self.account = account
        
        abiFile = open('./abiRegulatorSmartConcract.json')
        abi = json.load(abiFile)
        abiFile.close()
        self.contract_inst = self.web3.eth.contract(abi=abi,address=self.contractAddress)
        self.blockNumber = self.web3.eth.blockNumber
        self.gas=40000000

    def getTariffNumber(self):
        return self.contract_inst.functions.TariffNumber().call({'from': self.web3.eth.accounts[self.account],'gas': self.gas})

    def getSystemNeedsEnergy(self):
        return self.contract_inst.functions.SystemNeedsEnergy().call({'from': self.web3.eth.accounts[self.account],'gas': self.gas})

    def getSystemRuning(self):
        return self.contract_inst.functions.SystemNeedsEnergy().call({'from': self.web3.eth.accounts[self.account],'gas': self.gas})

    def getAssignedPower(self):
        return self.contract_inst.functions.AssignedPower().call({'from': self.web3.eth.accounts[self.account],'gas': self.gas})

    def sendRequiredPower(self,Preq):
        self.contract_inst.functions.RequiredPower(Preq).transact({'from': self.web3.eth.accounts[self.account], 'gas': self.gas})

    def getUserNumber(self):
        self.contract_inst.functions.RequiredPower(Preq).transact({'from': self.web3.eth.accounts[self.account], 'gas': self.gas})


    def checkBlock(self):
        if self.web3.eth.blockNumber<=self.blockNumber:
            return False
        else:
            self.blockNumber=self.web3.eth.blockNumber
            return True

    def getBlock(self):
        return self.blockNumber


class electricityBilling(object):
    
    def __init__(self, addressRegulatorContract, host, account):
        self.contractAddress = addressRegulatorContract
        self.web3 = Web3(HTTPProvider(host))
        self.account = account
        
        abiFile = open('sola.json')
        abi = json.load(abiFile)
        abiFile.close()
        self.contract_inst = self.web3.eth.contract(abi=abi,address=self.contractAddress)
        self.blockNumber = self.web3.eth.blockNumbe
        self.gas=4000000

    def sendEnergyStatus(self,Preq):
        self.contract_inst.functions.RequiredPower(Preq).transact({'from': self.web3.eth.accounts[self.account], 'gas': gas})

    def getWalletCashBalanceEuro(self):
        CENT=self.contract_inst.functions.getWalletCashBalanceCent().call({'from': self.web3.eth.accounts[self.account],'gas': self.gas})
        EURO=CENT/100
        abbEURO=("%.2f" % EURO)
        return(abbEURO)
