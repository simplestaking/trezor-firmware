from micropython import const

TRANSACTION_BLUEPRINT = '{"account_number":"{account_number}","chain_id":"{chain_id}","fee":{fee},"memo":"{memo}","msgs":[{msgs}],"sequence":"{sequence}"}'
FEE_BLUEPRINT = '{"amount":[{amount}],"gas":"{gas}"}'
AMOUNT_BLUEPRINT = '{"amount":"{amount}","denom":"{denom}"}'
SEND_MESSAGE_BLUEPRINT = '{"type":"cosmos-sdk/MsgSend","value":{value}}'
SEND_VALUE_BLUEPRINT = '"amount":[{amount}],"from_address":"{from_address}","to_address":"{to_address}"'


def construct_json_for_signing(msg) -> str:
    return TRANSACTION_BLUEPRINT.format(
        account_number=msg.account_number,
        chain_id=msg.chain_id,
        fee=construct_fee_json(msg),
        memo=msg.memo,
        msgs=construct_send_message_json(msg),
        sequence=msg.sequence
    )


def construct_fee_json(msg) -> str:
    return FEE_BLUEPRINT.format(
        amount=msg.fee.amount.amount,
        gas=msg.fee.gas
    )


def construct_send_value(msg) -> str:
    return SEND_VALUE_BLUEPRINT.format(
        amount=construct_amount_json(msg),
        from_address=msg.msgs.from_address,
        to_address=msg.msgs.to_address
    )


def construct_amount_json(msg) -> str:
    return SEND_VALUE_BLUEPRINT.format(
        amount=msg.msgs.amount.amount,
        denom=msg.msgs.amount.denom
    )


def construct_send_message_json(msg) -> str:
    return SEND_MESSAGE_BLUEPRINT.format(
        value=construct_send_value(msg)
    )
