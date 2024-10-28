from dataclasses import dataclass
from decimal import Decimal

from seeds_shop.core.models.enums.product import MeasurementUnit, StrainType
from seeds_shop.infrastructure.database.models import Feeling, Genetics


@dataclass(frozen=True)
class ProductImageDTO:
    product_id: int
    image_path: str


@dataclass
class ProductDTO:
    id: int
    category_id: int
    price: Decimal
    title: str
    description: str
    images: list[ProductImageDTO] | None = None
    measurement: MeasurementUnit = MeasurementUnit.grams
    weight: float | None = None
    strain_name: str | None = None
    strain_type: StrainType | None = None
    thc: int | None = None
    origin: str | None = None
    pgr: bool | None = None
    vhq: bool | None = None
    cbd: str | None = None
    available_quantity: int | None = None


@dataclass
class ProductWithParamsDTO(ProductDTO):
    feelings: list[Feeling] | None = None
    genetics: list[Genetics] | None = None


@dataclass(frozen=True)
class ProductWithQuantityDTO:
    product: ProductDTO
    quantity: int
