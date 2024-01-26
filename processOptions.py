from dataclasses import dataclass

@dataclass
class processOptions:
    schichtwechsel: bool
    modell_Option: str
    verhältnis_A: int
    verhältnis_B: int
    numberRepitions: int
    travelOutside: bool
    gradienten: bool
    gradientenFlächeFinden: int
    gradientenFlächeZiel: int
    gradientenStartHöhe: int
    gradientenEndHöhe: int
