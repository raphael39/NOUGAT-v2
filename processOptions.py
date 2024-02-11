from dataclasses import dataclass

@dataclass
class ProcessOptions:
    schichtwechsel: bool
    modell_Option: str
    verhältnis_A: int
    verhältnis_B: int
    numberRepitions: int
    travelOutside: bool
    gradienten: bool
    gradientGrundflächeLayer: int
    gradientStartHöhe: int
    gradientenLineStartHöhe: int
    gradientenLineEndHöhe: int
    gradientenFlowRate: int
    gradientenFlowRateFactor: int
    gradientenLayers: int