import logging

from datetime import date, datetime
from typing import Any

from src.gestor.model.bill import Bill
from src.gestor.constant.app_constants import AppConstants

logger = logging.getLogger(__name__)

class BillMapper:
    
    @staticmethod
    def format_date(date_arg):
        """Formats the date string to a standard format (DD/MM/YYYY)."""
        date_result = date_arg
        if isinstance(date_arg, str):
            date_result = date_arg.replace("-", "/")
            date_result = datetime.strptime(date_result, "%d/%m/%Y")
        return date_result
    
    @staticmethod
    def normalize_destiny(destiny: str) -> str:
        """Normalizes the destiny string."""
        return AppConstants.BILL_DESTINY_NORMALIZE_MAP.get(destiny, destiny)
    
    @staticmethod
    def from_json_dict(data):
        return Bill(
            description=data.get(AppConstants.DESCRIPTION_JSON_FIELD, ""),
            type=data.get(AppConstants.TYPE_JSON_FIELD, ""),
            destiny=BillMapper.normalize_destiny(data.get(AppConstants.DESTINY_ACCOUNT_JSON_FIELD, "")),
            amount=round(float(data.get(AppConstants.AMOUNT_JSON_FIELD, 0.0)), 2),
            date=BillMapper.format_date(data.get(AppConstants.DATE_JSON_FIELD, date.today().strftime("%d/%m/%Y"))),
            month=data.get(AppConstants.MONTH_JSON_FIELD, "")
        )
        
    @staticmethod
    def from_list_json_dict(data_list):
        return [BillMapper.from_json_dict(data) for data in data_list]
    
    @staticmethod
    def from_excel_dict(data, destiny, month):
        return Bill(
            description=data.get(AppConstants.DESCRIPTION_EXCEL_FIELD, ""),
            type=data.get(AppConstants.TYPE_EXCEL_FIELD, "") or "",
            destiny=data.get(AppConstants.DESTINY_EXCEL_FIELD, destiny),
            amount=data.get(AppConstants.AMOUNT_EXCEL_FIELD, 0.0),
            date=BillMapper.format_date(data.get(AppConstants.DATE_EXCEL_FIELD, date.today().strftime("%d/%m/%Y"))),
            month=month
        )
        
    @staticmethod
    def from_list_excel_dict(data_list, destiny, month):
        return [BillMapper.from_excel_dict(data, destiny, month) for data in data_list]
    
    @staticmethod
    def to_excel_dict(bill: Bill) -> dict[str, Any]:
        return {
            AppConstants.DESCRIPTION_EXCEL_FIELD: bill.description,
            AppConstants.TYPE_EXCEL_FIELD: bill.type,
            AppConstants.AMOUNT_EXCEL_FIELD: bill.amount,
            AppConstants.DATE_EXCEL_FIELD: bill.date,
            AppConstants.DESTINY_EXCEL_FIELD: bill.destiny
        }
        
    @staticmethod
    def to_excel_list_dict(bills: list[Bill]) -> list[dict[str, Any]]:
        return [BillMapper.to_excel_dict(bill) for bill in bills]