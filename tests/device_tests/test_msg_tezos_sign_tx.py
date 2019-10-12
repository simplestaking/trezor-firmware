# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
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

from trezorlib import messages, tezos
from trezorlib.protobuf import dict_to_proto
from trezorlib.tools import parse_path

TEZOS_PATH = parse_path("m/44'/1729'/0'")
TEZOS_PATH_10 = parse_path("m/44'/1729'/10'")


@pytest.mark.altcoin
@pytest.mark.tezos
@pytest.mark.skip_t1
class TestMsgTezosSignTx:
    def input_flow(self, debug, num_pages):
        yield
        for _ in range(num_pages - 1):
            debug.swipe_down()
        debug.press_yes()

    def test_tezos_sign_tx_proposal(self, client):
        with client:
            client.set_input_flow(self.input_flow(client.debug, num_pages=1))
            resp = tezos.sign_tx(
                client,
                TEZOS_PATH_10,
                dict_to_proto(
                    messages.TezosSignTx,
                    {
                        "branch": "dee04042c0832d68a43699b2001c0a38065436eb05e578071a763e1972d0bc81",
                        "proposal": {
                            "source": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                            "period": 17,
                            "proposals": [
                                "dfa974df171c2dad9a9b8f25d99af41fd9702ce5d04521d2f9943c84d88aa572"
                            ],
                        },
                    },
                ),
            )

        assert (
            resp.signature
            == "edsigtfY16R32k2WVMYfFr7ymnro4ib5zMckk28vsuViYNN77DJAvCJLRNArd9L531pUCxT4YdcvCvBym5dhcZ1rknEVm6yZ8bB"
        )
        assert (
            resp.sig_op_contents.hex()
            == "dee04042c0832d68a43699b2001c0a38065436eb05e578071a763e1972d0bc8105005f450441f41ee11eee78a31d1e1e55627c783bd60000001100000020dfa974df171c2dad9a9b8f25d99af41fd9702ce5d04521d2f9943c84d88aa5723b12621296a679b3a74ea790df5347995a76e20a09e76590baaacf4e09341965a04123f5cbbba8427f045b5f7d59157a3098e44839babe7c247d19b58bbb2405"
        )
        assert (
            resp.operation_hash == "opLqntFUu984M7LnGsFvfGW6kWe9QjAz4AfPDqQvwJ1wPM4Si4c"
        )

    def test_tezos_sign_tx_multiple_proposals(self, client):
        with client:
            client.set_input_flow(self.input_flow(client.debug, num_pages=2))
            resp = tezos.sign_tx(
                client,
                TEZOS_PATH_10,
                dict_to_proto(
                    messages.TezosSignTx,
                    {
                        "branch": "7e0be36a90c663c73c60da3889ffefff1383fb65cc29f0639f173d8f95a52df7",
                        "proposal": {
                            "source": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                            "period": 17,
                            "proposals": [
                                "2a6ff28ab4d0ccb18f7129aaaf9a4b8027d794f2562849665fdb6999db2a4e57",
                                "47cd60c09ab8437cc9fe19add494dce1b9844100f660f02ce77510a0c66d2762",
                            ],
                        },
                    },
                ),
            )

        assert (
            resp.signature
            == "edsigu6GAjhiWAQ64ctWTGEDYAZ16tYzLgzWzqc4CUyixK4FGRE8YUBVzFaVJ2fUCexZjZLMLdiNZGcUdzeL1bQhZ2h5oLrh7pA"
        )
        assert (
            resp.sig_op_contents.hex()
            == "7e0be36a90c663c73c60da3889ffefff1383fb65cc29f0639f173d8f95a52df705005f450441f41ee11eee78a31d1e1e55627c783bd600000011000000402a6ff28ab4d0ccb18f7129aaaf9a4b8027d794f2562849665fdb6999db2a4e5747cd60c09ab8437cc9fe19add494dce1b9844100f660f02ce77510a0c66d2762f813361ac00ada7e3256f23973ae25b112229476a3cb3e506fe929ea1e9358299fed22178d1be689cddeedd1f303abfef859b664f159a528576a1c807079f005"
        )
        assert (
            resp.operation_hash == "onobSyNgiitGXxSVFJN6949MhUomkkxvH4ZJ2owgWwNeDdntF9Y"
        )

    def test_tezos_sing_tx_ballot_yay(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "3a8f60c4cd394cee5b50136c7fc8cb157e8aaa476a9e5c68709be6fc1cdb5395",
                    "ballot": {
                        "source": "0002298c03ed7d454a101eb7022bc95f7e5f41ac78",
                        "period": 2,
                        "proposal": "def7ed9c84af23ab37ebb60dd83cd103d1272ad6c63d4c05931567e65ed027e3",
                        "ballot": 0,
                    },
                },
            ),
        )

        assert (
            resp.signature
            == "edsigtkxNm6YXwtV24DqeuimeZFTeFCn2jDYheSsXT4rHMcEjNvzsiSo55nVyVsQxtEe8M7U4PWJWT4rGYYGckQCgtkNJkd2roX"
        )

    def test_tezos_sing_tx_ballot_nay(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "3a8f60c4cd394cee5b50136c7fc8cb157e8aaa476a9e5c68709be6fc1cdb5395",
                    "ballot": {
                        "source": "0002298c03ed7d454a101eb7022bc95f7e5f41ac78",
                        "period": 2,
                        "proposal": "def7ed9c84af23ab37ebb60dd83cd103d1272ad6c63d4c05931567e65ed027e3",
                        "ballot": 1,
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigtqLaizfF6Cfc2JQL7TrsyniGhpZEojZAKMFW6AeudaUoU8KGXEHJH69Q4Lf27qFyUSTfbeHNnnCt69SGEPWkmpkgkgqMbL"
        )

    def test_tezos_sing_tx_ballot_pass(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "3a8f60c4cd394cee5b50136c7fc8cb157e8aaa476a9e5c68709be6fc1cdb5395",
                    "ballot": {
                        "source": "0002298c03ed7d454a101eb7022bc95f7e5f41ac78",
                        "period": 2,
                        "proposal": "def7ed9c84af23ab37ebb60dd83cd103d1272ad6c63d4c05931567e65ed027e3",
                        "ballot": 2,
                    },
                },
            ),
        )

        assert (
            resp.signature
            == "edsigu6YX7EegPwrpcEbdNQsNhrRiEagBNGJBmFamP4mixZZw1UynhahGQ8RNiZLSUVLERUZwygrsSVenBqXGt9VnknTxtzjKzv"
        )

    def test_tezos_sign_tx_tranasaction(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "ce69c5713dac3537254e7be59759cf59c15abd530d10501ccf9028a5786314cf",
                    "transaction": {
                        "source": "0002298c03ed7d454a101eb7022bc95f7e5f41ac78",
                        "fee": 50000,
                        "counter": 3,
                        "gas_limit": 200,
                        "storage_limit": 0,
                        "amount": 100000000,
                        "destination": {
                            "tag": 0,
                            "hash": "00e7670f32038107a59a2b9cfefae36ea21f5aa63c",
                        },
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigtrw2WiZ1ukvuGKxC5D3vDYENtHAKTVNCMRucP4V2NZa65FrEWF6VfLCeDPZVXgS8gr2UBefUA8tazSemirEQAb9E3Rbhwi"
        )

    def test_tezos_sign_tx_delegation(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "f7332bca1c541848c070050487a12d0e95a83f2f0b6615c05bb31526bb5c14a1",
                    "delegation": {
                        "source": "00fe24d178d020b7fd8e9e4f5887ace9f32feba4f9",
                        "fee": 1257,
                        "counter": 190,
                        "gas_limit": 10100,
                        "storage_limit": 0,
                        "delegate": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigttZHuCmpHDkWn4XboUq6UkSiaLDaY6V2cHW3eGBELeq7bpUALoLAfXr5ktbq2r1KAeBCxSR3YQ9mcY485jyAnY57fhk3RP"
        )

    def test_tezos_sign_tx_origination(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "464bc6bd8be4087b86691cce1af635c1a4ccdcd9fa8d71c55279e4395503d46e",
                    "origination": {
                        "source": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                        "fee": 1391,
                        "counter": 193,
                        "gas_limit": 11137,
                        "storage_limit": 323,
                        "balance": 100000000,
                        "script": "0000001c02000000170500036805010368050202000000080316053d036d03420000000a010000000568656c6c6f",
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigtwqvmAmZDSjS9yw4zvRbrYW4y7xjmo4yk5yoWCxFAiyVzHbCkDXWUMq7RH14Q3Loe4rgkA562uBqJEK6tffVnYFLsEBfHv"
        )

    def test_tezos_sign_tx_reveal(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "ce69c5713dac3537254e7be59759cf59c15abd530d10501ccf9028a5786314cf",
                    "reveal": {
                        "source": "00a1133f154bf55df7189dede340db03bad09235fb",
                        "fee": 1269,
                        "counter": 416223,
                        "gas_limit": 10100,
                        "storage_limit": 0,
                        "public_key": "0056a1c1fbae8ae7dc0c79519634d61ae67bd0ce92a9974f3d3cfe2ccf44e55b06",
                    },
                    "transaction": {
                        "source": "0002298c03ed7d454a101eb7022bc95f7e5f41ac78",
                        "fee": 50000,
                        "counter": 3,
                        "gas_limit": 200,
                        "storage_limit": 0,
                        "amount": 100000000,
                        "destination": {
                            "tag": 0,
                            "hash": "00e7670f32038107a59a2b9cfefae36ea21f5aa63c",
                        },
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigu43ztCKfgeHybP78pjdMBpNHXKtL9TmpymMSLYi5ss6hSYbZBeTR7rgNqwuq4iT8cEj8KHsii5jraAsK4mF3x8AqGqCP1Y"
        )

    def test_tezos_smart_contract_delegation(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "6f2867511d04e00a0aa0fe8d4240a0755a49d265262a3ad76f6124531d8e8cb5",
                    "transaction": {
                        "source": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                        "fee": 2894,
                        "counter": 195,
                        "gas_limit": 25917,
                        "storage_limit": 0,
                        "amount": 0,
                        "destination": {
                            "tag": 1,
                            "hash": "8b83360512c6045c1185f8000de41302e23a220c00",
                        },
                        # rework naming
                        "smart_contract_delegation": {
                            "delegate": "00a31e81ac3425310e3274a4698a793b2839dc0afa"
                        },
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigtsFTxYMoeRbzCCRg2ck4ChSrNNms99RF5KvWw1X5VSmhCTn3akccxjEQFLg982p8LvRdwhLUoEaekEF6MrZhyEooXXxvdz"
        )

    def test_tezos_kt_remove_delegation(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "38f027151adbf750cf05f5e7259fd7e1d8122a7f76be5204c0db5eb93757c3e4",
                    "transaction": {
                        "source": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                        "fee": 2857,
                        "counter": 196,
                        "gas_limit": 25822,
                        "storage_limit": 0,
                        "amount": 0,
                        "destination": {
                            "tag": 1,
                            "hash": "8b83360512c6045c1185f8000de41302e23a220c00",
                        },
                        "smart_contract_delegation": {"delegate": None},
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigu5B11SxhJqcvhwgHvLKfEb8wwtnJeFfBRocTaVs4RGiiW21c8nQ3F6xuVRRGLg4p51YtikvK4E3bTsHE5t5guoaDNjMToK"
        )

    def test_tezos_smart_contract_transfer(self, client):
        resp = tezos.sign_tx(
            client,
            TEZOS_PATH_10,
            dict_to_proto(
                messages.TezosSignTx,
                {
                    "branch": "dafa0777baf8a81cef1e2511398638703f8353d3572f835e87a078124c757ea8",
                    "transaction": {
                        "source": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                        "fee": 2941,
                        "counter": 195,
                        "gas_limit": 26283,
                        "storage_limit": 0,
                        "amount": 0,
                        "destination": {
                            "tag": 1,
                            "hash": "8b83360512c6045c1185f8000de41302e23a220c00",
                        },
                        "smart_contract_transfer": {
                            "amount": 20000,
                            "recipient": "005f450441f41ee11eee78a31d1e1e55627c783bd6",
                        },
                    },
                },
            ),
        )
        assert (
            resp.signature
            == "edsigu2MMdtkWyRofmSwB5gZuF3P6rzbuWXjWHmsG6v2NQgfgKrDoEZ6czUUXXrCCoQL3TfuTX1r3epCXpvVMcFKuRcjBL83RFN"
        )
