from opentrons_http_api.defs.enums import SettingId, Axis, Action


def test_setting_id():
    SettingId('shortFixedTrash')
    SettingId.SHORT_FIXED_TRASH


def test_axis():
    Axis('x')
    Axis.X


def test_action_type():
    Action('play')
    Action.PLAY
