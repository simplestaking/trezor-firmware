from ubinascii import unhexlify

from common import *

from apps.aeternity.sign_tx import (
    write_uint_arbitrary_be
)


class TestAeternityEncoding(unittest.TestCase):
    def test_aeternity_encode_zarith(self):
        inputs = [2000000, 159066, 200, 60000, 157000000, 0]
        outputs = ["80897a", "dada09", "c801", "e0d403", "c0c2ee4a", "00"]

        for i, o in zip(inputs, outputs):
            w = bytearray()
            _encode_zarith(w, i)
            self.assertEqual(bytes(w), unhexlify(o))


if __name__ == "__main__":
    unittest.main()
