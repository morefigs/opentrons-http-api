from typing import Sequence, BinaryIO
import json
import urllib

import requests

from opentrons_http_api.paths import Paths


class API:
    _HEADERS = {'Opentrons-Version': '3'}
    _PORT = 31950
    _BASE = 'http://{host}:{port}'

    def __init__(self, host: str = 'localhost'):
        self._base = self._BASE.format(host=host, port=self._PORT)

    def _url(self, path):
        return urllib.parse.urljoin(self._base, path)

    @staticmethod
    def _check_response(response: requests.Response):
        response.raise_for_status()

    def _get(self, path: str) -> requests.Response:
        response = requests.get(self._url(path), headers=self._HEADERS)
        self._check_response(response)
        return response

    def _post(self, path: str, data=None, **kwargs) -> requests.Response:
        response = requests.post(self._url(path), data, headers=self._HEADERS, **kwargs)
        self._check_response(response)
        return response

    # v1

    # NETWORKING

    # CONTROL

    def post_identify(self, seconds: int) -> requests.Response:
        """
        Blink the OT-2's gantry lights so you can pick it out of a crowd.
        """
        data = {'seconds': seconds}
        return self._post(Paths.IDENTIFY, json.dumps(data))

    def get_robot_lights(self) -> requests.Response:
        """
        Get the current status of the OT-2's rail lights.
        """
        return self._get(Paths.ROBOT_LIGHTS)

    def post_robot_lights(self, on: bool) -> requests.Response:
        """
        Turn the rail lights on or off.
        """
        data = {'on': on}
        return self._post(Paths.ROBOT_LIGHTS, json.dumps(data))

    # SETTINGS

    def get_settings(self) -> requests.Response:
        """
        Get a list of available advanced settings (feature flags) and their values.
        """
        return self._get(Paths.SETTINGS)

    def post_settings(self, id_: str, value: bool):
        """
        Change an advanced setting (feature flag).
        """
        data = {'id': id_, 'value': value}
        return self._post(Paths.SETTINGS, json.dumps(data))

    def get_robot_settings(self) -> requests.Response:
        """
        Get the current robot config.
        """
        return self._get(Paths.SETTINGS_ROBOT)

    # DECK CALIBRATION

    def get_calibration_status(self) -> requests.Response:
        """
        Get the calibration status.
        """
        return self._get(Paths.CALIBRATION_STATUS)

    # MODULES

    # PIPETTES

    # MOTORS

    def get_motors_engaged(self) -> requests.Response:
        """
        Query which motors are engaged and holding.
        """
        return self._get(Paths.MOTORS_ENGAGED)

    def post_motors_disengage(self, axes: Sequence[str]) -> requests.Response:
        """
        Disengage a motor or set of motors.
        """
        data = {'axes': axes}
        return self._post(Paths.MOTORS_DISENGAGE, json.dumps(data))

    # CAMERA

    def get_camera_picture(self) -> requests.Response:
        """
        Capture an image from the OT-2's on-board camera and return it.
        """
        return self._get(Paths.CAMERA_PICTURE)

    # LOGS

    # HEALTH

    def get_health(self) -> requests.Response:
        """
        Get information about the health of the robot server.

        Use the health endpoint to check that the robot server is running and ready to operate. A 200 OK response means
        the server is running. The response includes information about the software and system.
        """
        return self._get(Paths.HEALTH)

    # RUN MANAGEMENT

    def get_runs(self) -> requests.Response:
        """
        Get a list of all active and inactive runs.
        """
        return self._get(Paths.RUNS)

    def post_runs(self, data: dict) -> requests.Response:
        """
        Create a new run to track robot interaction.

        When too many runs already exist, old ones will be automatically deleted to make room for the new one.
        """
        return self._post(Paths.RUNS, json.dumps(data))

    def get_runs_run_id(self, run_id: str) -> requests.Response:
        """
        Get a specific run by its unique identifier.
        """
        return self._get(Paths.RUNS_RUN_ID.format(run_id=run_id))

    def get_runs_run_id_commands(self, run_id: str) -> requests.Response:
        """
        Get a list of all commands in the run and their statuses. This endpoint returns command summaries. Use GET
        /runs/{runId}/commands/{commandId} to get all information available for a given command.
        """
        return self._get(Paths.RUNS_RUN_ID_COMMANDS.format(run_id=run_id))

    def get_runs_run_id_commands_command_id(self, run_id: str, command_id: str) -> requests.Response:
        """
        Get a command along with any associated payload, result, and execution information.
        """
        return self._get(Paths.RUNS_RUN_ID_COMMANDS_COMMAND_ID.format(run_id=run_id, command_id=command_id))

    def post_runs_run_id_actions(self, run_id: str, data: dict) -> requests.Response:
        """
        Provide an action in order to control execution of the run.
        """
        return self._post(Paths.RUNS_RUN_ID_ACTIONS.format(run_id=run_id), json.dumps(data))

    # MAINTENANCE RUN MANAGEMENT

    # PROTOCOL MANAGEMENT

    def get_protocols(self) -> requests.Response:
        """
        Get a list of all currently uploaded protocols.
        """
        return self._get(Paths.PROTOCOLS)

    def post_protocols(self, files: Sequence[BinaryIO]) -> requests.Response:
        """
        Upload a protocol to your device. You may include the following files:

        * A single Python protocol file and 0 or more custom labware JSON files
        * A single JSON protocol file (any additional labware files will be ignored)

        When too many protocols already exist, old ones will be automatically deleted to make room for the new one. A
        protocol will never be automatically deleted if there's a run referring to it, though.
        """
        files = [('files', f) for f in files]
        return self._post(Paths.PROTOCOLS, files=files)

    def get_protocols_protocol_id(self, protocol_id: str) -> requests.Response:
        """
        Get an uploaded protocol by ID.
        """
        return self._get(Paths.PROTOCOLS_PROTOCOL_ID.format(protocol_id=protocol_id))

    # SIMPLE COMMANDS

    # DECK CONFIGURATION

    # ATTACHED MODULES

    # ATTACHED INSTRUMENTS

    # SESSION MANAGEMENT

    # LABWARE CALIBRATION MANAGEMENT

    # PIPETTE OFFSET CALIBRATION MANAGEMENT

    # TIP LENGTH CALIBRATION MANAGEMENT

    # SYSTEM CONTROL

    # SUBSYSTEM MANAGEMENT
