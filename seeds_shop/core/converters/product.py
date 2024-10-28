from seeds_shop.core.models.dto.cart import CartLineDTO
from seeds_shop.core.models.dto.order import OrderLineDTO
from seeds_shop.core.models.dto.product import ProductDTO, ProductWithQuantityDTO


def convert_products_to_products_with_quantity(
    lines: list[OrderLineDTO | CartLineDTO],
    products: list[ProductDTO],
) -> list[ProductWithQuantityDTO]:
    return [
        ProductWithQuantityDTO(product=product, quantity=item.quantity)
        for item in lines
        for product in products
        if item.product_id == product.id
    ]
