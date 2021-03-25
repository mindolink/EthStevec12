# BootNode 

## What is BootNode

The first time a node connects to the network it uses one of the predefined bootnodes. Through these bootnodes a node can join the network and find other nodes. In the case of a private cluster these predefined bootnodes are not of much use. Therefore go-ethereum offers a bootnode implementation that can be configured and run in your private network [1].

[1] https://geth.ethereum.org/docs/getting-started/private-net

## Set and Run BootNode device

First must we genereted BootNode key for device that will be working as BootNode in private Ethereum Network. BootNode Hash key is only posible genereted thro comande bootnode, previously installed on this device.

        cd /EthStevec/BootNode/
        bootnode -genkey boot.key

When we generate BootNode key on device we check what is it like.

        bootnode -nodekey boot.key -writeaddress

Start and run BootNode device we use below command.

        bootnode -nodekey boot.key -verbosity 9 -addr :31313

More info about bootnode command is in source [2].

        bootnode -help

