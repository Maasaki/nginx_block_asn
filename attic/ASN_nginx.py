import requests
import re
import os

def get_asn_ips(asn_numbers, output_file):
    # Vérifier si le fichier existe déjà
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w') as file:
        for asn_number in asn_numbers:
            # Construire l'URL pour chaque ASN
            url = f"https://www.enjen.net/asn-blocklist/index.php?asn={asn_number.strip()}&type=nginx"
            
            # Effectuer la requête GET
            response = requests.get(url)
            
            # Vérifier que la requête s'est bien passée
            if response.status_code == 200:
                # Récupérer le contenu de la réponse et nettoyer les balises <br />
                cleaned_data = re.sub(r'<br\s*/?>', '\n', response.text)
                
                # Filtrer les lignes qui contiennent 'deny'
                deny_lines = [line.strip() for line in cleaned_data.splitlines() if line.strip().startswith('deny')]
                
                if deny_lines:
                    # Ajouter un commentaire pour chaque ASN
                    file.write(f"# ASN Number : {asn_number.strip()}\n")
                    # Écrire les lignes 'deny' propres dans le fichier
                    file.write("\n".join(deny_lines) + "\n\n")
                else:
                    print(f"Aucune donnée 'deny' trouvée pour l'ASN {asn_number.strip()}.")
            else:
                print(f"Erreur lors de la récupération des données pour l'ASN {asn_number.strip()}. Code de statut: {response.status_code}")

    print(f"Les IPs pour les ASN {', '.join(asn_numbers)} ont été enregistrées dans {output_file}.")

# Ajouter manuellement les numéros ASN ici
asn_numbers = ["63023", "13335", "21859", "62240", "14061", "40021", "136787", "40676", "61272"]

# Spécifier le nom du fichier de sortie
output_file = "multi_asn_ips.conf"

# Appeler la fonction avec les ASN fournis
get_asn_ips(asn_numbers, output_file)