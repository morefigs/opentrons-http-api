from io import BytesIO

import pytest

from opentrons_http_api.utils.parameterize_protocol import Parameter, parameterize_protocol


@pytest.mark.parametrize('name, value, full_name_b, value_b', [
    ('foo', 123, b"'''foo'''", b'123'),
    ('foo', '123', b"'''foo'''", b'123'),
])
def test_parameter(name: str, value: object, full_name_b: bytes, value_b: bytes):
    param = Parameter(name, value)
    assert param.full_name_b == full_name_b
    assert param.value_b == value_b


@pytest.mark.parametrize('type_, value', [
    (int, 'foo'),
    (str, 123),
])
def test_parameter_type_check(type_, value):
    with pytest.raises(ValueError):
        Parameter('name', type_, value)


def test_parameterize_protocol():
    # Test correct usage
    buffer_out = BytesIO()
    parameterize_protocol(
        BytesIO(b"NUM_FLASHES = '''num_flashes'''\nDELAY_S = '''delay_s'''"),
        buffer_out,
        [Parameter('num_flashes', 3), Parameter('delay_s', 0.2)]
    )
    assert buffer_out.read() == b"NUM_FLASHES = 3\nDELAY_S = 0.2"

    # Test same buffer error
    buffer = BytesIO()
    with pytest.raises(ValueError):
        parameterize_protocol(buffer, buffer, [])

    # Test missing protocol
    with pytest.raises(ValueError):
        parameterize_protocol(
            BytesIO(b"NUM_FLASHES = '''num_flashes'''\nDELAY_S = '''delay_s'''"),
            BytesIO(),
            [Parameter('num_flashes', 3), Parameter('delay_s', 0.2), Parameter('fake', 123)]
        )
