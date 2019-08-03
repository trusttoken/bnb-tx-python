from binance_transaction.base import Address, Amino, String, VarInt, make_prefix


"""
dex.py

Transaction types associated with Binance DEX
Usually these start with dex/*


DexList (dex/ListMsg)
NewOrder
CancelOrder
"""


# side
BUY = 1
SELL = 2

# timeinforce
GTE = 1
IOC = 3

# ordertype
LIMIT_ORDER = 2


class DexList(Amino):
    def __init__(self, from_address, proposal_id, base_asset_symbol, quote_asset_symbol, init_price):
        dict.__init__(
            self,
            proposal_id=VarInt(proposal_id),
            base_asset_symbol=String(base_asset_symbol),
            quote_asset_symbol=String(quote_asset_symbol),
            init_price=VarInt(init_price)
        )
        self['from'] = Address(from_address)

    @staticmethod
    def object_id():
        return bytes.fromhex('B41DE13F')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['from'].encode(1)
        buf += self['proposal_id'].encode(2)
        buf += self['base_asset_symbol'].encode(3)
        buf += self['quote_asset_symbol'].encode(4)
        buf += self['init_price'].encode(5)
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
        assert data[0:4] == DexList.object_id()
        data = data[4:]
        from_address, data = Address.decode(data, 1)
        proposal_id, data = VarInt.decode(data, 2)
        base_asset_symbol, data = String.decode(data, 3)
        quote_asset_symbol, data = String.decode(data, 4)
        init_price, data = VarInt.decode(data, 5)
        return DexList(from_address, proposal_id, base_asset_symbol, quote_asset_symbol, init_price)

    def from_msg_obj(list_data):
        return DexList(
            list_data['from'],
            list_data['proposal_id'],
            list_data['base_asset_symbol'],
            list_data['quote_asset_symbol'],
            list_data['init_price']
        )


class NewOrder(Amino):
    def __init__(self, sender, order_id, symbol, ordertype, side, price, quantity, timeinforce):
        dict.__init__(
            self,
            sender=Address(sender),
            symbol=String(symbol),
            ordertype=VarInt(ordertype),
            side=VarInt(side),
            price=VarInt(price),
            quantity=VarInt(quantity),
            timeinforce=VarInt(timeinforce)
        )
        self['id'] = String(order_id)

    @staticmethod
    def object_id():
        return bytes.fromhex('CE6DC043')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['sender'].encode(1)
        buf += self['id'].encode(2)
        buf += self['symbol'].encode(3)
        buf += self['ordertype'].encode(4)
        buf += self['side'].encode(5)
        buf += self['price'].encode(6)
        buf += self['quantity'].encode(7)
        buf += self['timeinforce'].encode(8)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    def decode(self, field_id=None):
        pass

    @staticmethod
    def from_msg_obj(msg_data):
        return NewOrder(
            msg_data['sender'],
            msg_data['id'],
            msg_data['symbol'],
            msg_data['ordertype'],
            msg_data['side'],
            msg_data['price'],
            msg_data['quantity'],
            msg_data['timeinforce']
        )


class CancelOrder(Amino):
    def __init__(self, sender, symbol, refid):
        dict.__init__(self, sender=sender, symbol=symbol, refid=refid)

    @staticmethod
    def object_id():
        return bytes.fromhex('166E681B')

    def encode(self, field_id=None):
        buf = self.object_id()
        buf += self['sender'].encode(1)
        buf += self['symbol'].encode(2)
        buf += self['refid'].encode(3)
        if field_id is None:
            return buf
        else:
            return make_prefix(field_id, 2) + VarInt(len(buf)).encode() + buf

    def decode(self):
        pass

    @staticmethod
    def from_msg_obj(cancel_data):
        return CancelOrder(
            Address(cancel_data['sender']),
            String(cancel_data['symbol']),
            String(cancel_data['refid'])
        )
