from __future__ import annotations
from typing import Dict, List, Tuple, BinaryIO, Optional, Sequence
from dataclasses import dataclass
from abc import ABC

from opentrons_http_api.api import API, SettingId, ActionType


class _Info(ABC):
    """
    Base info class.
    """
    def __init__(self, args, kwargs):
        pass

    @classmethod
    def from_dict(cls, d: dict) -> _Info:
        return cls(**d)


@dataclass(frozen=True)
class SettingInfo(_Info):
    id: str
    old_id: str
    title: str
    description: str
    restart_required: bool
    value: bool


@dataclass(frozen=True)
class HealthInfo(_Info):
    name: str
    robot_model: str
    api_version: str
    fw_version: str
    board_revision: str
    logs: List[str]
    system_version: str
    maximum_protocol_api_version: List[int]
    minimum_protocol_api_version: List[int]
    robot_serial: str
    links: Dict[str, str]


@dataclass(frozen=True)
class RunInfo(_Info):
    id: str
    createdAt: str
    status: str
    current: bool
    actions: List[dict]
    errors: List[dict]
    pipettes: List[dict]
    modules: List[dict]
    labware: List[dict]
    liquids: List[dict]
    labwareOffsets: List[dict]
    protocolId: str


@dataclass(frozen=True)
class ProtocolInfo(_Info):
    id: str
    createdAt: str
    files: List[Dict]
    protocolType: str
    robotType: str
    metadata: Dict
    analyses: List
    analysisSummaries: List[Dict]
