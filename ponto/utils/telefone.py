import re
from django.core.exceptions import ValidationError

def validar_telefone(telefone):
    """
    Valida se o telefone está em um dos formatos permitidos:
    - (xx) xxxx-xxxx
    - (xx) xxxxx-xxxx
    - xxxx xxx xxxx
    """
    phone_pattern = re.compile(r'^(\(\d{2}\) \d{4,5}-\d{4})|(\d{4} \d{3} \d{4})$')
    if not phone_pattern.match(telefone):
        raise ValidationError('O número de telefone deve estar no formato (xx) xxxxx-xxxx, (xx) xxxx-xxxx ou xxxx xxx xxxx.')
