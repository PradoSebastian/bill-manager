import logging
from datetime import datetime
from typing import Any

from src.gestor.constant.app_constants import AppConstants
from src.gestor.config.settings import settings
from src.gestor.mapper.bill_mapper import BillMapper
from src.gestor.model.bill import Bill
from src.gestor.util.excel import ExcelUtil
from src.gestor.util.path import PathUtil
from src.gestor.util.words import WordsUtil

logger = logging.getLogger(__name__)

class BillsService:
        
    def _classify_bills(self, bills: list[dict[str, Any]]) -> dict[str, list[Bill]]:
        classified_bills = {
            bill_destiny_account: [] for bill_destiny_account in AppConstants.BILL_DESTINY_ACCOUNT_MAP.keys()
        }
        
        for bill in bills:
            bill_destiny_account = bill.get(AppConstants.DESTINY_ACCOUNT_JSON_FIELD)
            bill_type = bill.get(AppConstants.TYPE_JSON_FIELD)
            for destiny, account in AppConstants.BILL_DESTINY_ACCOUNT_MAP.items():
                if (bill_destiny_account in account and not bill_type == AppConstants.INCOMES_ACCOUNT_NAME) or bill_type in account:
                    classified_bills[destiny].append(BillMapper.from_json_dict(bill))
        
        logger.info(f"Classified bills: {classified_bills}")        
        return classified_bills

    def _get_current_bills(self, bill_destiny: str, current_month: str) -> list[Bill]:
        range = ""
        if bill_destiny == AppConstants.INCOMES_REF and settings.incomes_table_range:
            range = settings.incomes_table_range
        current_bills = ExcelUtil.read_elements_from_table(
            excel_path=settings.excel_path,
            sheet_name=current_month,
            table_name=AppConstants.BILL_TABLE_MAP[bill_destiny] + f"_{current_month}",
            range=range,
            contains_header=bill_destiny != AppConstants.INCOMES_REF,  # Assuming income table does not have headers
            headers=AppConstants.INCOMES_HEADERS if bill_destiny == AppConstants.INCOMES_REF else []
        )
        current_bills = [
            b for b in current_bills 
            if b.get(settings.flag_header) 
            and not str(b.get(settings.flag_header)).startswith(AppConstants.MATH_EXPRESSION_CHARACTER)
        ]  # Filter out bills that are already present
        logger.info(f"Current bills in {bill_destiny} table: {current_bills}")
        return BillMapper.from_list_excel_dict(current_bills, bill_destiny, current_month)
    
    def _write_new_bills_to_excel_by_bill_destiny(
        self,
        bill_destiny: str,
        new_bills: list[Bill],
        current_month: str,
        init_row: int
    ) -> None:
        logger.info(f"Destiny Account saving {bill_destiny}")
        range = ""
        headers = []
        if bill_destiny == AppConstants.INCOMES_REF and settings.incomes_table_range:
            range = settings.incomes_table_range
            headers = AppConstants.INCOMES_HEADERS
            mensual_income_bills = [
                bill for bill in new_bills 
                if AppConstants.MENSUAL_INCOME_KEY_WORD in WordsUtil.remove_accents(bill.description)
            ]
            logger.info(f"Identified Bills with key word {AppConstants.MENSUAL_INCOME_KEY_WORD}: {mensual_income_bills}, init row: {init_row}")
                
            for idx, bill in enumerate(mensual_income_bills, start=1):
                new_bills.remove(bill)
                bill.description = AppConstants.MENSUAL_INCOME_COMPLETE_DESCRIPTION.format(
                    AppConstants.NUMBER_STR_CORRELATION.get(idx, ""))
            if mensual_income_bills:
                income_init_row = 0
                self._write_bills_to_excel(bill_destiny, mensual_income_bills, current_month, income_init_row, range, headers)
            init_row = init_row + 2
        
        if new_bills:
            self._write_bills_to_excel(bill_destiny, new_bills, current_month, init_row, range, headers)
        
    def _write_bills_to_excel(
        self,
        bill_destiny: str,
        bills: list[Bill],
        current_month: str,
        init_row: int,
        range: str = "",
        headers: list[str] = []
    ):
        logger.info(f"Bills to be created: {bills}")
        row_data_list = BillMapper.to_excel_list_dict(bills)
        ExcelUtil.add_row_elements_to_table(
            excel_path=settings.excel_path,
            sheet_name=current_month,
            table_name=AppConstants.BILL_TABLE_MAP[bill_destiny] + f"_{current_month}",
            row_data_list=row_data_list,
            range=range,
            coordinates=(init_row, 0),  # Assuming we start adding from the first column
            headers=headers,
            banned_headers=settings.banned_headers
        )
        logger.info(f"Added {len(bills)} bills to the {bill_destiny} table for {current_month}.")
  
    def _filter_new_bills(self, new_bills: list[Bill], current_bills: list[Bill]) -> list[Bill]:
        filtered_bills = []
        for new_bill in new_bills:
            if not any(new_bill.equals_by_amount_and_date(current_bill) for current_bill in current_bills):
                filtered_bills.append(new_bill)
        return filtered_bills        
    
    def process_bills(self):
        current_month = AppConstants.MONTHS_EQUIVALENCE.get(str(datetime.now().month), None)
        if not current_month:
            logger.error("Current month not found in MONTHS_EQUIVALENCE.")
            return
        logger.info(f"Processing bills for the month of {current_month}...")
        
        json_content=PathUtil.read_json_files_from_folder(settings.json_files_path + f"/{current_month}")
        classified_bills = self._classify_bills(json_content)
        logger.debug(f"Classified bills: {classified_bills}")
        
        for bill_destiny, bills in classified_bills.items():
            if bills:
                bills = sorted(bills, key=lambda b: (b.date))  # Sort bills by date ASC
                current_bills = self._get_current_bills(bill_destiny, current_month)
                logger.info(f"Checking bills for {bill_destiny}: {bills}")
                new_bills = self._filter_new_bills(bills, current_bills)
                if not new_bills:
                    logger.info(f"No new bills to add for the {bill_destiny} table.")
                    continue
                init_row = len(current_bills)
                if bill_destiny != AppConstants.INCOMES_REF:
                    init_row += 1  # Adjust for header row if not incomes table
                self._write_new_bills_to_excel_by_bill_destiny(bill_destiny, new_bills, current_month, init_row)
            else:
                logger.info(f"No bills to add for the {bill_destiny} table.")