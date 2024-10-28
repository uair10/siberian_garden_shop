from seeds_shop.core.models.dto.payment_details import PaymentDetailsDTO
from seeds_shop.infrastructure.database.models import PaymentDetails


def convert_db_model_to_payment_details_dto(
    payment_details: PaymentDetails,
) -> PaymentDetailsDTO:
    return PaymentDetailsDTO(
        id=payment_details.id,
        currency=payment_details.currency,
        currency_symbol=payment_details.currency_symbol,
        payment_address=payment_details.payment_address,
        exchange_percent=payment_details.exchange_percent,
        payment_image_path=payment_details.payment_image_path,
    )
