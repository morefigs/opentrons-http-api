from opentrons_http_api.robot import Robot
from opentrons_http_api.utils.parameterize_protocol import parameterize_protocol, Parameter


ROBOT_IP = 'localhost'
PARAMS = (
    Parameter('num_flashes', 3),
    Parameter('delay_s', 0.2),
)


robot = Robot(ROBOT_IP)

# Doesn't work with buffer_out as a BytesIO or tempfile object
with open('_temp.py', 'w+b') as buffer_out:
    with open('../example_parameterized_protocol.py', 'rb') as buffer_in:
        parameterize_protocol(buffer_in, buffer_out, PARAMS)

    print(robot.upload_protocol(buffer_out))
