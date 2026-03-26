# Variables globales
PROJECT_NAME="transcribe-ai"

# Dossier requis
DOCKER_DIR="docker"
CONFIG_DIR="config"
VOLUMES_DIR="$DOCKER_DIR/volumes"
REQUIRED_DIR=("$DOCKER_DIR" "$CONFIG_DIR" "$VOLUMES_DIR")

# Fichier requis
COMPOSE_FILE="$DOCKER_DIR/docker-compose.yml"
ENV_SCHEMA_FILE="$CONFIG_DIR/.env.schema.yaml"
REQUIRED_FILES=(
    "$COMPOSE_FILE"
    "$ENV_SCHEMA_FILE"
)

# Fichier d'environnement
ENV_FILE="$CONFIG_DIR/.env"

PORTS=(80 443)