def display_header(*title_parts):
    title = " ".join(title_parts)

    # Couleurs (ANSI)
    C_FRAME = "\033[1;34m"  # bleu
    C_TITLE = "\033[1;36m"  # cyan
    C_RESET = "\033[0m"

    # Largeur du texte + padding (2 espaces de chaque côté)
    padding = 2
    inner_width = len(title) + padding * 2

    # Ligne horizontale
    hline = "=" * inner_width

    print()
    print(f"{C_FRAME}+{hline}+{C_RESET}")
    print(
        f"{C_FRAME}|{C_RESET}"
        + " " * padding
        + f"{C_TITLE}{title}{C_RESET}"
        + " " * padding
        + f"{C_FRAME}|{C_RESET}"
    )
    print(f"{C_FRAME}+{hline}+{C_RESET}")

def display_error(message):
    # Couleurs (ANSI)
    C_ERROR = "\033[1;31m"  # rouge
    C_RESET = "\033[0m"

    print(f"{C_ERROR}Erreur : {message}{C_RESET}")

def display_success(message):
    # Couleurs (ANSI)
    C_SUCCESS = "\033[1;32m"  # vert
    C_RESET = "\033[0m"

    print(f"{C_SUCCESS}Succès : {message}{C_RESET}")

def display_warning(message):
    # Couleurs (ANSI)
    C_WARNING = "\033[1;33m"  # jaune
    C_RESET = "\033[0m"

    print(f"{C_WARNING}Attention : {message}{C_RESET}")

def display_info(message):
    # Couleurs (ANSI)
    C_INFO = "\033[1;34m"  # bleu
    C_RESET = "\033[0m"

    print(f"{C_INFO}Info : {message}{C_RESET}")

