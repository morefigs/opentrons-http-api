from datetime import datetime

import pytest

from opentrons_http_api.defs.dict_data import Vector, LabwareOffset, Setting, RobotSettings, HealthInfo, RunInfo, \
    ProtocolInfo, EngineStatus


@pytest.fixture
def vector_data():
    return {
        'x': '1.23',
        'y': '4.56',
        'z': '99',
    }


@pytest.fixture
def labware_offset_data(vector_data):
    return {
        'id': '99',
        'createdAt': str(datetime.now()),
        'definitionUri': 'opentrons/labware/1',
        'location': {'slotName': 2},
        'vector': vector_data,
    }


@pytest.fixture
def setting_data():
    return {
        'id': '123',
        'old_id': '456',
        'title': 'Test Title',
        'description': 'Test Description',
        'restart_required': True,
        'value': True
    }


@pytest.fixture
def robot_settings_data():
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
def run_info_data(labware_offset_data):
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
        'labwareOffsets': [labware_offset_data, labware_offset_data],
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


def test_vector(vector_data):
    vector = Vector(**vector_data)
    assert vector.x == '1.23'


def test_labware_offset(labware_offset_data, vector_data):
    labware_offset = LabwareOffset(**labware_offset_data)
    assert labware_offset.id == '99'
    assert labware_offset.definitionUri == 'opentrons/labware/1'
    assert labware_offset.vector_.dict() == vector_data

    labware_offset = LabwareOffset.create(labware_offset.definitionUri, labware_offset.location, labware_offset.vector)
    assert labware_offset.vector == vector_data

    labware_offset = LabwareOffset.create(labware_offset.definitionUri, labware_offset.location, Vector(**vector_data))
    assert labware_offset.vector == vector_data


def test_setting(setting_data):
    setting = Setting(**setting_data)
    assert setting.id == '123'
    assert setting.title == 'Test Title'


def test_robot_settings(robot_settings_data):
    robot_settings = RobotSettings(**robot_settings_data)
    assert robot_settings.model == 'Test Model'
    assert robot_settings.serial_speed == 9600


def test_health_info(health_info_data):
    health_info = HealthInfo(**health_info_data)
    assert health_info.name == 'Test Robot'
    assert health_info.logs == ['log1', 'log2']


def test_run_info(run_info_data, labware_offset_data):
    run_info = RunInfo(**run_info_data)
    assert run_info.id == '789'
    assert run_info.status == 'running'
    assert run_info.status_.status == EngineStatus('running')
    assert run_info.status_.is_active
    assert not run_info.status_.is_idle
    assert not run_info.status_.is_completed
    assert run_info.labwareOffsets_[0].dict() == labware_offset_data


def test_protocol_info(protocol_info_data):
    protocol_info = ProtocolInfo(**protocol_info_data)
    assert protocol_info.id == 'protocol123'
    assert protocol_info.protocolType == 'test_protocol'
