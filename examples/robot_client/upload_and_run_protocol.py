from time import sleep

from opentrons_http_api.robot_client import RobotClient, Action


ROBOT_IP = 'localhost'


robot = RobotClient(ROBOT_IP)

# Upload a protocol
with open('../example_protocol.py', 'rb') as f:
    protocol_info = robot.upload_protocol(f)

# Create and start a run
run_info = robot.create_run(protocol_info.id)
robot.action_run(run_info.id, Action.PLAY)

# Poll run status
while not run_info.status_.is_done:
    run_info = robot.run(run_info.id)
    print(run_info.status, [(error.errorType, error.detail)
                            for error in run_info.errors_])
    sleep(1)
