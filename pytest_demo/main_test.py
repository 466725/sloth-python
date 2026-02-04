import pytest
import os

pytest.main()

# Generate allure test report
os.system("allure generate ./temps -o ./temps --clean")