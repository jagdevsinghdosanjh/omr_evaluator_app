import re

# Validate email format
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# Validate mobile number (India-specific)
def is_valid_mobile(mobile):
    pattern = r"^[6-9]\d{9}$"
    return re.match(pattern, mobile) is not None

# Validate password strength
def is_valid_password(password):
    return len(password) >= 6

# Validate OTP format
def is_valid_otp(otp):
    return otp.isdigit() and len(otp) == 6

# Validate name (basic)
def is_valid_name(name):
    return len(name.strip()) >= 2 and all(x.isalpha() or x.isspace() for x in name)

# Validate role
def is_valid_role(role):
    return role in ["Student", "Evaluator", "Admin"]
