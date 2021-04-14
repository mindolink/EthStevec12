import linkEthNetwork, address, time



UserGethUnlockAccount=0
Http='http://localhost:8545'
AddrEB=address.addressConcractElectricityBilling
AddrSC=address.addressConcractSystemRegulation
PathUserInfo='./ImportData/userInfo.xlsx'
PathUserSchedule='./ImportData/userSchedule.xlsx'
PathAbiSC='./SmartConcract/abiSystemControlingConcract.json'
PathAbiEB='./SmartConcract/abiElectricityBillingConcract.json'
ethReg=linkEthNetwork.systemControling(AddrSC,PathAbiSC,Http,UserGethUnlockAccount)

i=0
while i<223:
    print(ethReg.checkBlock())

    time.sleep(1)