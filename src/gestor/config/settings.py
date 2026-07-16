from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    json_files_path: str = Field(default="resources/input", description="The path to the files directory.")
    excel_path: str = Field(default="resources/input/excel.xlsx", description="The path to the Excel file.")
    
    debit_table_name: str = Field(default="DebitTable", description="The name of the debit table in the Excel file.")
    credit_table_name: str = Field(default="CreditsTable", description="The name of the credits table in the Excel file.")
    credit_usd_table_name: str = Field(default="CreditsUSDTable", description="The name of the credits (USD) table in the Excel file.")
    
    debit_table_range: str | None = Field(default=None, description="The range of the debit table in the Excel file.")
    incomes_table_range: str | None = Field(default=None, description="The range of the incomes table in the Excel file.")
    credit_table_range: str | None = Field(default=None, description="The range of the credits table in the Excel file.")
    credit_usd_table_range: str | None = Field(default=None, description="The range of the credits (USD) table in the Excel file.")

    banned_headers: list[str] = Field(default=[], description="List of headers that should not be included in the output.")
    flag_header: str = Field(default="ID", description="The header used to identify flagged bills.")
    
    # In Pydantic v2+, use SettingsConfigDict to specify .env files
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()
