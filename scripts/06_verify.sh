
function verify_deployment(){

    # Récupère les IDs des conteneurs de la stack

    # Etape 1 : Vérifie que tous les conteneurs sont "up" (status "running")
    log_info "Vérification que tous les conteneurs sont en status 'running'..."
    CONTAINERS_IDS=$(sudo docker compose -p $PROJECT_NAME ps -a -q) 
    CONTAINER_EXCITED=()
    IS_ALL_UP=true
    
    for CONTAINER_ID in $CONTAINERS_IDS; do
        if ! is_container_up "$CONTAINER_ID"; then
            CONTAINER_EXCITED+=("$CONTAINER_ID")
            IS_ALL_UP=false
        fi
    done

    if [ "$IS_ALL_UP" = false ]; then
        for CONTAINER_ID in "${CONTAINER_EXCITED[@]}"; do
            container_name=$(sudo docker inspect --format '{{.Name}}' $CONTAINER_ID)
            log_error "Conteneur $container_name n'est pas en status 'running'."
            log_info "Vous pouvez consulter les logs du conteneur avec la commande : docker logs $container_name"
        done
        exit 1
    fi      

    log_success "Tous les conteneurs sont en status 'running'."

    # Etape 2 : Attendre que tous les services soient "healthy" (si healthcheck défini)
    log_info "Vérification que tous les services sont 'healthy' (si healthcheck défini)..."
    # while all service.status != "healthy":
    #     sleep(5)

    # Etape 3 : Pour chaque STT curl /ready et vérifier que la réponse est 200
}

# Vérifie que le conteneur avec l'ID $1 est "up" via docker inspect
# Retourne true si le conteneur est "up", false sinon
function is_container_up(){
    local status=$(sudo docker inspect -f '{{.State.Status}}' $1)
    if [ "$status" == "running" ]; then
        return 0
    else
        return 1
    fi
}