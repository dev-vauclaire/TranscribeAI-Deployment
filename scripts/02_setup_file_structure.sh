function setup_file_structure() {

    # Etape 1 : Vérifier et créer les dossiers requis
    for dir in "${REQUIRED_DIR[@]}"; do
        if folder_exists "$dir"; then
            log_success "Le dossier '$dir' existe déjà."
        else
            log_info "Création du dossier '$dir'..."
            create_folder "$dir"
            log_success "Dossier '$dir' créé avec succès."
        fi
    done

    # Etape 2 : Vérifier et créer les fichiers requis
    for file in "${REQUIRED_FILES[@]}"; do
        if file_exists "$file"; then
            log_success "Le fichier '$file' existe déjà."
        else
            log_error "Le fichier '$file' est manquant. Veuillez vous assurer que tous les fichiers nécessaires sont présents dans le répertoire de déploiement."
            exit 1
        fi
    done
}