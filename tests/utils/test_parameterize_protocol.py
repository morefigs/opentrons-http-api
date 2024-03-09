from io import BytesIO
from typing import Union, Type

import pytest

from opentrons_http_api.utils.parameterize_protocol import Parameter, inject_parameters


@pytest.mark.parametrize('name, type_, value, token_b, value_b', [
    ('foo', int, 123, b"'''parameter: foo'''", b'123'),
    ('foo', str, '123', b"'''parameter: foo'''", b'"123"'),
    ('foo', str, 'bar', b"'''parameter: foo'''", b'"bar"'),
    ('foo', list, [1, 2, 3], b"'''parameter: foo'''", b'[1, 2, 3]'),
    ('foo', list, [1], b"'''parameter: foo'''", b'[1]'),
    ('foo', tuple, (1, 2, 3), b"'''parameter: foo'''", b'(1, 2, 3)'),
    ('foo', tuple, (1,), b"'''parameter: foo'''", b'(1,)'),
    ('foo', dict, {'a': 1, 'b': 2}, b"'''parameter: foo'''", b"{'a': 1, 'b': 2}"),

])
def test_parameter(name: str,
                   type_: Union[Type[int], Type[float], Type[str], Type[list], Type[tuple]],
                   value: Union[int, float, str, list, tuple],
                   token_b: bytes,
                   value_b: bytes):
    param = Parameter(name, type_, value)
    assert param.token_b == token_b
    assert param.value_b == value_b


@pytest.mark.parametrize('type_, value', [
    (int, 'foo'),
    (list, 'foo'),
    (list, {'a': 1, 'b': 2}),
    (str, 123),
    (list, 123),
    (tuple, 123),
    (dict, 123),
])
def test_parameter_type_check(type_, value):
    with pytest.raises(ValueError):
        Parameter('name', type_, value)


@pytest.mark.parametrize('safe, string', [
    (True, 'foo'),
    (True, 'foo_bar_123'),
    (True, ''),
    (False, '"'),
    (False, '""'),
    (False, '\"'),
    (False, '"print(123)'),
])
def test_parameter_safe_str_check(safe, string):
    assert safe is Parameter.is_safe_str(string)

    if safe:
        Parameter('name', str, string)
    else:
        with pytest.raises(ValueError):
            Parameter('name', str, string)


def test_inject_parameters():
    # Test correct usage
    buffer_out = BytesIO()
    assert inject_parameters(
        b"NUM_FLASHES = '''parameter: num_flashes'''\nDELAY_S = '''parameter: delay_s'''",
        [Parameter('num_flashes', int, 3), Parameter('delay_s', float, 0.2)]
    ) == b"NUM_FLASHES = 3\nDELAY_S = 0.2"

    # Test extra parameter
    with pytest.raises(ValueError):
        inject_parameters(
            b"NUM_FLASHES = '''parameter: num_flashes'''\nDELAY_S = '''parameter: delay_s'''",
            [Parameter('num_flashes', int, 3), Parameter('delay_s', float, 0.2), Parameter('fake', int, 123)]
        )

    # Test missing parameter
    with pytest.raises(ValueError):
        inject_parameters(
            b"NUM_FLASHES = '''parameter: num_flashes'''\nDELAY_S = '''parameter: delay_s'''",
            [Parameter('num_flashes', int, 3)]
        )
