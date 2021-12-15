"""Pack object in msgpack format

The msgpack format is similar to json, except that the encoded data is binary.
See https://msgpack.org for details. The module implements a subset of the cpython
module msgpack-python.

Not implemented: 64-bit int, uint, float.

Example 1::

   import msgpack
   from io import BytesIO

   b = BytesIO()
   msgpack.pack({'list': [True, False, None, 1, 3.14], 'str': 'blah'}, b)
   b.seek(0)
   print(msgpack.unpack(b))

Example 2: handling objects::

   from msgpack import pack, unpack, ExtType
   from io import BytesIO

   class MyClass:
       def __init__(self, val):
           self.value = val
       def __str__(self):
           return str(self.value)

   data = MyClass(b'my_value')

   def encoder(obj):
       if isinstance(obj, MyClass):
           return ExtType(1, obj.value)
       return f"no encoder for {obj}"

   def decoder(code, data):
       if code == 1:
           return MyClass(data)
       return f"no decoder for type {code}"

   buffer = BytesIO()
   pack(data, buffer, default=encoder)
   buffer.seek(0)
   decoded = unpack(buffer, ext_hook=decoder)
   print(f"{data} -> {buffer.getvalue()} -> {decoded}")

"""

from __future__ import annotations

from typing import Callable, Union

from _typing import ReadableBuffer, WriteableBuffer

def pack(
    obj: object,
    buffer: WriteableBuffer,
    *,
    default: Union[Callable[[object], None], None] = None
) -> None:
    """Ouput object to buffer in msgpack format.

    :param object obj: Object to convert to msgpack format.
    :param ~_typing.WriteableBuffer buffer: buffer to write into
    :param Optional[~_typing.Callable[[object], None]] default:
          function called for python objects that do not have
          a representation in msgpack format.
    """
    ...

def unpack(
    buffer: ReadableBuffer,
    *,
    ext_hook: Union[Callable[[int, bytes], object], None] = None,
    use_list: bool = True
) -> object:
    """Unpack and return one object from buffer.

    :param ~_typing.ReadableBuffer buffer: buffer to read from
    :param Optional[~_typing.Callable[[int, bytes], object]] ext_hook: function called for objects in
           msgpack ext format.
    :param Optional[bool] use_list: return array as list or tuple (use_list=False).

    :return object: object read from buffer.
    """
    ...

class ExtType:
    """ExtType represents ext type in msgpack."""

    def __init__(self, code: int, data: bytes) -> None:
        """Constructor
        :param int code: type code in range 0~127.
        :param bytes data: representation."""
    code: int
    """The type code, in range 0~127."""
    ...

    data: bytes
    """Data."""
    ...
