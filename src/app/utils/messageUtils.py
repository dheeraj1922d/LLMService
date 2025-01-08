import re

class messageUtils:

    def isBankSMS(self , message ):
        print(type(message))
        # Regex pattern
        pattern = r'\b(?:credited|debited|withdrawn|balance|NEFT|IMPS|UPI|ATM)\b.*?\b(?:₹|\$|€)?\s?\d+(?:,\d{3})*(?:\.\d{2})?'

        return bool(re.search(pattern, message))