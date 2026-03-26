#!/bin/bash
# Script principal pour déployer la stack TranscribeAI
source scripts/bash_lib/utils.sh
source scripts/bash_lib/log.sh

source scripts/config.sh
source scripts/01_cleanup.sh
source scripts/02_setup_file_structure.sh
source scripts/03_prerequisites.sh
source scripts/04_configure_env.sh
source scripts/05_deploy.sh
source scripts/06_verify.sh

# Etape 1 : Tout nettoyer avant de commencer 
display_header "Nettoyage de l'environnement de déploiement"
echo ""
cleanup

# Etape 2 : Configurer la structure de fichiers nécessaire pour la stack
display_header "Configuration de la structure de fichiers"
echo ""
setup_file_structure

# Etape 3 : Vérifier les prérequis 
display_header "Vérification des prérequis logiciels et matériels"
echo ""
check_prerequisites

# Etape 4 : Configurer le fichier d'environnement via un script Python interactif
display_header "Configuration des variables d'environnement"

echo ""

source ./.venv/bin/activate
python3 scripts/04_configure_env.py
status=$? # Récupère le code de retour du script Python
deactivate

if [ $status -eq 0 ]; then
    log_success "Configuration des variables d'environnement terminée avec succès."
else
    log_error "Erreur pendant la configuration des variables d'environnement, le script d'installation s'est arrêté."
    exit 1
fi


# Etape 5 : Lancer la stack avec docker-compose
display_header "Déploiement de la stack Docker"
echo ""
deploy

# Etape 6 : Vérifier que les services sont opérationnels
time=60
log_info "Attente de $time secondes pour laisser le temps à Docker de démarrer les conteneurs..."
for i in $(seq 1 $time); do
    echo -ne "Attente... $i/$time\r"
    sleep 1
done

display_header "Vérification de la stack Docker"
echo ""
verify_deployment