from .Job import Job, monster_families
from .SpriteSet import SpriteSet
from ..patchersuite.ENTD.Unit import UnitGender


class SourceUnit:
    sprite_set: SpriteSet
    job: Job
    gender: UnitGender
    immortal: bool = False

    def __init__(self, sprite_set: SpriteSet, job: Job, gender: UnitGender, immortal: bool = False):
        self.sprite_set = sprite_set
        self.job = job
        self.gender = gender
        self.immortal = immortal

    def to_json(self):
        return {
            "SpriteSet": self.sprite_set.value,
            "Job": self.job.value,
            "Gender": self.gender.value
        }

    def __repr__(self):
        return f"Sprite: {self.sprite_set.name}, Job: {self.job.name}, Gender: {self.gender.name}"

    def __eq__(self, other):
        if self.sprite_set != other.sprite_set:
            return False
        if self.job != other.job:
            if self.job in monster_families.keys():
                if other.job not in monster_families[self.job]:
                    return False
            else:
                return False
        if self.gender != other.gender:
            return False
        return True

    def __hash__(self):
        job = self.job.value
        if self.job in monster_families.keys():
            job = monster_families[self.job][0]
        return hash((self.sprite_set.value, job, self.gender.value))

    def __lt__(self, other):
        if self.job.value == other.job.value:
            return self.gender.value < other.gender.value
        return self.job.value < other.job.value

    def __gt__(self, other):
        if self.job.value == other.job.value:
            return self.gender.value > other.gender.value
        return self.job.value > other.job.value