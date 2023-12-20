from typing import Dict
from unittest.mock import Mock, patch

import pytest
from requests import Response

from opentrons_http_api.api import API, SettingId, Axis, ActionType
from opentrons_http_api.paths import Paths


RESPONSE = {'response': 'response'}


@pytest.fixture
def api():
    yield API('some_host')


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


def test_setting_id():
    SettingId('shortFixedTrash')
    SettingId.SHORT_FIXED_TRASH


def test_axis():
    Axis('x')
    Axis.X


def test_action_type():
    ActionType('play')
    ActionType.PLAY


def test_cls(api):
    assert api._HEADERS == {'Opentrons-Version': '3'}


def test_init(api):
    assert api._base == 'http://some_host:31950'


def test_url(api):
    assert api._url('/path') == 'http://some_host:31950/path'


def test_get(api):
    """
    Tests API._get by mocking requests.get.
    """
    with patch('opentrons_http_api.api.requests.get') as mock_requests_get:
        with patch.object(api, '_check_response'):
            mock_response = Mock(spec=Response)
            mock_requests_get.return_value = mock_response

            path = '/path'

            # Call
            response = api._get(path)

            mock_requests_get.assert_called_once_with(api._url(path), headers=API._HEADERS)
            api._check_response.assert_called_once_with(mock_response)

            assert response == mock_response.json()


def test_post(api):
    """
    Tests API._post by mocking requests.post.
    """
    with patch('opentrons_http_api.api.requests.post') as mock_requests_post:
        with patch.object(api, '_check_response'):
            mock_response = Mock(spec=Response)
            mock_requests_post.return_value = mock_response

            path = '/path'
            params = {'foo': 123}
            body = {'data': 456}
            other = 'other'

            # Call
            response = api._post(path, query=params, body=body, other=other)

            mock_requests_post.assert_called_once_with(api._url(path), headers=API._HEADERS, params=params,
                                                       json=body, other=other)
            api._check_response.assert_called_once_with(mock_response)

            assert response == mock_response.json()


@pytest.mark.parametrize('method_name, path, kwargs', [
    ('get_robot_lights', Paths.ROBOT_LIGHTS, {}),
    ('get_settings', Paths.SETTINGS, {}),
    ('get_robot_settings', Paths.SETTINGS_ROBOT, {}),
    ('get_calibration_status', Paths.CALIBRATION_STATUS, {}),
    ('get_motors_engaged', Paths.MOTORS_ENGAGED, {}),
    ('get_health', Paths.HEALTH, {}),
    ('get_runs', Paths.RUNS, {}),
    ('get_runs_run_id', Paths.RUNS_RUN_ID, {'run_id': 'run_123'}),
    ('get_runs_run_id_commands', Paths.RUNS_RUN_ID_COMMANDS, {'run_id': 'run_123'}),
    ('get_runs_run_id_commands_command_id', Paths.RUNS_RUN_ID_COMMANDS_COMMAND_ID, {'run_id': 'run_123',
                                                                                    'command_id': 'command_123'}),
    ('get_protocols', Paths.PROTOCOLS, {}),
    ('get_protocols_protocol_id', Paths.PROTOCOLS_PROTOCOL_ID, {'protocol_id': 'protocol_123'}),
])
def test_get_methods(api_with_mock_get: API, method_name: str, path: str, kwargs: Dict):
    """
    Tests the API's get_* methods by mocking API._get.
    """
    assert getattr(api_with_mock_get, method_name)(**kwargs) == RESPONSE
    api_with_mock_get._get.assert_called_once_with(path.format(**kwargs))


@pytest.mark.parametrize('method_name, path, path_kwargs, kwargs_in, kwargs_out', [
    (
            'post_identify', Paths.IDENTIFY, {},
            {'seconds': 3},
            {'query': {'seconds': 3}},
    ),
    (
            'post_robot_lights', Paths.ROBOT_LIGHTS, {},
            {'on': True},
            {'body': {'on': True}},
    ),
    (
            'post_settings', Paths.SETTINGS, {},
            {'id_': SettingId.SHORT_FIXED_TRASH, 'value': True},
            {'body': {'id': SettingId.SHORT_FIXED_TRASH, 'value': True}},
    ),
    (
            'post_motors_disengage', Paths.MOTORS_DISENGAGE, {},
            {'axes': [Axis.X, Axis.Y]},
            {'body': {'axes': [Axis.X, Axis.Y]}},
    ),
    (
            'post_runs', Paths.RUNS, {'protocol_id': 'protocol_123'},
            {'labware_offsets': [{'labware': 'offsets'}]},
            {'body': {'data': {'protocolId': 'protocol_123', 'labwareOffsets': [{'labware': 'offsets'}]}}},
    ),
    (
            'post_runs_run_id_actions', Paths.RUNS_RUN_ID_ACTIONS, {'run_id': 'run_123'},
            {'action': ActionType.PLAY},
            {'body': {'data': {'actionType': ActionType.PLAY}}},
    ),
    (
            'post_protocols', Paths.PROTOCOLS, {},
            {'protocol_file': b'file_contents'},
            {'files': [('files', b'file_contents')]},
    ),
])
def test_post_methods(api_with_mock_post: API, method_name: str, path: str, path_kwargs: Dict, kwargs_in: Dict,
                      kwargs_out: Dict):
    """
    Tests the API's post_* methods by mocking API._post.
    """
    path = path.format(**path_kwargs)
    assert getattr(api_with_mock_post, method_name)(**path_kwargs, **kwargs_in) == RESPONSE
    api_with_mock_post._post.assert_called_once_with(path, **kwargs_out)
