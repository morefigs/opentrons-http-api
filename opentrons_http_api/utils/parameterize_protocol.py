import re
from typing import BinaryIO, Sequence, Union, Type
from dataclasses import dataclass


@dataclass(frozen=True)
class Parameter:
    """
    A parameter name and value to replace a string token in a protocol file with.

    For example, Parameter('some_name', int, 123) would replace the instance of '''some_name''' with 123 within the
    contents of a protocol file.
    """
    name: str
    type: Union[Type[int], Type[float], Type[str]]
    value: object

    @staticmethod
    def is_safe_str(string: str) -> bool:
        """
        Checks string is empty or contains only lowercase letters, numbers, and underscores.
        """
        return bool(re.match(r'^[a-z0-9_]*$', string))

    def __post_init__(self):
        if not type(self.value) is self.type:
            raise ValueError(f'expected type "{self.type}" but got {type(self.value)}')

        # Prevent code injection
        if self.type is str and not self.is_safe_str(self.value):
            raise ValueError('string values must only contain lower case letters, numbers, and underscores')

    @property
    def token_b(self) -> bytes:
        """
        The full token with quotes, as bytes, e.g. b'''some_name'''.
        """
        return f"'''{self.name}'''".encode()

    @property
    def value_b(self) -> bytes:
        """
        The value as bytes.
        """
        return f'{self.value}'.encode()


def parameterize_protocol(buffer_in: BinaryIO, buffer_out: BinaryIO, params: Sequence[Parameter]) -> None:
    """
    Replaces parameter tokens with their values in a protocol file binary object as a means of dynamically enabling
    parameters to be injected into an otherwise fixed parameter file.
    :param buffer_in: The protocol file buffer to insert parameters into.
    :param buffer_out: The output protocol file buffer with parameters injected.
    :param params: The parameter names and values to replace.
    """
    if buffer_in is buffer_out:
        raise ValueError("buffer_in and buffer_out can't be the same")

    contents = buffer_in.read()

    for param in params:
        # Check exactly one of each token exists
        count = contents.count(param.token_b)
        if count != 1:
            raise ValueError(f'expected 1 occurrence of "{param.token_b}", but got {count} occurrences')

        # Replace parameter tokens
        contents = contents.replace(param.token_b, param.value_b)

    buffer_out.write(contents)
    buffer_out.seek(0)
