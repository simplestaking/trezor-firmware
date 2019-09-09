from . import messages
from .tools import expect


@expect(messages.CosmosAddress, field="address")
def get_address(client, address_n, show_display=False):
    return client.call(
        messages.CosmosGetAddress(address_n=address_n, show_display=show_display)
    )


@expect(messages.CosmosPublicKey)
def get_public_key(client, address_n, show_display=False):
    return client.call(
        messages.CosmosGetPublicKey(address_n=address_n, show_display=show_display)
    )


@expect(messages.CosmosSignedTx)
def sign_tx(client, address_n, sign_tx_msg):
    sign_tx_msg.address_n = address_n
    return client.call(sign_tx_msg)
