from opentrons_http_api.robot_client import RobotClient


ROBOT_IP = 'localhost'


robot = RobotClient(ROBOT_IP)
print(robot.robot_settings())
