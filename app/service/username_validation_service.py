from datetime import datetime
import re
from app.service.current_reference_data_service import get_current_reference_data_by_reference_data_type_and_code_service

class UsernameValidator:
    def __init__(self, min_length=16, max_length=16):
        self.min_length = min_length
        self.max_length = max_length
        # self.pattern = r"^[a-zA-Z0-9_]+$"
        self.pattern = r"^[0-9]{16}$"

    def validate(self, username, password):
        if len(username) < self.min_length:
            return False, f"Username must be at least {self.min_length} characters long"
        if len(username) > self.max_length:
            return False, f"Username must be no more than {self.max_length} characters long"
        if not re.match(self.pattern, username):
            return False, "Username can only numbers"
        
        # validate if first 6 characters are exist in current reference data table using this service get_current_reference_data_by_reference_data_type_and_code_service, set the code as prefix and set the reference data type as "DISTRICT"
        prefix = username[:6]
        currentReferenceData = get_current_reference_data_by_reference_data_type_and_code_service('DISTRICT', prefix)
        if not currentReferenceData:
            return False, f"Username prefix {prefix} is not valid"

        #validate if characters 6 until 12 compare to today is more than 17 years 0 month 0 day 3275111806870008
        today = datetime.today()
        birth_date = datetime(int(username[11:12]), int(username[9:10]), int(username[7:8]))
        age = today - birth_date
        if age.days > 17 * 365.25 * 24 * 60 * 60:
            return False, "Age must be at least 17 years old"
        
        if password != 'Pajak@123':
            return False, "Password is not matched"

        return True, "Username is valid"