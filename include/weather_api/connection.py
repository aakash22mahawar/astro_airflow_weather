import snowflake.connector
import configparser
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from logging_config import setup_logger

# Initialize the logger
logger = setup_logger()

# Add your custom module path to sys.path
config_file_path = '/usr/local/airflow/include/weather_api/config.ini'  # Update if different since it is inside docker container 


# Function to establish and return the Snowflake connection using private key authentication
def get_snowflake_connection():
    # Load the configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    try:
        # Read Snowflake credentials from the config file
        SNOWFLAKE_USER = config['Snowflake']['user']
        SNOWFLAKE_ACCOUNT = config['Snowflake']['account']
        SNOWFLAKE_WAREHOUSE = config['Snowflake']['warehouse']
        SNOWFLAKE_DATABASE = config['Snowflake']['database']
        SNOWFLAKE_SCHEMA = config['Snowflake']['schema']
        SNOWFLAKE_AUTOCOMMIT = config.getboolean('Snowflake', 'autocommit')
        ROLE = config['Snowflake']['role']
        PRIVATE_KEY_PATH = config['Snowflake']['private_key_path']  # Path to your private key file

        # Load the private key from the PEM file
        with open(PRIVATE_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,  # Provide the password if your PEM file is encrypted
                backend=default_backend()
            )

        # Convert the private key to the required format (PKCS8 DER format)
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Establish and return the Snowflake connection
        connection = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            autocommit=SNOWFLAKE_AUTOCOMMIT,
            role=ROLE,
            private_key=private_key_bytes  # Using private key authentication
        )

        logger.info("Snowflake connection established successfully!")
        return connection

    except Exception as e:
        logger.error(f"Snowflake connection failed: {e}")
        raise


# Test the connection
#if __name__ == "__main__":
   # conn = get_snowflake_connection()
    #if conn:
       # cursor = conn.cursor()
        #cursor.execute("SELECT CURRENT_VERSION()")
        #print("Snowflake Version:", cursor.fetchone()[0])
