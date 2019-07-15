from . import messages
from .tools import expect


@expect(messages.AeternityAddress, field="address")
def get_address(client, address_n, show_display=False):
    return client.call(
        messages.AeternityGetAddress(address_n=address_n, show_display=show_display)
    )


@expect(messages.AeternityPublicKey, field="public_key")
def get_public_key(client, address_n, show_display=False):
    return client.call(
        messages.AeternityGetPublicKey(address_n=address_n, show_display=show_display)
    )


@expect(messages.AeternitySignedTx)
def sign_tx(client, address_n, sign_tx_msg):
    sign_tx_msg.address_n = address_n
    return client.call(sign_tx_msg)
