from io import BytesIO
from typing import Union, Type

import pytest

from opentrons_http_api.utils.parameterize_protocol import Parameter, parameterize_protocol


@pytest.mark.parametrize('name, type_, value, token_b, value_b', [
    ('foo', int, 123, b"'''parameter: foo'''", b'123'),
    ('foo', str, '123', b"'''parameter: foo'''", b'"123"'),
    ('foo', str, 'bar', b"'''parameter: foo'''", b'"bar"'),
])
def test_parameter(name: str, type_: Union[Type[int], Type[float], Type[str]], value: object, token_b: bytes,
                   value_b: bytes):
    param = Parameter(name, type_, value)
    assert param.token_b == token_b
    assert param.value_b == value_b


@pytest.mark.parametrize('type_, value', [
    (int, 'foo'),
    (str, 123),
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


def test_parameterize_protocol():
    # Test correct usage
    buffer_out = BytesIO()
    parameterize_protocol(
        BytesIO(b"NUM_FLASHES = '''parameter: num_flashes'''\nDELAY_S = '''parameter: delay_s'''"),
        buffer_out,
        [Parameter('num_flashes', int, 3), Parameter('delay_s', float, 0.2)]
    )
    assert buffer_out.read() == b"NUM_FLASHES = 3\nDELAY_S = 0.2"

    # Test same buffer error
    buffer = BytesIO()
    with pytest.raises(ValueError):
        parameterize_protocol(buffer, buffer, [])

    # Test extra parameter
    with pytest.raises(ValueError):
        parameterize_protocol(
            BytesIO(b"NUM_FLASHES = '''parameter: num_flashes'''\nDELAY_S = '''parameter: delay_s'''"),
            BytesIO(),
            [Parameter('num_flashes', int, 3), Parameter('delay_s', float, 0.2), Parameter('fake', int, 123)]
        )

    # Test missing parameter
    with pytest.raises(ValueError):
        parameterize_protocol(
            BytesIO(b"NUM_FLASHES = '''parameter: num_flashes'''\nDELAY_S = '''parameter: delay_s'''"),
            BytesIO(),
            [Parameter('num_flashes', int, 3)]
        )
