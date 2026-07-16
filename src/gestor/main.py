import logging

from src.gestor.business.bills_service import BillsService

# Configure the logger to show all messages from INFO up
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

def main():
    bills_service = BillsService()
    bills_service.process_bills()


if __name__ == "__main__":
    main()
