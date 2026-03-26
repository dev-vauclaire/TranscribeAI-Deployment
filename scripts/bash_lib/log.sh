# Fournir des logs uniformes 

# Affiche un titre encadré
function display_header() {
    local title="$*"

    # Couleurs (ANSI)
    local C_FRAME="\033[1;34m"  # bleu
    local C_TITLE="\033[1;36m"  # cyan
    local C_RESET="\033[0m"

    # Largeur du texte + padding (2 espaces de chaque côté)
    local padding=2
    local inner_width=$(( ${#title} + padding * 2 ))

    # Ligne horizontale
    local hline
    hline=$(printf '%*s' "$inner_width" '' | tr ' ' '=')

    echo
    echo -e "${C_FRAME}+${hline}+${C_RESET}"
    echo -e "${C_FRAME}|${C_RESET}$(printf "%*s" "$padding" "")${C_TITLE}${title}${C_RESET}$(printf "%*s" "$padding" "")${C_FRAME}|${C_RESET}"
    echo -e "${C_FRAME}+${hline}+${C_RESET}"
}

function log_info() {
    echo -e "\e[34m[INFO]\e[0m $1"
}

function log_success() {
    echo -e "\e[32m[SUCCESS]\e[0m $1"
}

function log_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}