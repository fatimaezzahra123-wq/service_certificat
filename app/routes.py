from flask import Blueprint, render_template, request, send_file, redirect, url_for, jsonify
from app.services import sign_certificate

bp = Blueprint('main', __name__)

# Dossier où sont sauvegardés les certificats
CERT_PATH = "certs/clients/"
KEY_PATH = "certs/root/"

# Route pour afficher le formulaire
@bp.route('/')
def home():
    return render_template('form.html')

# Route pour générer le certificat
@bp.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    try:
        name = request.form['name']
        domain = request.form['domain']

        # Validation des entrées
        if not name or not domain:
            return "<h1>Erreur :</h1><p>Le nom et le domaine sont obligatoires.</p>", 400

        # Appel au service pour signer le certificat
        key_path, cert_path = sign_certificate(name, domain)

        # Retourne les chemins avec une option de téléchargement
        return f"""
        <h1>Certificat généré avec succès !</h1>
        <p><strong>Clé privée :</strong> <a href="/download_key/{key_path}" target="_blank">Télécharger la clé</a></p>
        <p><strong>Certificat :</strong> <a href="/download_cert/{cert_path}" target="_blank">Télécharger le certificat</a></p>
        <a href="/">Retour</a>
        """
    except Exception as e:
        return f"<h1>Erreur :</h1><p>{str(e)}</p>", 500

# Route pour télécharger le certificat
@bp.route('/download_cert/<path:filename>')
def download_cert(filename):
    try:
        file_path = f"{CERT_PATH}{filename}"
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return f"<h1>Erreur :</h1><p>Le fichier {filename} est introuvable.</p>", 404

# Route pour télécharger la clé privée
@bp.route('/download_key/<path:filename>')
def download_key(filename):
    try:
        file_path = f"{KEY_PATH}{filename}"
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return f"<h1>Erreur :</h1><p>Le fichier {filename} est introuvable.</p>", 404


















