import nltk
import ssl
import os

# Get the path to the .venv directory in your project
venv_path = os.path.join(os.getcwd(), '.venv')

# Create the path to the nltk_data directory inside .venv
nltk_data_path = os.path.join(venv_path, 'nltk_data')

# Check if the nltk_data directory already exists
if not os.path.exists(nltk_data_path):
    # Create the nltk_data directory
    os.makedirs(nltk_data_path)
    print("nltk_data folder created successfully.")
else:
    print("nltk_data folder already exists.")

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()

# A pop up window will appear and paste the path to your /.venv/nltk_data and download all 