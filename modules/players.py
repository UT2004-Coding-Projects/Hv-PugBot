from dataclasses import dataclass
from typing import Optional
import abc
from functools import lru_cache
import time
import MySQLdb
import os


@dataclass
class Player:
    name: str
    discord_id: Optional[str] = None
    ut_2k4_id: Optional[str] = None


@dataclass
class PlayerStat:
    player: Player
    stat_type: str
    stat_value: float


def get_ttl_hash(seconds=600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


class AbstractPlayerStatsRetriever(abc.ABC):

    @abc.abstractmethod
    def get_player(discord_id: str) -> Player:
        raise NotImplementedError


class KokueiUFCStatsRetriever(AbstractPlayerStatsRetriever):

    def __init__(self):
        self._player_stats = {}
        self._connection = None

    @property
    def connection(self):
        if not self._connection:
            self._connection = MySQLdb.connect(
                host=os.getenv("PLAYER_STATS_DB_HOST"),
                user=os.getenv("PLAYER_STATS_DB_USERNAME"),
                passwd=os.getenv("PLAYER_STATS_DB_PASSWORD"),
                db="utstatsdb",
            )
        return self._connection

    def add_player(self, player: Player):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO UFC.UT_PLAYERS (NAME, DISCORD_ID, UT_2K4_ID)
            VALUES (%s, %s, %s)
            """,
            [player.name, player.discord_id, player.ut_2k4_id],
        )
        cursor.close()

    @property
    def player_stats(self):
        stats = self._load_player_stats(ttl_hash=get_ttl_hash())
        for p_stat in stats:
            self._player_stats[p_stat.player.discord_id] = p_stat

        return self._player_stats

    def get_player(self, discord_id: str):
        return self.player_stats.get(str(discord_id))

    @lru_cache()
    def _load_player_stats(self, ttl_hash=None):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            WITH player_match_history as (
            SELECT
                p.pnum,
                p.plr_key,
                p.plr_name,
                IF(gp.gp_team = 0, gp.gp_tscore0, gp.gp_tscore1) as Score,
                m.gm_tscore0 + m.gm_tscore1 AS Rounds,
                m.gm_numplayers as PlayerCount,
                t.tp_num as GameModeID
            FROM
                utstatsdb.ut_players p
                JOIN utstatsdb.ut_gplayers gp ON gp.gp_pnum = p.pnum
                JOIN utstatsdb.ut_matches m ON m.gm_num = gp.gp_match
                JOIN utstatsdb.ut_type t ON t.tp_num = m.gm_type
            WHERE
                t.tp_desc = 'TeamArenaMaster'
                AND m.gm_numplayers >= 8
                AND m.gm_tscore0 + m.gm_tscore1 >= 10
                    AND IF(gp.gp_team = 0, gp.gp_tscore0, gp.gp_tscore1) > 0
                AND m.gm_start BETWEEN FROM_UNIXTIME(1714521600) AND FROM_UNIXTIME(1718849956)
            )

            SELECT
            player_match_history.plr_name as name,
            ut_players.DISCORD_ID,
            player_match_history.plr_key as player_guid,
            SUM(Score) / SUM(Rounds) as PPR,
            COUNT(*) as MatchCount
            FROM player_match_history
            JOIN ufc.ut_players
                on player_match_history.plr_key = ut_players.UT_2K4_ID
            GROUP by 1, 2
            HAVING
            MatchCount > '0';
            """
        )

        results = cursor.fetchall()
        player_stats = []
        for result in results:
            plr = Player(
                name=result[0],
                discord_id=result[1],
                ut_2k4_id=result[2],
            )

            player_stats.append(PlayerStat(player=plr, stat_type='ppr', stat_value=float(result[3])))
        return player_stats
