import typing
from Options import Choice, Toggle, PerGameCommonOptions
from dataclasses import dataclass

class Dummy_Option(Toggle):
    """A dummy option for testing purposes."""
    display_name = "Dummy Option"
    description = "This is a dummy option used for testing purposes."

@dataclass
class FFVWOptions(PerGameCommonOptions):
    DummyOption = Dummy_Option