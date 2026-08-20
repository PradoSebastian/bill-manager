import logging
import argparse

from src.gestor.business.bills_service import BillsService

# Configure the logger to show all messages from INFO up
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

def main():
    parser = argparse.ArgumentParser(description="Bills Manager")
    parser.add_argument("--month", type=str, default="", help="The month for which to process bills as String, e.g. 'Julio'.")
    args = parser.parse_args()
    bills_service = BillsService(args.month)
    bills_service.process_bills()


if __name__ == "__main__":
    main()
