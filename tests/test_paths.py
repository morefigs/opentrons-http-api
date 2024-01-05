from opentrons_http_api.paths import Paths


def test_paths():
    Paths.IDENTIFY
    Paths.RUNS_RUN_ID
    Paths.RUNS_RUN_ID.format(run_id='123')
