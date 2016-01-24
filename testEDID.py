import unittest
import copy
import EDID


class DatabaseTests(unittest.TestCase):
    # http://kodi.wiki/view/Creating_and_using_edid.bin_via_xorg.conf
    validEDIDData = bytearray.fromhex('''
		00 ff ff ff ff ff ff 00  4c 2d bc 03 00 00 00 00
		2f 11 01 03 80 10 09 78  0a ee 91 a3 54 4c 99 26
		0f 50 54 21 08 00 81 80  a9 40 01 01 01 01 01 01
		01 01 01 01 01 01 02 3a  80 18 71 38 2d 40 58 2c
		45 00 a0 5a 00 00 00 1e  66 21 50 b0 51 00 1b 30
		40 70 36 00 a0 5a 00 00  00 1e 00 00 00 fd 00 17
		3d 1a 4c 17 00 0a 20 20  20 20 20 20 00 00 00 fc
		00 53 41 4d 53 55 4e 47  0a 20 20 20 20 20 01 d3
		02 03 27 f1 4b 90 1f 04  13 05 14 03 12 20 21 22
		23 09 07 07 83 01 00 00  e2 00 0f e3 05 03 01 67
		03 0c 00 20 00 b8 2d 01  1d 00 72 51 d0 1e 20 6e
		28 55 00 a0 5a 00 00 00  1e 01 1d 00 bc 52 d0 1e
		20 b8 28 55 40 a0 5a 00  00 00 1e 01 1d 80 18 71
		1c 16 20 58 2c 25 00 a0  5a 00 00 00 9e 01 1d 80
		d0 72 1c 16 20 10 2c 25  80 a0 5a 00 00 00 9e 00
		00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 0d
		'''.replace('\n', ' ').replace('\t', ' '))

    # http://flipthatbit.net/2011/04/ddc2-interface-crafting-your-own-edid/
    validEDIDData2 = bytearray.fromhex('''
        00 FF FF FF FF FF FF 00  1A 82 00 01 00 00 00 01
        0C 15 01 02 08 11 0D 78  05 00 00 00 00 00 00 00
        00 00 00 20 00 00 31 40  01 01 01 01 01 01 01 01
        01 01 01 01 01 01 00 00  00 FC 00 66 6C 69 70 74
        68 61 74 62 69 74 30 31  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 0A
        '''.replace('\n', ' ').replace('\t', ' '))

    def testCheckChecksumValid(self):
        edid = EDID.EDID(data=self.validEDIDData)
        self.assertTrue(edid.checkChecksum())

    def testCheckChecksumInvalid(self):
        edid = EDID.EDID(data=self.validEDIDData)
        edid[127] = 0
        self.assertFalse(edid.checkChecksum())

    def testCalculateChecksum(self):
        edid = EDID.EDID(data=bytearray(128))
        edid[-1] = 42

        edid.calculateChecksum()
        self.assertEqual(edid[127], 0x00)

    def testCalculateChecksum2(self):
        edid = EDID.EDID(data=bytearray(128))
        edid[0] = 1

        edid.calculateChecksum()
        self.assertEqual(edid[127], 255)

    def testCheckHeaderValid(self):
        edid = EDID.EDID(data=self.validEDIDData)
        self.assertTrue(edid.checkHeader())

    def testCheckHeaderInvalid(self):
        edid = EDID.EDID(data=bytearray(128))
        self.assertFalse(edid.checkHeader())

    def testSetHeader(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setHeader()
        self.assertEqual(edid[0:8],
                         bytearray.fromhex('00 FF FF FF FF FF FF 00'))

    def testSetManufacturerID(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setManufacturerID('SAM')
        self.assertEqual(edid[8:10], bytearray.fromhex('4C 2D'))

    def testGetManufacturerID(self):
        edid = EDID.EDID(data=self.validEDIDData)
        self.assertEqual(edid.getManufacturerID(), 'SAM')

    def testSetManufacturerProductCode(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setManufacturerProductCode(956)
        self.assertEqual(edid[10:12], bytearray.fromhex('BC 03'))

    def testGetManufacturerProductCode(self):
        edid = EDID.EDID(data=self.validEDIDData)
        self.assertEqual(edid.getManufacturerProductCode(), 956)

    def testSetSerialNumber(self):
        edid = EDID.EDID(data=bytearray(128))
        edid.setSerialNumber(12345678)
        self.assertEqual(edid[12:16], bytearray.fromhex('4E 61 BC 00'))

    def testGetSerialNumber(self):
        edid = EDID.EDID(data=bytearray(128))
        edid[12:16] = bytearray.fromhex('4E 61 BC 00')
        self.assertEqual(edid.getSerialNumber(), 12345678)