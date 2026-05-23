import os
from typing import TextIO, Optional

#AGREGAR CARPETAS A EXCLUIR SI SE DESEA, POR EJEMPLO: "dist", "build", "venv", etc.
EXCLUDE = {".venv", "node_modules", ".git", "__pycache__", ".next", "dist", "build"}

OUTPUT_FILE = "Estructura.txt"


def print_tree(
    path: str,
    prefix: str = "",
    file: Optional[TextIO] = None
):
    try:
        items = os.listdir(path)
    except PermissionError:
        return

    items = sorted(items)

    for i, item in enumerate(items):

        if item in EXCLUDE:
            continue

        full_path = os.path.join(path, item)
        is_last = i == len(items) - 1

        connector = "└── " if is_last else "├── "
        line = prefix + connector + item

        print(line)

        if file is not None:
            file.write(line + "\n")

        if os.path.isdir(full_path):
            extension = "    " if is_last else "│   "
            print_tree(full_path, prefix + extension, file)


if __name__ == "__main__":
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        print_tree(".", file=f)

    print(f"\n✔ Estructura guardada en {OUTPUT_FILE}")

#Ejecutar el script con: python GESTIONGASTRONOMICA/tree.py
