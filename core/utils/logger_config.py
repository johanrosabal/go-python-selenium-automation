import logging
import os

# Global variable to store the shared file handler to avoid overwriting and duplicates
_shared_file_handler = None

def setup_logger(name):
    """
    Configures and returns a logger instance mimicking Log4j behavior.
    Uses a shared file handler to ensure all logs go to the same file without 
    overwriting each other during the same execution.
    """
    global _shared_file_handler
    
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, don't add more
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG)

    # Create 'logs' directory if it doesn't already exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Define log format: [TIMESTAMP] [LEVEL] [LOGGER] - MESSAGE
    log_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')

    # Configure Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # Configure Shared File Handler: Opened in 'w' mode only once per process
    if _shared_file_handler is None:
        file_name = "logs/automation.log"
        _shared_file_handler = logging.FileHandler(file_name, mode='w')
        _shared_file_handler.setFormatter(log_format)

    logger.addHandler(_shared_file_handler)

    return logger
