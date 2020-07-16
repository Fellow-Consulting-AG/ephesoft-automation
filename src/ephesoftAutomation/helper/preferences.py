from ephesoftAutomation.helper import constants as const

KEY_FIELD = const.Fields.KEY_IDENTIFIER

CSV_DELIMITER = ';'

CURRENCY_FIELDS = [const.Fields.TAX_RATE,
                   const.Fields.TAX_AMOUNT,
                   const.Fields.NET_AMOUNT,
                   const.Fields.TOTAL_AMOUNT]

DATE_FIELDS = [const.Fields.INVOICE_DATE,
               const.Fields.DELIVERY_DATE]

MULTI_OPTION_FIELDS = [const.Fields.IBAN_EXTRACTED]

FIELDS_TO_CLEAN_BEFORE_COMPARISON = [const.Fields.TAX_RATE,
                                     const.Fields.TAX_AMOUNT,
                                     const.Fields.NET_AMOUNT,
                                     const.Fields.TOTAL_AMOUNT,
                                     "KOSTENSTELLE"]

FIELDS_TO_ADV_CLEAN_BEFORE_COMPARISON = [const.Fields.PAYMENT_TERMS,
                                         const.Fields.VAT_NO,
                                         const.Fields.IBAN_EXTRACTED]

ORIGINAL_CURRENCY_FIELDS_NON_US_FORMAT = ['TAX_RATE', 'TAX_AMOUNT', "NET_AMOUNT", "TOTAL_AMOUNT"]
EXTRACTED_CURRENCY_FIELDS_NON_US_FORMAT = ['TAX_RATE']

ORIGINAL_VAL_DATE_FORMATS = ['%d.%m.%Y', '%d.%m.%y']
EXTRACTED_VAL_DATE_FORMAT = '%d/%m/%Y'
