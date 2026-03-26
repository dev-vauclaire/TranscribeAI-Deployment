import os
import yaml
from python_lib import Schema

SCHEMA_FILE = "config/.env.schema.yaml"
ENV_FILE = "config/.env"

if __name__ == "__main__":
    # Etape 1 : Charger le fichier YAML en tant que dictionnaire Python
    try:
        with open(SCHEMA_FILE, "r") as file:
            schema_dict = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {SCHEMA_FILE} est introuvable.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Erreur lors du chargement du fichier YAML : {e}")
        exit(1)
    except Exception as e:
        print("Une erreur inattendue s'est produite lors du chargement du fichier YAML :", e)
        exit(1)

    # Etape 2 : Valider la structure du schéma et construire les objets Python à partir du dictionnaire
    try:
        schema = Schema.model_validate(schema_dict)
    except Exception as e:
        print("Erreur lors de la validation du schéma :", e)
        exit(1)

    # Etape 3 : Trier les sections et les variables d'environnement par ordre défini dans le schéma
    schema_ordered = schema.sorted()

    # Etape 4 : Demander à l'utilisateur de saisir les valeurs pour chaque variable d'environnement, en appliquant les validations définies dans le schéma
    env_values = schema_ordered.get_config_from_user()

    # Etape 5 : Générer le fichier .env à partir des valeurs saisies par l'utilisateur
    if os.path.exists(ENV_FILE):
        overwrite = input(f"Le fichier {ENV_FILE} existe déjà. Voulez-vous l'écraser ? (y/n) : ").strip().lower()
        if overwrite != 'y':
            print("Opération annulée. Le fichier .env n'a pas été modifié.")
            exit(0)

    with open(ENV_FILE, "w") as env_file:
        for key, value in env_values.items():
            env_file.write(f"{key}={value}\n")