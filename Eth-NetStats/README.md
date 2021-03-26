# Ethereum Network Stats (Eth-NetStats)

## 1. What is Eth-NetStat server

This is a visual interface for tracking ethereum network status. It uses WebSockets to receive stats from running nodes and output them through an angular interface. More abaout this user interface is in [[1]](https://github.com/cubedro/eth-netstats).

![Screenshot](https://raw.githubusercontent.com/cubedro/eth-netstats/master/src/images/screenshot.jpg?v=0.0.6 "Screenshot")

</br>

## 2. Set Eth-NetStats server

Install Eth-NetStats thro bellow comands.

```shell
        cd /Eth-NetStats
	    git clone https://github.com/cubedro/eth-netstats
	    cp -r /Eth-NetStats/eth-netstats /EthStevec/Eth-NetStats
        rm -rf eth-netstats
        cd /EthStevec/NetStats
	    npm install 
        sudo npm install -g grunt-cli
        grunt all
```

</br>

## 3. Run Eth-NetStats server

Run Eth-NetStats thro bellow comand.

```shell
        WS_SECRET=stevec && npm start
```

See the interface at <http://localhost:3000>