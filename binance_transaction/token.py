from binance_transaction.base import Address, Amino, Bool, Input, Output, Repeated, String, Token, VarInt, make_prefix


"""
token.py

Message types regarding BEP2 tokens
Their message type usually starts with tokens/*

* Send (cosmos-sdk/Send)
* Issue (tokens/IssueMsg)
* Mint (tokens/MintMsg)
* Burn
* Freeze
* Unfreeze
* TimeLock
* TimeUnlock
* TimeRelock
"""


class Send(Amino):
    def __init__(self, inputs, outputs):
        dict.__init__(self, inputs=inputs, outputs=outputs)

    @staticmethod
    def object_id():
        return bytes.fromhex('2A2C87FA')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['inputs'].encode(1)
        buf += self['outputs'].encode(2)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def decode(data, field_id=None):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return None, data
            data = data[len(field_id):]
        assert data[0:4] == Send.object_id()
        data = data[4:]
        inputs, data = Repeated.decode(data, bytes([8 | 2]), Input)
        outputs, data = Repeated.decode(data, bytes([16 | 2]), Output)
        return Send(inputs, outputs), data

    @staticmethod
    def from_msg_obj(send_data):
        inputs = Repeated([])
        outputs = Repeated([])
        for source in send_data['inputs']:
            coins = []
            for coin in source['coins']:
                coins.append(Token(coin['amount'], coin['denom']))
            inputs.append(Input(source['address'], coins))
        for source in send_data['outputs']:
            coins = []
            for coin in source['coins']:
                coins.append(Token(coin['amount'], coin['denom']))
            outputs.append(Output(source['address'], coins))
        return Send(inputs, outputs)


class Issue(Amino):
    def __init__(self, from_address, name, symbol, total_supply, mintable):
        dict.__init__(
            self,
            name=String(name),
            symbol=String(symbol),
            total_supply=VarInt(total_supply),
            mintable=bool(mintable))
        self['from'] = Address(from_address)

    @staticmethod
    def object_id():
        return bytes.fromhex('17EFAB80')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['from'].encode(1)
        buf += self['name'].encode(2)
        buf += self['symbol'].encode(3)
        buf += self['total_supply'].encode(4)
        buf += Bool(self['mintable']).encode(5)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    def decode(data, field_id=None, hrp='bnb'):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return None, data
            data = data[len(field_id):]
        assert data[0:4] == Issue.object_id()
        data = data[4:]
        address, data = Address.decode(data, 1, hrp)
        name, data = String.decode(data, 2)
        symbol, data = String.decode(data, 3)
        total_supply, data = VarInt.decode(data, 4)
        mintable, data = Bool.decode(data, 5)
        mintable = True if mintable else 0
        return Issue(address, name, symbol, total_supply, mintable), data

    @staticmethod
    def from_msg_obj(issue_data):
        return Issue(
            issue_data['from'],
            issue_data['name'],
            issue_data['symbol'],
            issue_data['total_supply'],
            issue_data['mintable']
        )


class Mint(Amino):
    def __init__(self, from_address, symbol, amount):
        dict.__init__(
            self,
            symbol=String(symbol),
            amount=VarInt(amount)
        )
        self['from'] = Address(from_address)

    @staticmethod
    def object_id():
        return bytes.fromhex('467E0829')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['from'].encode(1)
        buf += self['symbol'].encode(2)
        buf += self['amount'].encode(3)
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
        from_address, data = Address.decode(data, 1)
        symbol, data = String.decode(data, 2)
        amount, data = VarInt.decode(data, 3)
        return Mint(from_address, symbol, amount)

    @staticmethod
    def from_msg_obj(mint_data):
        return Mint(
            mint_data['from'],
            mint_data['symbol'],
            mint_data['amount']
        )


class Burn(Amino):
    def __init__(self, from_address, symbol, amount):
        dict.__init__(
            self,
            amount=VarInt(amount),
            symbol=String(symbol)
        )
        self['from'] = Address(from_address)

    @staticmethod
    def object_id():
        return bytes.fromhex('7ED2D2A0')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['from'].encode(1)
        buf += self['symbol'].encode(2)
        buf += self['amount'].encode(3)
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
        assert data[0:4] == Burn.object_id()
        data = data[4:]
        from_address, data = Address.decode(data, 1)
        symbol, data = String.decode(data, 2)
        amount, data = VarInt.decode(data, 3)
        return Burn(from_address, symbol, amount), data

    @staticmethod
    def from_msg_obj(burn_data):
        return Burn(
            burn_data['from'],
            burn_data['symbol'],
            burn_data['amount']
        )


class Freeze(Amino):
    def __init__(self, from_address, symbol, amount):
        dict.__init__(
            self,
            amount=VarInt(amount),
            symbol=String(symbol)
        )
        self['from'] = Address(from_address)

    @staticmethod
    def object_id():
        return bytes.fromhex('E774B32D')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += Address(self['from']).encode(1)
        buf += String(self['symbol']).encode(2)
        buf += VarInt(self['amount']).encode(3)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @classmethod
    def decode(klass, data, field_id=None):
        if field_id is not None:
            prefix = make_prefix(field_id, 2)
            for i in range(len(prefix)):
                if prefix[i] != data[i]:
                    return None, data
            data = data[len(field_id):]
        assert data[0:4] == klass.object_id()
        data = data[4:]
        from_address, data = Address.decode(data, 1)
        symbol, data = String.decode(data, 2)
        amount, data = VarInt.decode(data, 3)
        return klass(from_address, symbol, amount), data

    @classmethod
    def from_msg_obj(klass, freeze_data):
        return klass(
            freeze_data['from'],
            freeze_data['symbol'],
            freeze_data['amount']
        )


class Unfreeze(Freeze):
    @staticmethod
    def object_id():
        return bytes.fromhex('6515FF0D')


class TimeLock(Amino):
    def __init__(self, from_address, description, amount, lock_time):
        dict.__init__(
            self,
            description=String(description),
            amount=Repeated(amount),
            lock_time=VarInt(lock_time)
        )
        self['from'] = from_address

    @staticmethod
    def object_id():
        return bytes.fromhex('07921531')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['from'].encode(1)
        buf += self['description'].encode(2)
        buf += self['amount'].encode(3)
        buf += self['lock_time'].encode(4)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def from_msg_obj(timelock_data):
        coins = []
        for amount in timelock_data['amount']:
            coins.append(Token(VarInt(amount['amount']), amount['denom']))
        return TimeLock(
            Address(timelock_data['from']),
            String(timelock_data.get('description', '')),
            Repeated(coins),
            VarInt(timelock_data['lock_time'])
        )


class TimeUnlock(Amino):
    def __init__(self, from_address, time_lock_id):
        dict.__init__(
            self,
            time_lock_id=VarInt(time_lock_id)
        )
        self['from'] = Address(from_address)

    @staticmethod
    def object_id():
        return bytes.fromhex('C4050C6C')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['from'].encode(1)
        buf += self['time_lock_id'].encode(2)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def from_msg_obj(timeunlock_data):
        return TimeUnlock(
            timeunlock_data['from'],
            timeunlock_data['time_lock_id']
        )


class TimeRelock(Amino):
    def __init__(self, from_address, time_lock_id, description, amount, lock_time):
        dict.__init__(
            self,
            time_lock_id=VarInt(time_lock_id),
            description=String(description),
            amount=Repeated(amount),
            lock_time=VarInt(lock_time)
        )
        self['from'] = Address(from_address)

    @staticmethod
    def object_id():
        return bytes.fromhex('504711DA')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['from'].encode(1)
        buf += self['time_lock_id'].encode(2)
        buf += self['description'].encode(3)
        buf += self['amount'].encode(4)
        buf += self['lock_time'].encode(5)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    @staticmethod
    def from_msg_obj(timerelock_data):
        amounts = []
        for amount in timerelock_data['amount']:
            amounts.append(Token(VarInt(amount['amount']), String(amount['denom'])))
        return TimeRelock(
            timerelock_data['from'],
            timerelock_data['time_lock_id'],
            timerelock_data['description'],
            amounts,
            timerelock_data['lock_time']
        )
