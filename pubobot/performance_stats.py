from dataclasses import dataclass
from typing import Optional
import abc
from functools import lru_cache
import time
import MySQLdb
import os
from contextlib import contextmanager



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
