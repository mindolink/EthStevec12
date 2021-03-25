# Set and run NetStat

    # Install EthNetStats server for tracking trafic in Ethereum NEtwork
        cd
	    git clone https://github.com/cubedro/eth-netstats
	    cp -r /home/pi/eth-netstats /home/pi/EthStevec/NetStats
        rm -rf eth-netstats
        cd /home/pi/EthStevec/NetStats
	    npm install 
        sudo npm install -g grunt-cli
        grunt all

    # Run EthNetStats server 
        WS_SECRET=stevec&& npm start

    # More info on official website https://github.com/cubedro/eth-netstats