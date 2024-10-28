import enum


class StrainType(enum.Enum):
    indica = "indica"
    sativa = "sativa"
    indica_dominant = "indica dominant"
    sativa_dominant = "sativa dominant"
    hybrid = "hybrid"


class MeasurementUnit(enum.Enum):
    grams = "Граммы"
    pcs = "Штуки"
