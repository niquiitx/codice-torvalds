import subprocess


def git(cmd):
    return subprocess.check_output(
        cmd,
        shell=True,
        text=True,
        stderr=subprocess.DEVNULL
    ).strip()


def obtener_commits():
    salida = git(
        "git rev-list --reverse --parents HEAD"
    )

    commits = []

    for linea in salida.splitlines():
        partes = linea.split()

        commit_hash = partes[0]

        es_merge = len(partes) > 2

        commits.append((commit_hash, es_merge))

    return commits


def contenido_nucleo(commit_hash):
    try:
        return subprocess.check_output(
            f"git show {commit_hash}:nucleo.txt",
            shell=True,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
    except subprocess.CalledProcessError:
        return None


def contar_numeros(hash_completo):
    return sum(c.isdigit() for c in hash_completo)


def contar_letras_hex(hash_completo):
    return sum(c in "abcdef" for c in hash_completo.lower())


def cesar(letra, shift):
    if not letra.isalpha():
        return letra

    base = ord('A') if letra.isupper() else ord('a')

    return chr(
        (ord(letra) - base + shift) % 26 + base
    )


llave = ""

commits = obtener_commits()

for commit_hash, es_merge in commits:

    contenido = contenido_nucleo(commit_hash)

    if contenido is None:
        continue

    valor = int(commit_hash[:6], 16)

    if valor % 2 == 0:

        caracter = contenido[0]

        shift = contar_numeros(commit_hash)

        resultado = cesar(
            caracter,
            shift
        )

    else:

        caracter = contenido[-1]

        ascii_valor = ord(caracter)

        letras = contar_letras_hex(commit_hash)

        resultado = chr(
            ascii_valor + letras
        )

    llave += resultado

    if es_merge:
        llave = llave[::-1]

print(llave)