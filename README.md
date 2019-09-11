# WIP: Cosmos

**Disclaimer: this feature is still under development**

### OS
This demo works on the following operating systems:
- Mac OS X
- Ubuntu/Debian

### Prerequisites

- Python3
- pip3
- pipenv

### Prepare the environment

Prepare the environment for the trezor emulator


    git clone --recursive https://github.com/simplestaking/trezor-firmware.git
    cd trezor-firmware
    git chceckout cosmos
    pipenv sync
    cd python
    pipenv run make gen
    python3 setup.py develop
    cd ../core
    pipenv run make build_unix



### Setup a test mnemonic seed on the emulator

Launch the emulator

    ./emu.sh
    
In a new terminal, type:

    trezorctl recovery-device

This will ask you to enter a new bip39 mnemonic. Select the 12 word choice and enter the word "all" 12 times.


### Install gaia cli to connect to the testnet

Install golang. For this project **version 1.12.1+** is needed. Follow the official instructions on https://golang.org/doc/install

Next set up the environment variables:

    mkdir -p $HOME/go/bin
    echo "export GOPATH=$HOME/go" >> ~/.bash_profile
    echo "export GOBIN=$GOPATH/bin" >> ~/.bash_profile
    echo "export PATH=$PATH:$GOBIN" >> ~/.bash_profile
    source ~/.bash_profile

Next we install gaia binaries

    mkdir -p $GOPATH/src/github.com/cosmos
    cd $GOPATH/src/github.com/cosmos
    git clone https://github.com/cosmos/cosmos-sdk
    cd cosmos-sdk && git checkout master
    make tools install

Verify that everything is ok by executing

    gaiacli version --long

The output should be similar to

    cosmos-sdk: 0.33.0
    git commit: 7b4104aced52aa5b59a96c28b5ebeea7877fc4f0
    vendor hash: 5db0df3e24cf10545c84f462a24ddc61882aa58f
    build tags: netgo ledger
    go version go1.12 linux/amd64

Next thing is to set up a node or connect to a trusted remote node, we do the later.

    gaiacli config node http://46.101.160.245:26657
    gaiacli config trust-node true

### Transaction demo

All is set up! Now just run the script cosmos_test.py in tests/device_tests and it will send 1000 tokens from the trezor address cosmos1evwx7u5xllw5fvyl6wpkmqszl6ql6ta8xd06rn (m/44'/118'/0')