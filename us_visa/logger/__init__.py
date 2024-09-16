import logging
import os

from from_root import from_root  # Imports 'from_root' to get the root directory
from datetime import datetime  # Imports datetime to generate timestamped log file names

# Create a log file name with the current date and time (formatted as month_day_year_hour_minute_second)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir = 'logs'  # Directory where log files will be stored

# Generate the full path to the log file, combining the root directory, the logs folder, and the log file name
logs_path = os.path.join(from_root(), log_dir, LOG_FILE)

# Create the directory if it doesn't exist, ensuring no error is raised if it already exists
os.makedirs(log_dir, exist_ok=True)

# Set up logging configuration
logging.basicConfig(
    filename=logs_path,  # The log file path where logs will be written
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",  # Format of each log entry
    level=logging.DEBUG,  # The minimum log level (DEBUG here) to capture all log messages (DEBUG and above)
)
