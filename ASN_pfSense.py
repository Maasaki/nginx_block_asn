import requests
import re
import os

def get_asn_ip(asn_numbers):
    # Nom du dossier où stocker les fichiers
    directory = "ASN_VPN_pfSense"
    
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(directory):
        os.makedirs(directory)

    for asn_number in asn_numbers:
        # Générer le nom du fichier pour chaque ASN à l'intérieur du dossier
        output_file = os.path.join(directory, f"pfsense_vpn_AS{asn_number.strip()}.txt")

        # Vérifier si le fichier existe déjà, si oui, le supprimer
        if os.path.exists(output_file):
            os.remove(output_file)

        with open(output_file, 'w') as file:
            # Construire l'URL pour chaque ASN avec `type=iplist`
            url = f"https://www.enjen.net/asn-blocklist/index.php?asn={asn_number.strip()}&type=iplist"
            
            # Effectuer la requête GET
            response = requests.get(url)
            
            # Vérifier que la requête s'est bien passée
            if response.status_code == 200:
                # Récupérer le contenu de la réponse
                cleaned_data = re.sub(r'<br\s*/?>', '\n', response.text)
                
                # Utiliser une regex pour extraire les IPv4 et IPv6
                ipv4_regex = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})"
                ipv6_regex = r"([a-fA-F0-9:]+:+[a-fA-F0-9:]+/\d{1,3})"
                
                ipv4_addresses = re.findall(ipv4_regex, cleaned_data)
                ipv6_addresses = re.findall(ipv6_regex, cleaned_data)
                
                # Ajouter un commentaire pour chaque ASN
                file.write(f"# ASN Number : {asn_number.strip()}\n")
                
                # Écrire les plages IPv4 dans le fichier
                if ipv4_addresses:
                    file.write("# IPv4 addresses:\n")
                    file.write(" ;\n".join(ipv4_addresses) + " ;\n\n")
                else:
                    file.write("# No IPv4 addresses found.\n\n")
                
                # Écrire les plages IPv6 dans le fichier
                if ipv6_addresses:
                    file.write("# IPv6 addresses:\n")
                    file.write(" ;\n".join(ipv6_addresses) + " ;\n\n")
                else:
                    file.write("# No IPv6 addresses found.\n\n")
                    
            else:
                print(f"Erreur lors de la récupération des données pour l'ASN {asn_number.strip()}. Code de statut: {response.status_code}")

        print(f"Les plages IPv4 et IPv6 pour l'ASN {asn_number.strip()} ont été enregistrées dans {output_file}.")

# Ajouter manuellement les numéros ASN ici
asn_numbers = ["63023", "13335", "21859", "62240", "14061", "40021", "136787", "40676", "61272"]

# Appeler la fonction avec les ASN fournis
get_asn_ip(asn_numbers)
