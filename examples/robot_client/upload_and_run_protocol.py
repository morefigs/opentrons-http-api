from opentrons_http_api.robot_client import RobotClient, Action


ROBOT_IP = 'localhost'


robot = RobotClient(ROBOT_IP)

# Upload a protocol
with open('../example_protocol.py', 'rb') as f:
    protocol_info = robot.upload_protocol(f)

# Create a run
run_info = robot.create_run(protocol_info.id)

# Start the run
robot.action_run(run_info.id, Action.PLAY)

# Check run status
print(robot.run(run_info.id).status)
