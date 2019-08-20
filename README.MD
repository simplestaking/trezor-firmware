# WIP: Polkadot

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
    git chceckout polkadot
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


### Polkadot Get Address

With the emulator running launch the script located in python/trezorlib/tests/device_tests

    python3 polkadot_get_address.py

### Polkadot transaction demo

Sending miliDOTs from:

5Fg1HwmobhcwGVQDe52Tm48gUdtnEFZ9d18xhMGMRvqq9sGw - m/44'/357'/0' - 9fa0fbd0526becc1f653a1898d18946c0b702a9d02caa262652a612b74012383 (== public_key == account_id)

to

5D4eo8YhXBPBVqVqaFFzPsomCZxMjphUjj2BJ213QzCgdmDk - m/44'/357'/1' - 2c31ede147b6ba608a5f89bf218cb9962914895980b1881a4e4b7bd3a0faa2a6 (== public_key == account_id)

In the polkadot_sign_tx.py script, increment the nonce field by one and launch the script

    python3 polkadot_sign_tx.py

Next, go to https://polkadot.js.org/apps/#/toolbox and select author endpoint and submitExtrinsic method. Copy the
Balance transfer extrinsic output from the previous script to send the transaction to the live node.