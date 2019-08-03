from binance_transaction.base import (
    Amino, Repeated, String, Address, StringVarInt, StringToken, Token, VarInt, make_prefix
)


"""
gov.py

Message types regarding Binance Chain governance
Their message type usually starts with cosmos-sdk/*

* Proposal (cosmos-sdk/MsgSubmitProposal)
* Vote
"""


proposal_type_to_int = {
    'Text': 1,
    'ParameterChange': 2,
    'SoftwareUpgrade': 3,
    'ListTradingPair': 4,
    'FeeChange': 5,
}


class Proposal(Amino):
    def __init__(self, title, description, proposal_type, proposer, initial_deposit, voting_period):
        dict.__init__(
            self,
            title=String(title),
            description=String(description),
            proposal_type=String(proposal_type),
            proposer=Address(proposer),
            initial_deposit=initial_deposit,
            voting_period=StringVarInt(voting_period)
        )

    @staticmethod
    def object_id():
        return bytes.fromhex('B42D614E')

    def encode(self, field_id=None):
        # buf = bytes.fromhex('ACCBA2DE')
        buf = self.object_id()
        buf += self['title'].encode(1)
        buf += self['description'].encode(2)
        buf += VarInt(proposal_type_to_int[self['proposal_type']]).encode(3)
        buf += self['proposer'].encode(4)
        buf += self['initial_deposit'].encode(5)
        buf += self['voting_period'].encode(6)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    def decode(data, field_id=None):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return None, data
            data = data[len(field_id):]
        assert data[0:4] == Proposal.object_id()
        data = data[4:]
        title, data = String.decode(data, 1)
        description, data = String.decode(data, 2)
        proposal_type, data = VarInt.decode(data, 3)
        proposer, data = Address.decode(data, 4)
        initial_deposit, data = Repeated.decode(data, 5, Token)
        voting_period, data = StringVarInt.decode(data, 6)
        return Proposal(title, description, proposal_type, proposer, initial_deposit, voting_period)

    @staticmethod
    def from_msg_obj(proposal_data):
        initial_deposit = Repeated([])
        for deposit in proposal_data['initial_deposit']:
            initial_deposit.append(StringToken(deposit['amount'], deposit['denom'])),
        return Proposal(
            proposal_data['title'],
            proposal_data['description'],
            proposal_data['proposal_type'],
            proposal_data['proposer'],
            initial_deposit,
            proposal_data['voting_period']
        )


vote_option_to_varint = {
    "Yes": VarInt(1),
    "Abstain": VarInt(2),
    "No": VarInt(3),
    "NoWithVeto": VarInt(4)
}


class VoteOption(String):
    """
    A String enum for JSON, a VarInt for encoding
    """
    def encode(self, field_id=None):
        return VarInt.encode(vote_option_to_varint[self], field_id)


class Vote(Amino):
    def __init__(self, proposal_id, voter, option):
        dict.__init__(
            self,
            proposal_id=StringVarInt(proposal_id),
            voter=Address(voter),
            option=VoteOption(option)
        )

    @staticmethod
    def object_id():
        return bytes.fromhex('A1CADD36')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['proposal_id'].encode(1)
        buf += self['voter'].encode(2)
        buf += self['option'].encode(3)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def from_msg_obj(vote_data):
        return Vote(
            StringVarInt(vote_data['proposal_id']),
            Address(vote_data['voter']),
            VoteOption(vote_data['option'])
        )
