# SET and RUN Ethereum Network

## 1. SET Ethereum Network

Devices must have genesis block that device could start or joined to private Ethereum Network. Genesis block we can be created with program Puppeth (previous install on device) or we copy precreating sample genesis block that is stored in folder /EthStevec/GenesisBlock/.

### a) Made own Genesis Block and SET Ethereum Network Propertise
```shell
    cd /EthStevec/Network/puppeth
    geth --datadir "." init nameOfMadeGenesisBlock.json
 ```

All information how creat genesis block thro plugings pupeth is in below link.

[1] https://yenhuang.gitbooks.io/blockchain/content/chapter1/creating-the-genesis-block.html

### b) Copy alredy made Genesis Block
```shell
    cd /EthStevec/Network
    cp /EthStevec/GenesisBlocks/genesisPoA5s.json /EthStevec/Network/
    geth --datadir "." init genesisPoA5s.json
```

Important it is that all devices in system initialize a same genesis block!

## 2. RUN Ethereum Network

Run Ethereum Network is posible thro comande Geth.

### a) Device RUN Ethereum Network as MINER
```shell
        geth --datadir "." --syncmode 'full' --networkid 1994 --http --http.addr 'localhost' --http.corsdomain "https://remix.ethereum.org" --http.port 8545 --nat "any" --http.api 'web3,eth,net,personal,miner,debug,txpool,admin' --bootnodes "enode://19c8fd97b5edc99f97170462400a38c2e7c9347c1a96e15b7f623562b9d0a637e2a70b749077c38d1a07b34f802985521403eb6b69bf30806993a1623c53be10@192.168.1.107:31313" --keystore /home/pi/EthStevec/UserHash/ --password /home/pi/EthStevec/UserHash/password.sec --mine --port 50507 --ethstats node7:test@192.168.1.107:3000
```
### b) Device RUN Ethereum Network as FULL NODE
```shell
        geth --datadir "." --syncmode 'full' --networkid 1994 --http --http.addr 'localhost' --http.corsdomain "https://remix.ethereum.org" --http.port 8545 --nat "any" --http.api 'web3,eth,net,personal,miner,debug,txpool,admin' --bootnodes "enode://19c8fd97b5edc99f97170462400a38c2e7c9347c1a96e15b7f623562b9d0a637e2a70b749077c38d1a07b34f802985521403eb6b69bf30806993a1623c53be10@192.168.1.107:31313" --keystore /home/pi/EthStevec/UserHash/ --password /home/pi/EthStevec/UserHash/password.sec --mine --allow-insecure-unlock --vmdebug --port 50507 --ethstats node7:test@192.168.1.107:3000
```
### c) Device RUN Ethereum Network as LIGHT NODE
```shell
        geth --datadir "." --syncmode 'full' --networkid 1994 --http --http.addr 'localhost' --http.corsdomain "https://remix.ethereum.org" --http.port 8545 --nat "any" --http.api 'web3,eth,net,personal,miner,debug,txpool,admin' --bootnodes "enode://19c8fd97b5edc99f97170462400a38c2e7c9347c1a96e15b7f623562b9d0a637e2a70b749077c38d1a07b34f802985521403eb6b69bf30806993a1623c53be10@192.168.1.107:31313" --keystore /home/pi/EthStevec/UserHash/ --password /home/pi/EthStevec/UserHash/password.sec --light --allow-insecure-unlock --vmdebug --port 50507 --ethstats node7:test@192.168.1.107:3000
```

All information what each comande in Geth mean is bellow link.

[2] https://geth.ethereum.org/docs/interface/command-line-options