import re
from unidecode import unidecode
from django.core.exceptions import ValidationError


def validate_mac(val):
    MAC_REG = r'^([0-9a-fA-F]{2}([:-]?|$)){6}$'
    mac_reg = re.compile(MAC_REG)

    if mac_reg.match(val) is None:
        raise ValidationError("MAC address invalid (EUI-48 format, hexadecimal, ':' or '-' separated)")


def format_mac(val):
    return val.upper().replace("-", ":")


def sanitize_string(source):
    # 'Mon bât/iment#n°1' -> 'mon_bat_iment_ndeg1'
    dst = source.lower()
    dst = unidecode(dst)
    dst = dst[0:64]
    dst = re.sub('\W+', '_', dst)

    return dst
