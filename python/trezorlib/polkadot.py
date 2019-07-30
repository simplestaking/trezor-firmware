from . import messages
from .tools import expect


@expect(messages.PolkadotAddress, field="address")
def get_address(client, address_n, show_display=False):
    return client.call(
        messages.PolkadotGetAddress(address_n=address_n, show_display=show_display)
    )


@expect(messages.PolkadotPublicKey, field="public_key")
def get_public_key(client, address_n, show_display=False):
    return client.call(
        messages.PolkadotGetPublicKey(address_n=address_n, show_display=show_display)
    )


# @expect(messages.PolkadotSignedTx)
# def sign_tx(client, address_n, sign_tx_msg):
#     sign_tx_msg.address_n = address_n
#     return client.call(sign_tx_msg)
