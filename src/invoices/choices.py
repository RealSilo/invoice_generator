UPON_RECEIPT = 'UR'
NET30 = 'N3'
NET60 = 'N6'
FLAT = '$'
PERCENT = '%'
PAYMENT_TERMS_CHOICES = (
    (UPON_RECEIPT, 'Upon Receipt'),
    (NET30, 'NET30'),
    (NET60, 'NET60'),
)
DISCOUNT_TYPE_CHOICES = (
    (FLAT, '$'),
    (PERCENT, '%'),
)
TAX_TYPE_CHOICES = (
    (FLAT, '$'),
    (PERCENT, '%'),
)
