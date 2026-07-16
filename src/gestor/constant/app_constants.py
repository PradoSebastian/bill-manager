from src.gestor.config.settings import settings

class AppConstants:
    """Class to hold application constants."""
    
    DEBIT_REF: str = "debit"
    INCOMES_REF: str = "incomes"
    CREDIT_REF: str = "credit"
    CREDIT_USD_REF: str = "credit_usd"
    
    MENSUAL_INCOME_KEY_WORD: str = "Nomina"
    MENSUAL_INCOME_COMPLETE_DESCRIPTION: str = "Ingreso Nomina {}"
    
    NUMBER_STR_CORRELATION = {
        1: "1er",
        2: "2do"
    }
    
    MATH_EXPRESSION_CHARACTER = "="
    
    # Constants for Account Names
    DEBIT_ACCOUNT_NAME: str = "Ahorros"
    INCOMES_ACCOUNT_NAME: str = "Ingreso"
    CREDIT_ACCOUNT_NAME: str = "Credito Mastercard"
    CREDIT_USD_ACCOUNT_NAME: str = "Credito Mastercard USD"
    CREDIT_NU_ACCOUNT_NAME: str = "Credito Nu"
    
    # Constants for JSON field names
    TYPE_JSON_FIELD: str = "tipo"
    DESTINY_ACCOUNT_JSON_FIELD: str = "cuenta_destino"
    AMOUNT_JSON_FIELD: str = "valor"
    DATE_JSON_FIELD: str = "fecha"
    DESCRIPTION_JSON_FIELD: str = "razon"
    MONTH_JSON_FIELD: str = "mes"
    
    # Constants for Excel field names
    TYPE_EXCEL_FIELD: str = "Tipo"
    AMOUNT_EXCEL_FIELD: str = "Monto"
    DATE_EXCEL_FIELD: str = "Fecha"
    DESCRIPTION_EXCEL_FIELD: str = "Motivo"
    DESTINY_EXCEL_FIELD: str = "Tarjeta"
    
    BILL_DESTINY_ACCOUNT_MAP = {
        DEBIT_REF: [DEBIT_ACCOUNT_NAME],
        INCOMES_REF: [INCOMES_ACCOUNT_NAME],
        CREDIT_REF: [CREDIT_ACCOUNT_NAME, CREDIT_NU_ACCOUNT_NAME],
        CREDIT_USD_REF: [CREDIT_USD_ACCOUNT_NAME]
    }
       
    BILL_TABLE_MAP = {
        DEBIT_REF: settings.debit_table_name,
        INCOMES_REF: settings.debit_table_name,
        CREDIT_REF: settings.credit_table_name,
        CREDIT_USD_REF: settings.credit_usd_table_name
    }
    
    BILL_DESTINY_NORMALIZE_MAP = {
        CREDIT_ACCOUNT_NAME: "Mastercard Black",
        CREDIT_USD_ACCOUNT_NAME: "Mastercard Black",
        CREDIT_NU_ACCOUNT_NAME: "Nu Credito"
    }
    
    MONTHS_EQUIVALENCE = {
        "1": "Enero",
        "2": "Febrero",
        "3": "Marzo",
        "4": "Abril",
        "5": "Mayo",
        "6": "Junio",
        "7": "Julio",
        "8": "Agosto",
        "9": "Septiembre",
        "10": "Octubre",
        "11": "Noviembre",
        "12": "Diciembre"
    }
    
    INCOMES_HEADERS = [DESCRIPTION_EXCEL_FIELD, DATE_EXCEL_FIELD, AMOUNT_EXCEL_FIELD]