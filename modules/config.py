import dotenv
import os

dotenv.load_dotenv("config.env")

class config:
    def __init__(self):
        """
        Load the information from the config file."""

        self.host = os.getenv("host")
        self.port = os.getenv("port")

        self.database_path = os.getenv("database")

        self.admin = [os.getenv("administrator_username"), os.getenv("administrator_password")]

        self.maxZooBookings = os.getenv("max_zoo_slot_customers")