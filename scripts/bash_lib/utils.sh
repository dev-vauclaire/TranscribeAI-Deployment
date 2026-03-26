# Utilitaires génériques réutilisables 

# Affiche d'un titre de section

# Retourne 0 si le fichier existe, 1 sinon
function file_exists() {
    if [ -f "$1" ]; then
        return 0
    else
        return 1
    fi
}

# Retourne 0 si le répertoire existe, 1 sinon
function folder_exists() {
    if [ -d "$1" ]; then
        return 0
    else
        return 1
    fi
}

function create_folder(){
    mkdir -p "$1"
}

function create_file(){
    touch "$1"
}

# Retourne 0 si la commande existe, 1 sinon
function command_exists() {
    if command -v "$1" &> /dev/null
    then
        return 0
    else
        return 1
    fi
}
