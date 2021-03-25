# PC tools for set Ethereum Network

	# Download all tools for operation Ethereum Network
		wget https://gethstore.blob.core.windows.net/builds/geth-alltools-linux-amd64-1.10.1-c2d2f4ed.tar.gz

	# Unzip dowlanding folder
		tar -xvf geth-alltools-linux-amd64-1.10.1-c2d2f4ed.tar.gz
		
	# Move special program in unzipfile folder to local bin folder
		cd geth-alltools-linux-amd64-1.10.1-c2d2f4ed
		sudo mv geth /usr/local/bin/		# Program GETH is intended for connecting in Ethereum Network
        geth version                        # Chech version GETH
		sudo mv bootnode /usr/local/bin/	# Program BOOTNODE is intended for operation BootNode in Ethereum Network
		sudo mv puppeth /usr/local/bin/		# Program PUPPETH is intended for genereting genesis block for Etereum Network

	# Removing folders that which we no longer need
		cd ..
		rm -rf geth-alltools-linux-amd64-1.10.1-c2d2f4ed.tar.gz
		rm -rf geth-alltools-linux-amd64-1.10.1-c2d2f4ed


# RPi tools for set Ethereum Network

	# Download all tools for operation Ethereum Network
		wget https://gethstore.blob.core.windows.net/builds/geth-alltools-linux-arm7-1.10.1-c2d2f4ed.tar.gz

	# Unzip dowlanding folder
		tar -xvf geth-alltools-linux-arm7-1.10.1-c2d2f4ed.tar.gz
		
	# Move special program in unzipfile folder to local bin folder
		cd geth-alltools-linux-arm7-1.10.1-c2d2f4ed
		sudo mv geth /usr/local/bin/		# Program GETH is intended for connecting in Ethereum Network
        geth version                        # Chech version GETH
		sudo mv bootnode /usr/local/bin/	# Program BOOTNODE is intended for operation BootNode in Ethereum Network
		sudo mv puppeth /usr/local/bin/		# Program PUPPETH is intended for genereting genesis block for Etereum Network

	# Removing folders that which we no longer need
		cd ..
		rm -rf geth-alltools-linux-arm7-1.10.1-c2d2f4ed.tar.gz
		rm -rf geth-alltools-linux-arm7-1.10.1-c2d2f4ed