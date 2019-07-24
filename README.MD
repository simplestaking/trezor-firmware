# WIP: Aeternity

**Disclaimer: this feature is still under development! Do not use on the aeternity mainnet**

### OS
This demo works on the following operating systems:
- Mac OS X
- Ubuntu/Debian

### Prerequisites

- Python3
- pip3
- pipenv

### Prepare the environment

Install the aeternity python sdk

    pip3 install aepp-sdk

Prepare the environment for the trezor emulator


    git clone --recursive https://github.com/simplestaking/trezor-firmware.git
    cd trezor-firmware
    git chceckout aeternity
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


### Spend transaction via Trezor T

All is set up. Now launch the demo script that will send 1 milliAE from address "ak_31USV3rnR2UXfJwLUeezNoYscezfeXg8RYDir7kQUzfCbaShi" to "ak_27GArnMWZFadMReB8q47Y1UvDFGT2g475bLBu8pv36taYLRWsU"

    cd trezor-firmware/python/trezorlib/tests/device_tests/
    python3 python3 aeternity_transaction_demo.py
