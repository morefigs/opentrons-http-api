from opentrons_http_api.robot import Robot


ROBOT_IP = 'localhost'


robot = Robot(ROBOT_IP)
robot.identify(3)
