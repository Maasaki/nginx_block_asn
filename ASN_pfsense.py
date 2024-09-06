import requests
import re
import os
import json
import ipaddress


def get_asn_ip(asn_numbers):
    # Nom du dossier où stocker les fichiers
    directory = "ASN_VPN_pfSense"

    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Générer le nom du fichier pour chaque ASN à l'intérieur du dossier
    output_file = os.path.join(directory, f"pfsense_vpn_ALL.txt")

    # Vérifier si le fichier existe déjà, si oui, le supprimer
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, 'w') as all:

        for asn_number in asn_numbers:
            output_file = os.path.join(directory, f"pfsense_vpn_AS{asn_number.strip()}.txt")

            # Vérifier si le fichier existe déjà, si oui, le supprimer
            if os.path.exists(output_file):
                os.remove(output_file)

            with open(output_file, 'w') as file:
                # Construire l'URL pour chaque ASN avec `type=iplist`
                url = f"https://api.hackertarget.com/aslookup/?q={asn_number.strip()}&output=json"

                # Effectuer la requête GET
                response = requests.get(url)

                # Vérifier que la requête s'est bien passée
                if response.status_code == 200:
                    # Récupérer le contenu de la réponse
                    cleaned_data = json.loads(response.text)
                    asn_num = cleaned_data['as_number']
                    ips = cleaned_data['prefixes']
                    ips = [ipaddress.ip_network(ip) for ip in ips]
                    ip4s = [ ip for ip in ips if ip.version == 4]
                    ip6s = [ ip for ip in ips if ip.version == 6]
                    ip4s = ipaddress.collapse_addresses(ip4s)
                    ip6s = ipaddress.collapse_addresses(ip6s)

                    file.write(f"# ASN Number : {asn_num}\n")
                    all.write(f"# ASN Number : {asn_num}\n")

                    file.write("# IPv4 addresses:\n")
                    all.write("# IPv4 addresses:\n")

                    for ip in ip4s:
                        file.write(f"{ip} ;\n")
                        all.write(f"{ip} ;\n")

                    file.write("# IPv6 addresses:\n")
                    all.write("# IPv6 addresses:\n")

                    for ip in ip6s:
                        file.write(f"{ip} ;\n")
                        all.write(f"{ip} ;\n")

                else:
                    print(f"Erreur lors de la récupération des données pour l'ASN {asn_number.strip()}. Code de statut: {response.status_code}")

            print(f"Les plages IPv4 et IPv6 pour l'ASN {asn_number.strip()} ont été enregistrées dans {output_file}.")

# Ajouter manuellement les numéros ASN ici
asn_numbers = ["63023", "21859", "62240", "14061", "40021", "136787", "40676", "61272"]

# Appeler la fonction avec les ASN fournis
get_asn_ip(asn_numbers)
