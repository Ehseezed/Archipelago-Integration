from .Job import Job
from ..data.logic.Monsters import MonsterNames


class RandomizedPoachBattleSource:
    battle_level: int
    fight_id: int
    destination_job: Job
    monster_name: MonsterNames

    def __init__(self, battle_level: int, fight_id: int, destination_job: Job, monster_name: MonsterNames):
        self.battle_level = battle_level
        self.fight_id = fight_id
        self.destination_job = destination_job
        self.monster_name = monster_name

    def __eq__(self, other):
        return (self.battle_level == other.battle_level
                and self.destination_job == other.destination_job
                and self.monster_name == other.monster_name)

    def __hash__(self):
        return hash((self.battle_level, self.destination_job.value, self.monster_name.value))

    def __repr__(self):
        return f"{self.monster_name.value} -- {self.battle_level}"