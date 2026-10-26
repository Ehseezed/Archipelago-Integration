from .FactoryKey import FactoryKey
from .SourceUnit import SourceUnit
from .SpriteSet import SpriteSet
from .Job import Job
from ..patchersuite.ENTD.Unit import UnitGender


class RandomizedMapping:
    source_unit: SourceUnit
    destination_unit: FactoryKey | Job | None
    battle_level: int = 0
    boss_unit: bool = False

    def __init__(self, source_unit: SourceUnit = None, destination_unit: FactoryKey | Job = None):
        self.source_unit = source_unit
        self.destination_unit = destination_unit

    def to_json(self):
        return {
            "SourceUnit": self.source_unit.to_json(),
            "DestinationUnit": self.destination_unit,
            "BattleLevel": self.battle_level,
            "BossUnit": int(self.boss_unit)
        }

    @classmethod
    def from_json(cls, json_data) -> "RandomizedMapping":
        source_unit = SourceUnit(
            SpriteSet(json_data["SourceUnit"]["SpriteSet"]),
            Job(json_data["SourceUnit"]["Job"]),
            UnitGender(json_data["SourceUnit"]["Gender"])
        )
        try:
            new_mapping = RandomizedMapping(source_unit, FactoryKey(json_data["DestinationUnit"]))
        except ValueError:
            new_mapping = RandomizedMapping(source_unit, Job(json_data["DestinationUnit"]))
        new_mapping.battle_level = json_data["BattleLevel"]
        new_mapping.boss_unit = bool(json_data["BossUnit"])
        return new_mapping

    def __repr__(self):
        try:
            return f"{self.source_unit} -- {FactoryKey(self.destination_unit).name}"
        except:
            return f"{self.source_unit} -- {Job(self.destination_unit).name}"