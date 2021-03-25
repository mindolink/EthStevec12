# Set and run Bootnode

    # Made subFolder that will be running Ethereum Network
        cd EthStevec
        mkdir Network
        cd Network

    # Copy made genesi file from folder GenesisBlock to folder Network
        cp /home/pi/EthStevec/GenesisBlocks/genesisPoA5s.json  /home/pi/EthStevec/Network/

    # Set propertise for run Ethereum Network
        cd /home/pi/EthStevec/Network/PoA5s/
        geth --datadir "." init genesisPoA5s.json

