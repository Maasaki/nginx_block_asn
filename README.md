# Blocage des VPN par ASN sur pfSense

Ce projet contient une liste d'adresses IP associées à des VPNs spécifiques, extraites des ASN publics, que vous pouvez utiliser pour bloquer l'accès à votre réseau via pfSense.

## URL du fichier d'adresses IP

Les adresses IP sont disponibles dans le fichier suivant :
- [pfsense_vpn_ALL.txt](https://raw.githubusercontent.com/Maasaki/nginx_block_asn/main/ASN_VPN_pfSense/pfsense_vpn_ALL.txt)

## Utilisation avec pfSense

### Étape 1 : Créer un alias dans pfSense

1. Accédez à l'interface web de votre pfSense.
2. Allez dans **Firewall > Aliases**.
3. Cliquez sur **Add** pour créer un nouvel alias.
4. Configurez l'alias comme suit :
   - **Nom** : Donnez un nom significatif, par exemple `VPN_Block`.
   - **Type d'alias** : Sélectionnez **URL Table (IPs)**.
   - **URL** : Entrez l'URL suivante :
     ```
     https://raw.githubusercontent.com/Maasaki/nginx_block_asn/main/ASN_VPN_pfSense/pfsense_vpn_ALL.txt
     ```
   - **Refresh Frequency** : Choisissez une fréquence de mise à jour (par exemple, toutes les 6 heures ou tous les jours).
   - **Description** : Blocage des adresses IP associées aux VPNs.

5. Cliquez sur **Save** pour sauvegarder l'alias.

### Étape 2 : Créer une règle de firewall pour bloquer les IPs

1. Allez dans **Firewall > Rules**.
2. Sélectionnez l'interface sur laquelle vous voulez appliquer la règle (généralement **WAN** ou **LAN**).
3. Cliquez sur **Add** pour créer une nouvelle règle de firewall.
4. Configurez la règle comme suit :
   - **Action** : Sélectionnez **Block**.
   - **Interface** : Choisissez l'interface appropriée (WAN, LAN, etc.).
   - **Source** : Sélectionnez **Single host or alias** et choisissez l'alias `VPN_Block` que vous avez créé à l'étape précédente.
   - **Destination** : Laissez sur **Any** pour bloquer toutes les destinations.

5. Sauvegardez et appliquez les modifications.

### Étape 3 : Vérification et ajustement

Une fois la règle appliquée, vous pouvez utiliser les outils de diagnostic de pfSense pour vérifier si les adresses IP sont correctement bloquées :
- Accédez à **Diagnostics > Ping** pour tester des IP spécifiques.
- Utilisez **Diagnostics > States** pour vérifier l'état des connexions bloquées.


## Contributeurs

- **[Mathys LYOEN--JARRY](https://github.com/Maasaki)**
- **[Christophe Raffalli](https://github.com/craff)**
