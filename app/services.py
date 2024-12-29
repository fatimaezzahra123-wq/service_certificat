import subprocess
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.join(BASE_DIR, 'certs', 'root')
CLIENTS_DIR = os.path.join(BASE_DIR, 'certs', 'clients')

def sign_certificate(name, domain):
    """
    Signe un certificat client avec le certificat racine.
    """
    # Chemins des fichiers root
    root_key = os.path.join(ROOT_DIR, 'rootCA.key')
    root_cert = os.path.join(ROOT_DIR, 'rootCA.crt')

    # Chemins pour le client
    client_key = os.path.join(CLIENTS_DIR, f"{domain}.key")
    client_csr = os.path.join(CLIENTS_DIR, f"{domain}.csr")
    client_cert = os.path.join(CLIENTS_DIR, f"{domain}.crt")

    # Générer une clé privée pour le client
    subprocess.run([
        "openssl", "genrsa", "-out", client_key, "2048"
    ], check=True)

    # Générer une CSR (Certificate Signing Request) pour le client
    subprocess.run([
        "openssl", "req", "-new", "-key", client_key, "-out", client_csr,
        "-subj", f"/CN={domain}/O={name}"
    ], check=True)

    # Signer le certificat client avec le root CA
    subprocess.run([
        "openssl", "x509", "-req", "-in", client_csr, "-CA", root_cert,
        "-CAkey", root_key, "-CAcreateserial", "-out", client_cert, "-days", "365",
        "-sha256"
    ], check=True)

    # Retourner les chemins des fichiers générés
    return client_key, client_cert


