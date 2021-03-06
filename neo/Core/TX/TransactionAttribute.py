# -*- coding:utf-8 -*-
"""
Description:
    Transaction Attribute
Usage:
    from neo.Core.TX.TransactionAttribute import TransactionAttribute
"""

from neo.Network.Inventory import Inventory
from neo.IO.Mixins import SerializableMixin

import binascii
from autologging import logged


class TransactionAttributeUsage(object):
    ContractHash = int.from_bytes(b'\x00','little')

    ECDH02 = int.from_bytes(b'\x02','little')
    ECDH03 = int.from_bytes(b'\x03','little')

    Script = int.from_bytes(b'\x20','little')

    Vote = int.from_bytes(b'\x30','little')

    CertUrl = int.from_bytes(b'\x80','little')
    DescriptionUrl = int.from_bytes(b'\x81','little')
    Description = int.from_bytes(b'\x90','little')

    Hash1 = int.from_bytes(b'\xa1','little')
    Hash2 = int.from_bytes(b'\xa2','little')
    Hash3 = int.from_bytes(b'\xa3','little')
    Hash4 = int.from_bytes(b'\xa4','little')
    Hash5 = int.from_bytes(b'\xa5','little')
    Hash6 = int.from_bytes(b'\xa6','little')
    Hash7 = int.from_bytes(b'\xa7','little')
    Hash8 = int.from_bytes(b'\xa8','little')
    Hash9 = int.from_bytes(b'\xa9','little')
    Hash10 = int.from_bytes(b'\xaa','little')
    Hash11 = int.from_bytes(b'\xab','little')
    Hash12 = int.from_bytes(b'\xac','little')
    Hash13 = int.from_bytes(b'\xad','little')
    Hash14 = int.from_bytes(b'\xae','little')
    Hash15 = int.from_bytes(b'\xaf','little')

    Remark = int.from_bytes(b'\xf0','little')
    Remark1 = int.from_bytes(b'\xf1','little')
    Remark2 = int.from_bytes(b'\xf2','little')
    Remark3 = int.from_bytes(b'\xf3','little')
    Remark4 = int.from_bytes(b'\xf4','little')
    Remark5 = int.from_bytes(b'\xf5','little')
    Remark6 = int.from_bytes(b'\xf6','little')
    Remark7 = int.from_bytes(b'\xf7','little')
    Remark8 = int.from_bytes(b'\xf8','little')
    Remark9 = int.from_bytes(b'\xf9','little')
    Remark10 = int.from_bytes(b'\xfa','little')
    Remark11 = int.from_bytes(b'\xfb','little')
    Remark12 = int.from_bytes(b'\xfc','little')
    Remark13 = int.from_bytes(b'\xfd','little')
    Remark14 = int.from_bytes(b'\xfe','little')
    Remark15 = int.from_bytes(b'\xff','little')


@logged
class TransactionAttribute(Inventory, SerializableMixin):
    """docstring for TransactionAttribute"""
    def __init__(self, usage=None, data=None):
        super(TransactionAttribute, self).__init__()
        self.Usage = usage
        self.Data = data

    def Deserialize(self, reader):
        usage = reader.ReadByte()
        self.Usage = usage

        if usage == TransactionAttributeUsage.ContractHash or usage==TransactionAttributeUsage.Vote or \
            (usage >= TransactionAttributeUsage.Hash1 and usage <= TransactionAttributeUsage.Hash15):
            self.Data = reader.ReadBytes(32)

        elif usage == TransactionAttributeUsage.ECDH02 or usage == TransactionAttributeUsage.ECDH03:
            self.Data = bytearray(usage) + bytearray(reader.ReadBytes(32))

        elif usage == TransactionAttributeUsage.Script:
            self.Data = reader.ReadBytes(20)

        elif usage == TransactionAttributeUsage.DescriptionUrl:

            self.Data == reader.ReadBytes(reader.ReadByte())

        elif usage == TransactionAttributeUsage.Description or usage >= TransactionAttributeUsage.Remark:
            self.Data = reader.ReadVarBytes()
        else:
            self.__log.debug("format error!!!")


    def Serialize(self, writer):
        writer.WriteByte(self.Usage)

        if self.Usage == TransactionAttributeUsage.ContractHash or self.Usage == TransactionAttributeUsage.Vote or \
                (self.Usage >= TransactionAttributeUsage.Hash1 and self.Usage <= TransactionAttributeUsage.Hash15):
            writer.WriteBytes(self.Data)

        elif self.Usage == TransactionAttributeUsage.ECDH02 or self.Usage == TransactionAttributeUsage.ECDH03:
            writer.WriteBytes(self.Data[1:33])

        elif self.Usage == TransactionAttributeUsage.Script:
            writer.WriteBytes(self.Data)

        elif self.Usage == TransactionAttributeUsage.DescriptionUrl:
            writer.WriteVarString(self.Data)

        elif self.Usage == TransactionAttributeUsage.Description or self.Usage >= TransactionAttributeUsage.Remark:
            writer.WriteVarString(self.Data)
        else:
            self.__log.debug("format error!!!")



    def ToJson(self):
        obj = {
            'usage': self.Usage,
            'data': '' if not self.Data else self.Data.hex()
        }
        return obj