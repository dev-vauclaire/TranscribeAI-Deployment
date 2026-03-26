#!/bin/bash 
# Remettre l’environnement dans un état propre

function cleanup(){

    # Etape 1 : Arrêter et supprimer la stack Docker s'il existe
    log_info "Arrêt et suppression de la stack Docker existante (si présente)..."
    remove_docker_stack

    echo ""

    # Etape 2 : Nettoyer le fichier d'environnement s'il existe
    log_info "Nettoyage du fichier d'environnement..."
    if file_exists "$ENV_FILE"; then
        log_info "Fichier d'environnement trouvé. Suppression en cours..."
        rm "$ENV_FILE"
    else
        log_info "Aucun fichier d'environnement trouvé. Aucun nettoyage nécessaire."
    fi

    echo ""

    log_success "Fin du nettoyage. Prêt pour un nouveau déploiement."
}

function remove_docker_stack() {
    if sudo docker compose -p $PROJECT_NAME down --remove-orphans -v &> /dev/null; then 
        log_success "Stack Docker arrêtée et supprimée avec succès."
    else
        log_info "Aucune stack Docker existante à supprimer ou erreur lors de la suppression. Poursuite du nettoyage."
    fi
}