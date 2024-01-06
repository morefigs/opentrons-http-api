from datetime import datetime

import pytest

from opentrons_http_api.defs.dict_data import Setting, RobotSettings, HealthInfo, RunInfo, ProtocolInfo


@pytest.fixture
def settings_info_data():
    return {
        'id': '123',
        'old_id': '456',
        'title': 'Test Title',
        'description': 'Test Description',
        'restart_required': True,
        'value': True
    }


@pytest.fixture
def robot_settings_info_data():
    return {
        'model': 'Test Model',
        'name': 'Test Name',
        'version': 1,
        'gantry_steps_per_mm': {'x': 1, 'y': 1, 'z': 1},
        'acceleration': {'x': 1, 'y': 1, 'z': 1},
        'serial_speed': 9600,
        'default_pipette_configs': {'config1': 'value1', 'config2': 'value2'},
        'default_current': {'x': 1, 'y': 1, 'z': 1},
        'low_current': {'x': 1, 'y': 1, 'z': 1},
        'high_current': {'x': 1, 'y': 1, 'z': 1},
        'default_max_speed': {'x': 1, 'y': 1, 'z': 1},
        'log_level': 'DEBUG',
        'z_retract_distance': 10,
        'left_mount_offset': [1, 2, 3]
    }


@pytest.fixture
def health_info_data():
    return {
        'name': 'Test Robot',
        'robot_model': 'Test Model',
        'api_version': '1.0',
        'fw_version': '1.0',
        'board_revision': '1.0',
        'logs': ['log1', 'log2'],
        'system_version': '1.0',
        'maximum_protocol_api_version': [1, 2],
        'minimum_protocol_api_version': [1, 2],
        'robot_serial': '123456',
        'links': {'link1': 'url1', 'link2': 'url2'}
    }


@pytest.fixture
def run_info_data():
    return {
        'id': '789',
        'createdAt': str(datetime.now()),
        'status': 'running',
        'current': True,
        'actions': [{'action1': 'param1'}, {'action2': 'param2'}],
        'errors': [{'error1': 'message1'}, {'error2': 'message2'}],
        'pipettes': [{'pipette1': 'type1'}, {'pipette2': 'type2'}],
        'modules': [{'module1': 'type1'}, {'module2': 'type2'}],
        'labware': [{'labware1': 'type1'}, {'labware2': 'type2'}],
        'liquids': [{'liquid1': 'type1'}, {'liquid2': 'type2'}],
        'labwareOffsets': [{'offset1': 'value1'}, {'offset2': 'value2'}],
        'protocolId': 'protocol123',
        'completedAt': str(datetime.now()),
        'startedAt': str(datetime.now())
    }


@pytest.fixture
def protocol_info_data():
    return {
        'id': 'protocol123',
        'createdAt': str(datetime.now()),
        'files': [{'file1': 'path1'}, {'file2': 'path2'}],
        'protocolType': 'test_protocol',
        'robotType': 'test_robot',
        'metadata': {'key1': 'value1', 'key2': 'value2'},
        'analyses': [{'analysis1': 'result1'}, {'analysis2': 'result2'}],
        'analysisSummaries': [{'summary1': 'result1'}, {'summary2': 'result2'}]
    }


def test_settings_info(settings_info_data):
    settings_info = Setting(**settings_info_data)
    assert settings_info.id == '123'
    assert settings_info.title == 'Test Title'


def test_robot_settings_info(robot_settings_info_data):
    robot_settings_info = RobotSettings(**robot_settings_info_data)
    assert robot_settings_info.model == 'Test Model'
    assert robot_settings_info.serial_speed == 9600


def test_health_info_creation(health_info_data):
    health_info = HealthInfo(**health_info_data)
    assert health_info.name == 'Test Robot'
    assert health_info.logs == ['log1', 'log2']


def test_run_info_creation(run_info_data):
    run_info = RunInfo(**run_info_data)
    assert run_info.id == '789'
    assert run_info.status == 'running'


def test_protocol_info_creation(protocol_info_data):
    protocol_info = ProtocolInfo(**protocol_info_data)
    assert protocol_info.id == 'protocol123'
    assert protocol_info.protocolType == 'test_protocol'
