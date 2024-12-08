from contextlib import contextmanager
import time
import MySQLdb
import os
from pubobot.performance_stats import AbstractPlayerStatProvider, Player, PlayerStat
from threading import Thread


@contextmanager
def StatsDBConnection():
    connection = MySQLdb.connect(
        host=os.getenv("PLAYER_STATS_DB_HOST"),
        user=os.getenv("PLAYER_STATS_DB_USERNAME"),
        passwd=os.getenv("PLAYER_STATS_DB_PASSWORD"),
        db="utstatsdb",
    )
    cursor = connection.cursor()
    yield cursor
    connection.commit()


class UT2K4StatsDBStatProvider(AbstractPlayerStatProvider):

    def __init__(self, ttl=600):
        self._player_stats = {}
        self.ttl = 600
        self._last_refresh = 0
        self._is_currently_refreshing = False

    def add_player(self, player: Player):
        with StatsDBConnection() as cursor:
            cursor.execute(
                """
                INSERT INTO UFC.UT_PLAYERS (NAME, DISCORD_ID, UT_2K4_ID)
                VALUES (%s, %s, %s)
                """,
                [player.name, player.discord_id, player.ut_2k4_id],
            )

    @property
    def player_stats(self) -> dict:
        current_time = time.time()

        if self._player_stats:
            if current_time - self._last_refresh > self.ttl:
                self._trigger_background_refresh()
            return self._player_stats

        return self._refresh_stats()

    def _trigger_background_refresh(self):
        self.is_refreshing = True
        thread = Thread(target=self._refresh_stats)
        thread.daemon = True
        thread.start()

    def _refresh_stats(self) -> dict:
        try:
            stats = self._load_player_stats()
            self._player_stats = {p_stat.player.discord_id: p_stat for p_stat in stats}
            self._last_refresh = time.time()
            return self._player_stats
        finally:
            self._is_refreshing = False

    def get_player(self, discord_id: str) -> Player:
        return self.player_stats.get(str(discord_id))

    def _load_player_stats(self) -> dict:
        try:
            with StatsDBConnection() as cursor:
                cursor.execute(
                    """
                    WITH player_match_history as (
                    SELECT
                        p.pnum,
                        p.plr_key,
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
                        AND (m.gm_tscore0 >= 10 or m.gm_tscore1 >= 10)
                        AND m.gm_start >= DATE_SUB(NOW(), INTERVAL 60 DAY)
                    )

                    SELECT
                    ut_players.name,
                    ut_players.DISCORD_ID,
                    player_match_history.plr_key as player_guid,
                    SUM(Score) / SUM(Rounds) as PPR,
                    COUNT(*) as MatchCount
                    FROM player_match_history
                    JOIN ufc.ut_players
                        on player_match_history.plr_key = ut_players.UT_2K4_ID
                    WHERE
                        Rounds > 0
                        AND Score > 0
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
                        gamer_id=result[2],
                    )

                    player_stats.append(PlayerStat(player=plr, stat_type='ppr', stat_value=float(result[3])))

                return player_stats
        except Exception as e:
            print("Exception loading player stats. %s", e)
            return []
