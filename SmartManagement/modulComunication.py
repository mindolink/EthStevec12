#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Lorenz Ammon, Jonas Schlund
"""
#https://pypi.python.org/pypi/web3/4.0.0b5
#https://web3py.readthedocs.io/en/stable/overview.html#overview-type-conversions
#https://web3py.readthedocs.io/en/stable/contracts.html
#https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI

import json
from web3 import Web3, HTTPProvider
from web3.contract import Contract#ConciseContract

class modulComunication(object):

    def __init__(self, address, host, account):
        self.contractAddress = address
        self.web3 = Web3(HTTPProvider(host))
        self.account = account
        
        abiFile = open('smartConcractRegulationABI.json')
        abi = json.load(abiFile)
        abiFile.close()
        self.contract_inst = self.web3.eth.contract(abi=abi,address=self.contractAddress)
        self.blockNumber = self.web3.eth.blockNumber
        
    def getValues(self):
        return self.contract_inst.functions.dataOutput().call({'from': self.web3.eth.accounts[self.account],'gasl': 8000000})

    def setValues(self):
        self.contract_inst.functions.dataInput(1).transaction({'from': self.web3.eth.accounts[self.account], 'gas': 8000000})
    
    def checkBlock(self):
        if self.web3.eth.blockNumber<=self.blockNumber:
            return False
        else:
            self.blockNumber=self.web3.eth.blockNumber
            return True

    def getBlock(self):
        return self.blockNumber
    
    def __del__(self):
        pass
