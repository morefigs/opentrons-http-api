from unittest.mock import Mock, patch
import json

import pytest
from requests import Response

from opentrons_http_api.api import API
from opentrons_http_api.paths import Paths


RESPONSE = Response()


@pytest.fixture
def api():
    yield API()


@pytest.fixture
def api_with_mock_get(api):
    with patch.object(api, '_get') as mock_get:
        mock_get.return_value = RESPONSE
        yield api


@pytest.fixture
def api_with_mock_post(api):
    with patch.object(api, '_post') as mock_post:
        mock_post.return_value = RESPONSE
        yield api


def test_cls(api):
    assert api._HEADERS == {'Opentrons-Version': '3'}


def test_init(api):
    assert api._base == 'http://localhost:31950'


def test_url(api):
    assert api._url('/path') == 'http://localhost:31950/path'


def test_get(api):
    with patch('opentrons_http_api.api.requests.get') as mock_get:
        with patch.object(api, '_check_response'):
            mock_response = Mock(spec=Response)
            mock_get.return_value = mock_response

            path = '/path'
            response = api._get(path)

            assert response == mock_response
            mock_get.assert_called_once_with(api._url(path), headers=API._HEADERS)
            api._check_response.assert_called_once_with(mock_response)


def test_post(api):
    with patch('opentrons_http_api.api.requests.post') as mock_post:
        with patch.object(api, '_check_response'):
            mock_response = Mock(spec=Response)
            mock_post.return_value = mock_response

            path = '/path'
            data = json.dumps({'foo': 123})
            other = 'bar'
            response = api._post(path, data, other=other)

            assert response == mock_response
            mock_post.assert_called_once_with(api._url(path), data, headers=API._HEADERS, other=other)
            api._check_response.assert_called_once_with(mock_response)


def test_post_identify(api_with_mock_post):
    seconds = 5
    assert api_with_mock_post.post_identify(seconds) == RESPONSE
    data = json.dumps({'seconds': seconds})
    api_with_mock_post._post.assert_called_once_with(Paths.IDENTIFY, data)


def test_get_robot_lights(api_with_mock_get):
    assert api_with_mock_get.get_robot_lights() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.ROBOT_LIGHTS)


@pytest.mark.parametrize('on', [
    True,
    False,
])
def test_post_robot_lights(api_with_mock_post, on):
    assert api_with_mock_post.post_robot_lights(on=on) == RESPONSE
    data = json.dumps({'on': on})
    api_with_mock_post._post.assert_called_once_with(Paths.ROBOT_LIGHTS, data)


def test_get_settings(api_with_mock_get):
    assert api_with_mock_get.get_settings() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.SETTINGS)


@pytest.mark.parametrize('id_, value', [
    ('feature_flag_1', True),
    ('feature_flag_2', False),
])
def test_post_settings(api_with_mock_post, id_, value):
    assert api_with_mock_post.post_settings(id_, value) == RESPONSE
    data = json.dumps({'id': id_, 'value': value})
    api_with_mock_post._post.assert_called_once_with(Paths.SETTINGS, data)


def test_get_robot_settings(api_with_mock_get):
    assert api_with_mock_get.get_robot_settings() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.SETTINGS_ROBOT)


def test_get_calibration_status(api_with_mock_get):
    assert api_with_mock_get.get_calibration_status() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.CALIBRATION_STATUS)


def test_get_motors_engaged(api_with_mock_get):
    assert api_with_mock_get.get_motors_engaged() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.MOTORS_ENGAGED)


@pytest.mark.parametrize('axes', [
    ['x', 'y'],
    ['a'],
])
def test_post_motors_disengage(api_with_mock_post, axes):
    assert api_with_mock_post.post_motors_disengage(axes) == RESPONSE
    data = json.dumps({'axes': axes})
    api_with_mock_post._post.assert_called_once_with(Paths.MOTORS_DISENGAGE, data)


def test_get_camera_picture(api_with_mock_get):
    assert api_with_mock_get.get_camera_picture() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.CAMERA_PICTURE)


def test_get_health(api_with_mock_get):
    assert api_with_mock_get.get_health() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.HEALTH)


def test_get_runs(api_with_mock_get):
    assert api_with_mock_get.get_runs() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.RUNS)


@pytest.mark.parametrize('data', [
    {
        'protocolId': 'protocol_id_1',
        'labwareOffsets': [
            {
                'definitionUri': 'string',
                'location': {
                    'slotName': '1',
                    'moduleModel': 'temperatureModuleV1',
                    'definitionUri': 'string'
                },
                'vector': {
                    'x': 0,
                    'y': 0,
                    'z': 0
                }
            }
        ]
    }
])
def test_post_runs(api_with_mock_post, data):
    assert api_with_mock_post.post_runs(data) == RESPONSE
    api_with_mock_post._post.assert_called_once_with(Paths.RUNS, json.dumps(data))


@pytest.mark.parametrize('run_id', [
    'run_id_1',
    'run_id_2',
])
def test_get_runs_run_id(api_with_mock_get, run_id):
    assert api_with_mock_get.get_runs_run_id(run_id) == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.RUNS_RUN_ID.format(run_id=run_id))


@pytest.mark.parametrize('run_id', [
    'run_id_1',
    'run_id_2',
])
def test_get_runs_run_id_commands(api_with_mock_get, run_id):
    assert api_with_mock_get.get_runs_run_id_commands(run_id) == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.RUNS_RUN_ID_COMMANDS.format(run_id=run_id))


@pytest.mark.parametrize('run_id, command_id', [
    ('run_id_1', 'command_id_1'),
    ('run_id_2', 'command_id_2'),
])
def test_get_runs_run_id_commands_command_id(api_with_mock_get, run_id, command_id):
    assert api_with_mock_get.get_runs_run_id_commands_command_id(run_id, command_id) == RESPONSE
    api_with_mock_get._get.assert_called_once_with(
        Paths.RUNS_RUN_ID_COMMANDS_COMMAND_ID.format(run_id=run_id, command_id=command_id)
    )


@pytest.mark.parametrize('run_id, data', [
    ('run_id_1', {'actionType': 'play'}),
    ('run_id_2', {'actionType': 'pause'}),
])
def test_post_runs_run_id_actions(api_with_mock_post, run_id, data):
    assert api_with_mock_post.post_runs_run_id_actions(run_id, data) == RESPONSE
    api_with_mock_post._post.assert_called_once_with(Paths.RUNS_RUN_ID_ACTIONS.format(run_id=run_id), json.dumps(data))


def test_get_protocols(api_with_mock_get):
    assert api_with_mock_get.get_protocols() == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.PROTOCOLS)


@pytest.mark.parametrize('files', [
    [],
    ['file_1', 'file_2'],
])
def test_post_protocols(api_with_mock_post, files):
    assert api_with_mock_post.post_protocols(files) == RESPONSE
    api_with_mock_post._post.assert_called_once_with(Paths.PROTOCOLS, files=[('files', f) for f in files])


@pytest.mark.parametrize('protocol_id', [
    'protocol_id_1',
    'protocol_id_2',
])
def test_get_protocols_protocol_id(api_with_mock_get, protocol_id):
    assert api_with_mock_get.get_protocols_protocol_id(protocol_id) == RESPONSE
    api_with_mock_get._get.assert_called_once_with(Paths.PROTOCOLS_PROTOCOL_ID.format(protocol_id=protocol_id))
