import re
from django.core.exceptions import ValidationError

def validar_email(email):
    """
    Valida se o endereço de e-mail fornecido está no formato correto.

    Args:
        email (str): O endereço de e-mail a ser validado.

    Returns:
        str: O endereço de e-mail validado se estiver no formato correto.

    Raises:
        ValidationError: Se o endereço de e-mail não estiver no formato correto.
    """
    email_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    if not email_pattern.match(email):
        raise ValidationError('Insira um endereço de e-mail válido.')
    return email