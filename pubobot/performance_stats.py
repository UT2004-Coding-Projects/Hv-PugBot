from dataclasses import dataclass
from typing import Optional
import abc

from . import config


stat_provider = None


@dataclass
class Player:
    name: str
    discord_id: Optional[str] = None
    gamer_id: Optional[str] = None


@dataclass
class PlayerStat:
    player: Player
    stat_type: str
    stat_value: float


class AbstractPlayerStatProvider(abc.ABC):
    @abc.abstractmethod
    def get_player(self, discord_id: str) -> Optional[Player]:
        """Get player stats by discord ID"""
        pass


class NullStatProvider(AbstractPlayerStatProvider):
    """Implementation that does nothing - used when stats are disabled"""
    def get_player(self, discord_id: str) -> Optional[Player]:
        return None


def init():
    global stat_provider
    stat_provider = NullStatProvider()

    if config.cfg.PERFORMANCE_STAT_PROVIDER == "UT2K4StatsDBStatProvider":
        from .providers.ut2k4_statsdb_provider import UT2K4StatsDBStatProvider
        stat_provider = UT2K4StatsDBStatProvider()
