"""
Requires a connection to a real device or simulator (see
https://github.com/Opentrons/opentrons/blob/edge/robot-server/README.rst#simulators). A simulator will perform faster
than real hardware. This will change the state of the hardware.
"""
import pytest

from opentrons_http_api.api import API, SettingId, Axis, ActionType


# Host of a real or simulated device
HOST = 'localhost'


@pytest.fixture
def api():
    yield API(HOST)


def test_api_on_hardware(api: API):
    # General
    api.post_identify(2)
    api.get_robot_lights()
    api.post_robot_lights(False)
    api.get_settings()
    api.post_settings(SettingId.SHORT_FIXED_TRASH, False)
    api.get_robot_settings()
    api.get_calibration_status()
    api.get_motors_engaged()
    api.post_motors_disengage([Axis.X, Axis.Y])
    api.get_health()

    # Protocols
    api.get_protocols()
    with open('../examples/example_protocol.py', 'rb') as f:
        d = api.post_protocols(f)
    protocol_id = d['data']['id']
    api.get_protocols_protocol_id(protocol_id=protocol_id)

    # Runs
    api.get_runs()
    d = api.post_runs(protocol_id=protocol_id)
    run_id = d['data']['id']
    api.get_runs_run_id(run_id=run_id)
    d = api.get_runs_run_id_commands(run_id=run_id)
    command_id = d['data'][0]['id']
    api.get_runs_run_id_commands_command_id(run_id=run_id, command_id=command_id)
    api.post_runs_run_id_actions(run_id=run_id, action=ActionType.STOP)
