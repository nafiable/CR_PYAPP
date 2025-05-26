# constante/const2.py

import logging

logger = logging.getLogger(__name__)
# 1. Database Configuration Constants
# These constants will be populated by extracting key-value pairs
# from a 'config' table in the database at application startup.
# Placeholder comments for database extraction logic:

from database.connexionsqlLiter import get_database_config

# Initial placeholder values (will be overwritten by database config)
try:
 db_config = get_database_config()
 DB_SETTING_EXAMPLE = db_config.get('example_setting', 'default_value')
 # Add other constants derived from db_config here
except Exception as e:  # Gérer les autres exceptions potentielles
 logger.error(f"Could not load database configuration: {e}")
 db_config = {} # Use an empty dict if loading fails
 DB_SETTING_EXAMPLE = 'default_value' # Use a default if loading fails
 # Assign default values to other constants here if needed

# 2. SQL Table Column Name Constants
# These constants define the names of columns in SQL tables.
# They are hardcoded.
ID_COLUMN = 'id'
COLUMN_NAME = "name"
COLUMN_CODE = "code"
COLUMN_DESCRIPTION = "description"
COLUMN_CREATED_AT = "created_at"
COLUMN_UPDATED_AT = "updated_at"
COLUMN_IS_ACTIVE = "is_active"
COLUMN_VALUE = "value"
COLUMN_DATE = "date"
COLUMN_AMOUNT = "amount"
COLUMN_CURRENCY = "currency"

# Example specific table columns
TABLE_FONDS_COL_ISIN = "isin"
TABLE_FONDS_COL_NOM = "nom"
TABLE_TITRE_COL_ISIN = "isin"
TABLE_TITRE_COL_NOM = "nom"


# 3. Other Hardcoded Constants
# Other hardcoded variables accessible throughout the project.
DEFAULT_LIMIT = 100
DEFAULT_LANGUAGE = "en"
DEFAULT_TIMEZONE = "UTC"
API_TIMEOUT_SECONDS = 30
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 5
LOG_FILE_PATH = "application.log"
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
APP_VERSION = '1.0'