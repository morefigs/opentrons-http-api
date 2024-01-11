from opentrons_http_api.robot_client import RobotClient


ROBOT_IP = 'localhost'


robot = RobotClient(ROBOT_IP)
robot.set_lights(True)
assert robot.lights()
