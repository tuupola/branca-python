# Copyright 2018 Mika Tuupola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of  this software and associated documentation files (the "Software"), to
# deal in  the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copied of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from branca import Branca
from binascii import unhexlify, hexlify
import base62
import pytest
import struct
import xchacha20poly1305

def test_vector1():
    branca = Branca(key="supersecretkeyyoushouldnotcommit")
    branca._nonce = unhexlify("0102030405060708090a0b0c0102030405060708090a0b0c")
    token = branca.encode("Hello world!", timestamp=123206400)

    assert token == "875GH233T7IYrxtgXxlQBYiFobZMQdHAT51vChKsAIYCFxZtL1evV54vYqLyZtQ0ekPHt8kJHQp0a"

def test_vector2():
    branca = Branca(key="supersecretkeyyoushouldnotcommit")
    branca._nonce = unhexlify("0102030405060708090a0b0c0102030405060708090a0b0c")
    token = branca.encode("Hello world!", timestamp=123206400)

    with pytest.raises(RuntimeError):
        branca.decode(token, 3600)

def test_encode_and_decode():
    branca = Branca(key="supersecretkeyyoushouldnotcommit")
    token = branca.encode("Hello world!")
    decoded = branca.decode(token)

    assert decoded == "Hello world!"

def test_encode_with_timestamp():
    branca = Branca(key="supersecretkeyyoushouldnotcommit")
    token = branca.encode("Hello world!", timestamp=123206400)
    binary = base62.decodebytes(token)
    version, timestamp = struct.unpack(">BL", bytes(binary[0:5]))

    assert version == 0xba
    assert timestamp == 123206400

def test_encode_with_zero_timestamp():
    branca = Branca(key="supersecretkeyyoushouldnotcommit")
    token = branca.encode("Hello world!", timestamp=0)
    binary = base62.decodebytes(token)
    version, timestamp = struct.unpack(">BL", bytes(binary[0:5]))

    assert version == 0xba
    assert timestamp == 0

def test_should_throw_with_invalid_token():
    branca = Branca(key="supersecretkeyyoushouldnotcommit")
    token = branca.encode("Hello world!")

    with pytest.raises(RuntimeError):
        decoded = branca.decode("XX" + token + "XX")
