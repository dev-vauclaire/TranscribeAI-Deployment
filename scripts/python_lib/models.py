from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from python_lib.validators import VALIDATORS
from python_lib.logs import display_header, display_success, display_error, display_warning, display_info

# =====================
# ENUMS
# =====================

class ModeEnum(str, Enum):
    user = "user"
    managed = "managed"

class VarTypeEnum(str, Enum):
    string = "string"
    int = "int"
    bool = "bool"

# =====================
# VALIDATOR SPEC
# =====================

class ValidatorSpec(BaseModel):
    name: str
    params: Dict[str, Any] = Field(default_factory=dict)

# =====================
# ENV VARIABLE
# =====================

class EnvVar(BaseModel):
    required: bool = True
    mode: ModeEnum
    title: str
    description: str

    example: Optional[str] = None
    default: Optional[Any] = None

    var_type: VarTypeEnum
    validators: List[ValidatorSpec] = Field(default_factory=list)

    order: Optional[int] = 999

    # Applique les validateurs à la valeur donnée
    def run_validators(self, value):
        for validator in self.validators:
            validator_function = VALIDATORS.get(validator.name)
            if validator_function is None:
                raise ValueError(f"Validator inconnu: {validator.name}")
            value = validator_function(value, **validator.params)
        return value
    
    def ask_user(self):
        prompt = f"Entrez la valeur pour '{self.title}' ou appuyez sur Entrée pour garder la valeur par défaut : "
        return input(prompt)
    
    # Convertit la valeur en fonction du type défini (string, int, bool)
    def cast_type(self, value):
        if self.var_type == VarTypeEnum.int:
            return int(value)
        elif self.var_type == VarTypeEnum.bool:
            if value.lower().strip() in ("yes", "oui", "true", "y", "1"):
                return True
            elif value.lower().strip() in ("no", "non", "false", "n", "0"):
                return False
            else:                 
                raise ValueError("La valeur doit être un booléen (yes/no/oui/non, true/false, y/n, 1/0).")    
        elif self.var_type == VarTypeEnum.string:
            return value.strip()
        else:
            return value.strip()
    
    # Valide la valeur en fonction des règles définies (Type, validateurs)
    def validate_value(self, value):
        if self.required and (value is None or str(value).strip() == ""):
            raise ValueError("Valeur requise.")
        value = self.cast_type(value)
        value = self.run_validators(value)
        return value

    # Affiche les infos de la variable et demande à l'utilisateur de saisir une valeur, puis valide cette valeur et la retourne
    # Return : la valeur validée et convertie dans le type défini
    def get_config_from_user(self):
        info = self.get_info()
        print(info)

        config_value = None

        # Cas où la variable est en mode "managed" (gérée automatiquement par le système)
        if(self.mode == ModeEnum.managed):
            error = False
            while True:
                if error:
                    config_value = self.ask_user()
                else:
                    config_value = self.default
                try:
                    return self.validate_value(config_value)
                except ValueError as e:
                    error = True
                    display_warning(f"Erreur de validation pour la valeur par défaut: {e}")
                    display_info("Veuillez corriger cette variable manuellement.")
        # Cas où la variable est en mode "user" (doit être saisie par l'utilisateur)
        if(self.mode == ModeEnum.user):
            while True:
                user_input = self.ask_user()
                if user_input == "" and self.default is not None:
                    config_value = self.default
                else:
                    config_value = user_input
                try:
                    return self.validate_value(config_value)
                except ValueError as e:
                    display_warning(f"Erreur de validation: {e}")
                    display_info("Veuillez réessayer.")

    # Fonction pour avoir les infos d'une variable
    # Return : une string avec les infos de la variable (titre, description, exemple, défaut, etc.)
    def get_info(self):
        info = f" → {self.title} \n"
        if self.description:
            info += f"Description → {self.description} \n"

        if not self.required:
            info += " (optionnel)"
        if self.example:
            info += f" (exemple: {self.example})"
        if self.default is not None:
            info += f" (Valeur par défaut: {self.default})"
        return info
        

# =====================
# SECTION
# =====================

class Section(BaseModel):
    title: str
    description: str
    docker_image: Optional[str] = None
    order: Optional[int] = 9999

    vars: Optional[Dict[str, EnvVar]] = None

    # Demande à l'utilisateur de configurer les variables de la section
    # Return : un dict avec les valeurs configurées
    def get_config_from_user(self):
        section_config = {}

        if not self.vars:
            display_header("Section", self.title)
            display_info(f"Section '{self.title}' (0 variable) - {self.description}")
            return section_config
        
        section_config["# " + self.title] = self.description

        total_vars = len(self.vars) if self.vars else 0

        display_header("Section", self.title, f"({total_vars} variable{'s' if total_vars > 1 else ''})")
        display_info(self.description)

        for var_key, var in self.vars.items():
            value = var.get_config_from_user()
            section_config[var_key] = value
            print()

        display_success(f"Service '{self.title}' configuré ({total_vars} variable(s)).")

        return section_config

# =====================
# SCHEMA ROOT
# =====================

class Schema(BaseModel):
    services: Dict[str, Section]

    # Trie les sections et les variables par ordre
    # Return : une nouvelle instance de Schema avec les sections et les variables triées
    def sorted(self):
        sorted_services = dict(
            sorted(self.services.items(), key=lambda item: item[1].order)
        )

        new_services = {}

        for key, service in sorted_services.items():
            sorted_vars = dict(
                sorted(service.vars.items(), key=lambda item: item[1].order)
            )

            new_services[key] = service.model_copy(update={
                "vars": sorted_vars
            })

        return self.model_copy(update={"services": new_services})

    # Demande à l'utilisateur de configurer les variables de toutes les sections
    # Return : un dict avec les valeurs configurées
    def get_config_from_user(self):
        env_values = {}

        for service_key, service in self.services.items():
            env_values.update(service.get_config_from_user())

        return env_values
