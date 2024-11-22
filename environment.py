import subprocess
import sys

# Function to install packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_package("nicegui")
install_package("werkzeug")
install_package('pandas')
install_package('flask')