# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib.tezos import sign_delegator_op
from trezorlib.tezos import control_staking
from trezorlib.tezos import get_address
from trezorlib.tools import parse_path
from trezorlib.protobuf import dict_to_proto
from trezorlib.messages import TezosSignDelegatorOp
from trezorlib import messages as proto
from trezorlib.exceptions import TrezorFailure
from trezorlib import device

from .common import TrezorTest

TEZOS_PATH = "m/44'/1729'/10'"              #path is set to address 10 due testing on tezos zeronet


@pytest.mark.tezos
@pytest.mark.skip_t1
class TestMsgTezosSignDelegatorOp(TrezorTest):

    def setup_mnemonic_pin_nopassphrase(self):
        # we need a pin and also the 12*all mnemonic
        self._setup_mnemonic(mnemonic=TrezorTest.mnemonic_all, pin=TrezorTest.pin4)

    def test_tezos_delegator_sign_block(self):
        self.setup_mnemonic_pin_nopassphrase()

        control_staking(self.client, True)
        res = self.sign_block_header()

        assert res.signature == "edsigtXzJQLfhaPk3Hd3UGYy9q88LyDPFg9Fx8ofULYVSZKKeSzHUH7gzUzVDtcBQPEFL5Uxo31qLWqn6As4pKcT7cj4R1HCFFF"

    def test_tezos_delegator_sign_endorsement(self):
        self.setup_mnemonic_pin_nopassphrase()

        control_staking(self.client, True)
        res = self.sign_endorsement()

        assert res.signature == "edsigtzzRYUQ5pEwri2gWRPyVpGKsazK8qaRaGiTwmaVET5KMZ16aC78YVDg7ym5NMLt6FnhMmUD96CEa9zVnGg7tcpzAphK8XM"

    def test_tezos_delegator_sign_block_nonce(self):
        self.setup_mnemonic_pin_nopassphrase()

        control_staking(self.client, True)
        res = self.sign_block_with_nonce()

        assert res.signature == "edsigtqLXgHP3pzzYDLSVgN9ie1NV7E9L671ZbWBLyNYmsTgj1kZk8WAvto4YrtQLK4WQ1eEuye4uKHj3CuWsyfGsBY7LJTf9uz"

    def test_tezos_staking_start(self):
        self.setup_mnemonic_allallall()
        # with no PIN
        with pytest.raises(TrezorFailure):
            res = control_staking(self.client, True)
            assert isinstance(res, proto.Failure)

        device.wipe(self.client)

        # with PIN
        self.setup_mnemonic_pin_nopassphrase()

        res = control_staking(self.client, True)
        assert isinstance(res, proto.Success)

    def test_tezos_stakaing_not_permited(self):
        self.setup_mnemonic_pin_nopassphrase()

        with pytest.raises(TrezorFailure):
            self.sign_endorsement()

    def test_tezos_deny_operation(self):
        """
        When in staking mode, only the messages needed for the signing operation are allowed
        """
        self.setup_mnemonic_pin_nopassphrase()
        control_staking(self.client, True)

        with pytest.raises(TrezorFailure):
            path = parse_path(TEZOS_PATH)
            get_address(self.client, path, show_display=True)
        device.wipe(self.client)

    def sign_block_with_nonce(self):
        res = sign_delegator_op(
            self.client,
            parse_path(TEZOS_PATH),
            dict_to_proto(
                TezosSignDelegatorOp,
                {
                    "magic_byte": "01",
                    "chain_id": "e3e15e60",
                    "block_header": {
                        "level": 0x00057720,
                        "proto": 1,
                        "predecessor": "346995bd69149d9d0dd41d3e865609ec19e0dc66b9fd98ace40b16f3e600b052",
                        "timestamp": 0x000000005bf1bdd1,
                        "validation_pass": 4,
                        "operations_hash": "a271cd9929166acff9fd0220976e14824aa59d400e91bd0c9b6a8b668e9257ba",
                        "bytes_in_field_fitness": 0x11,
                        "bytes_in_next_field": 0x1,
                        "fitness": "00000000080000000000ab7a4e",
                        "context": "12e8cb836a06c2f238be053de2055cc5ba0e1d023b67b8974e7dd8965b449d3c",
                        "priority": 0,
                        "proof_of_work_nonce": "6516f8698fde1399",
                        "presence_of_field_seed_nonce_hash": True,
                        "seed_nonce_hash": "40bcfc9798526a8549acdbbdf45402690a1e580c43938813a84a9da7d5ee94f9"
                    },
                },
            ),
        )
        return res

    def sign_block_header(self):
        res = sign_delegator_op(
            self.client,
            parse_path(TEZOS_PATH),
            dict_to_proto(
                TezosSignDelegatorOp,
                {
                    "magic_byte": "01",
                    "chain_id": "3bb717ee",
                    "block_header": {
                        "level": 0x0002c685,
                        "proto": 1,
                        "predecessor": "aac40470fa66b3ca657f46dba10df233837e14c31e1193505e056ea2116cf5b5",
                        "timestamp": 0x000000005c361155,
                        "validation_pass": 4,
                        "operations_hash": "cd38e4e70d5668a28b65dddb6fa82edf8f631553895735625cf0d183b7b05d6e",
                        "bytes_in_field_fitness": 0x11,
                        "bytes_in_next_field": 0x1,
                        "fitness": "000000000800000000005a62a2",
                        "context": "877920f3904dd8619b2fb66ebb323cc3b70a7f03e4baaf4a9f0a252cb0e501e0",
                        "priority": 0,
                        "proof_of_work_nonce": "3b3fb8058de0aca2",
                        "presence_of_field_seed_nonce_hash": False,
                    },
                },
            ),
        )
        return res

    def sign_endorsement(self):
        res = sign_delegator_op(
            self.client,
            parse_path(TEZOS_PATH),
            dict_to_proto(
                TezosSignDelegatorOp,
                {
                    "magic_byte": "02",
                    "chain_id": "e3e15e60",
                    "endorsement": {
                        "branch": "53f552f0e22a364259848b1e13f124cbae330569f10777e9fa1b1cd8ea57dac0",
                        "tag": 0,
                        "level": 0x00055507,
                    },
                },
            ),
        )
        return res
