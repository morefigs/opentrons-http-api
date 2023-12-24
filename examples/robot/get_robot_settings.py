from opentrons_http_api.robot import Robot


ROBOT_IP = 'localhost'


robot = Robot(ROBOT_IP)
print(robot.robot_settings())
