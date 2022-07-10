from django.forms import ValidationError


def only_letters_and_numbers_validator(value):
    are_alnums = [ch.isalnum() for ch in value]
    if not all(are_alnums) and not " " in value:
        raise ValidationError("Ensure this value contains only letters or numbers.")

def only_letters_validator(value):
    are_alpha = [ch.isalpha() for ch in value]
    if not all(are_alpha):
        raise ValidationError("Ensure this value contains only letters.")

def validate_password(password):
    are_alnums = [ch.isalnum() for ch in password]
    if not all(are_alnums) and " " in password:
        raise ValidationError("Ensure your password consists only of letters and digits.")