from binance_transaction.base import Amino, make_prefix
from binance_transaction.token import Send, Issue, Mint, Burn, Freeze, Unfreeze, TimeLock, TimeRelock, TimeUnlock
from binance_transaction.gov import Proposal, Vote
from binance_transaction.dex import DexList, NewOrder, CancelOrder


"""
msg.py

All message types are documented in this file to support decoding

Msg
"""


msg_class_by_type = {
    'cosmos-sdk/Send': Send,
    'dex/ListMsg': DexList,
    'dex/NewOrder': NewOrder,
    'dex/CancelOrder': CancelOrder,
    'tokens/IssueMsg': Issue,
    'tokens/MintMsg': Mint,
    'tokens/BurnMsg': Burn,
    'tokens/FreezeMsg': Freeze,
    'tokens/UnfreezeMsg': Unfreeze,
    'tokens/TimeLockMsg': TimeLock,
    'tokens/TimeUnlockMsg': TimeUnlock,
    'tokens/TimeRelockMsg': TimeRelock,
    'cosmos-sdk/MsgSubmitProposal': Proposal,
    'cosmos-sdk/MsgVote': Vote,
}


msg_class_by_object_id = {
    Send.object_id(): Send,
    Issue.object_id(): Issue,
    Mint.object_id(): Mint,
    Burn.object_id(): Burn,
    Freeze.object_id(): Freeze,
    Unfreeze.object_id(): Unfreeze,
    TimeLock.object_id(): TimeLock,
    TimeUnlock.object_id(): TimeUnlock,
    TimeRelock.object_id(): TimeRelock,
    Proposal.object_id(): Proposal,
    DexList.object_id(): DexList,
    Vote.object_id(): Vote,
    CancelOrder.object_id(): CancelOrder,
    NewOrder.object_id(): NewOrder
}


class Msg(Amino):
    @staticmethod
    def decode(data, field_id):
        prefix = make_prefix(field_id, 2)
        object_id = data[len(prefix):len(prefix) + 4]
        return msg_class_by_object_id[object_id].decode(data, prefix)

    @staticmethod
    def from_msg_obj(msg_obj):
        msg_klass = msg_class_by_type[msg_obj['type']]
        return msg_klass.from_msg_obj(msg_obj)
