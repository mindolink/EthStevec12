# Set-Run BootNode

    # Made subfolder that will be running BootNode
        cd EthStevec/BootNode

    # Made BootNode hash key
        bootnode -genkey boot.key
    
    # Look BootNode hash key
        bootnode --nodekey=boot.key --writeaddress
    
    # Run Boot Node device
        bootnode --nodekey boot.key -verbosity 9 -addr: 31313