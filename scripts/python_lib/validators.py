import re

def non_empty(value):
    if not value:
        raise ValueError("La valeur ne peut pas être vide.")
    return value

def as_int(value):
    try:
        return int(value)
    except ValueError:
        raise ValueError("La valeur doit être un entier.")

def fqdn_or_localhost(value):
    if value == "localhost":
        return value
    # Validation d'un FQDN (Fully Qualified Domain Name)
    pattern = r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
    if not re.match(pattern, value):
        raise ValueError("La valeur doit être un FQDN valide ou 'localhost'.")
    return value

def no_scheme (value):
    pattern = r"^[a-zA-Z]+://"
    if re.match(pattern, value):
        raise ValueError("La valeur ne doit pas contenir de schéma (http:// ou https://).")
    return value

def nginx_size(value):
    pattern = r"^\d+[mM]?$"
    if not re.match(pattern, value, re.IGNORECASE):
        raise ValueError("La valeur doit être un nombre suivi d'une unité optionnelle (M m).")
    return value

def filename_safe(value):
    pattern = r"^[a-zA-Z0-9._-]+$"
    if not re.match(pattern, value):
        raise ValueError("La valeur doit être un nom de fichier valide (caractères alphanumériques, points, tirets et underscores uniquement).")
    return value

def file_exists(value, base_path):
    import os
    full_path = os.path.join(base_path, value)
    if not os.path.isfile(full_path):
        raise ValueError(f"Le fichier '{value}' n'existe pas dans le répertoire '{base_path}'. affichage du chemin complet : {full_path}")
    return value

def int_range(value, min, max):
    if not (min <= int(value) <= max):
        raise ValueError(f"La valeur doit être comprise entre {min} et {max}.")
    return int(value)

def min_length(value, min):
    if len(value) < min:
        raise ValueError(f"La valeur doit contenir au moins {min} caractères.")
    return value

def extension_in(value, allowed):
    for ext in allowed:
        if value.endswith(ext.lower()):
            return value
    raise ValueError(f"La valeur doit avoir une extension parmi {allowed}.")

def is_positive_int(value):
    try:
        int_value = int(value)
        if int_value < 1:
            raise ValueError("La valeur doit être un entier positif.")
        return int_value
    except ValueError:
        raise ValueError("La valeur doit être un entier positif.")

def convert_minutes_to_ms(value):
    try:
        is_positive_int(value)
        minutes = int(value)
        return minutes * 60 * 1000
    except ValueError:
        raise ValueError("La valeur doit être un entier représentant des minutes.")
    
def model_name_exists(value: str) -> str:
    WHISPER_MODELS = [
        "tiny", "tiny.en",
        "base", "base.en",
        "small", "small.en",
        "medium", "medium.en",
        "large", "large-v2", "large-v3"
    ]
    if value not in WHISPER_MODELS:
        raise ValueError(f"La valeur doit être un nom de modèle Whisper valide parmi {WHISPER_MODELS}.")
    return value

def docker_url(value):
    pattern = r"^https?:\/\/[a-zA-Z0-9.-]+:\d+$"
    if not re.match(pattern, value):
        raise ValueError("La valeur doit être une URL valide. ")
    return value
    
# Fonctions pour valider les entrées utilisateur
VALIDATORS = {
    "non_empty": non_empty,
    "as_int": as_int,
    "fqdn_or_localhost": fqdn_or_localhost,
    "no_scheme": no_scheme,
    "nginx_size": nginx_size,
    "filename_safe": filename_safe,
    "file_exists": file_exists,
    "int_range": int_range,
    "min_length": min_length,
    "extension_in": extension_in,
    "is_positive_int": is_positive_int,
    "convert_minutes_to_ms": convert_minutes_to_ms,
    "model_name_exists": model_name_exists,
    "docker_url": docker_url
}
