from seeds_shop.core.models.dto.cart import CartLineDTO
from seeds_shop.core.models.dto.order import OrderLineDTO
from seeds_shop.core.models.dto.product import ProductDTO, ProductImageDTO, ProductWithParamsDTO, ProductWithQuantityDTO
from seeds_shop.infrastructure.database.models import Product, ProductImage


def convert_db_model_to_product_image_dto(product_image: ProductImage) -> ProductImageDTO:
    return ProductImageDTO(product_id=product_image.product_id, image_path=product_image.image_path)


def convert_db_model_to_product_dto(product: Product) -> ProductDTO:
    product_images = [convert_db_model_to_product_image_dto(image) for image in product.images]
    return ProductDTO(
        id=product.id,
        title=product.title,
        images=product_images,
        description=product.description,
        measurement=product.measurement,
        category_id=product.category_id,
        price=product.price,
        weight=product.weight,
        strain_name=product.strain_name,
        strain_type=product.strain_type,
        thc=product.thc,
        origin=product.origin,
        pgr=product.pgr,
        vhq=product.vhq,
        cbd=product.cbd,
    )


def convert_db_model_to_product_with_params_dto(product: Product) -> ProductDTO:
    product_images = [convert_db_model_to_product_image_dto(image) for image in product.images]
    return ProductWithParamsDTO(
        id=product.id,
        title=product.title,
        images=product_images,
        description=product.description,
        measurement=product.measurement,
        category_id=product.category_id,
        price=product.price,
        weight=product.weight,
        feelings=product.feelings,
        genetics=product.genetics,
        strain_name=product.strain_name,
        strain_type=product.strain_type,
        thc=product.thc,
        origin=product.origin,
        pgr=product.pgr,
        vhq=product.vhq,
        cbd=product.cbd,
    )


def create_products_with_quantity_dto(lines: list[CartLineDTO | OrderLineDTO], products: list[ProductDTO]):
    return [
        ProductWithQuantityDTO(product=product, quantity=line.quantity)
        for line in lines
        for product in products
        if line.product_id == product.id
    ]
