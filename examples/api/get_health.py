from opentrons_http_api.api import API


ROBOT_IP = 'localhost'


api = API(ROBOT_IP)
print(api.get_health())
