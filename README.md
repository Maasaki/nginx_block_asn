# Blocage des utilisateurs via des VPN sur pfSense

Ce projet contient une liste d'adresses IP associées à des fournisseurs de VPN, collectées à partir des ASN publics, afin de restreindre l'accès des utilisateurs de votre réseau qui tentent d'utiliser des VPN.

## URL du fichier d'adresses IP

Les adresses IP à bloquer (celles des VPN) sont listées dans le fichier suivant :
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
   - **Description** : Blocage des adresses IP des fournisseurs VPN.

5. Cliquez sur **Save** pour sauvegarder l'alias.

### Étape 2 : Créer une règle de firewall pour bloquer les utilisateurs utilisant des VPN

1. Allez dans **Firewall > Rules**.
2. Sélectionnez l'interface sur laquelle vous voulez appliquer la règle (généralement **LAN**, car c'est à partir de là que les utilisateurs locaux accéderaient à Internet).
3. Cliquez sur **Add** pour créer une nouvelle règle de firewall.
4. Configurez la règle comme suit :
   - **Action** : Sélectionnez **Block**.
   - **Interface** : Choisissez l'interface appropriée (**LAN** pour bloquer les utilisateurs locaux).
   - **Source** : Choisissez **Single host or alias** pour spécifier vos plages d'IP locales, comme `10.0.0.0/24`, `192.168.1.0/24`, ou toute autre plage IP locale que vous utilisez.
   - **Destination** : Sélectionnez **Single host or alias**, puis choisissez l'alias `VPN_Block` que vous avez créé précédemment. Cela bloquera l'accès à ces adresses IP des VPN.

5. Sauvegardez et appliquez les modifications.

### Étape 3 : Vérification et ajustement

Une fois la règle appliquée, vous pouvez utiliser les outils de diagnostic de pfSense pour vérifier si les utilisateurs locaux sont correctement bloqués lorsqu'ils tentent d'accéder aux IP des VPN :
- Accédez à **Diagnostics > Ping** pour tester des IP spécifiques.
- Utilisez **Diagnostics > States** pour vérifier l'état des connexions bloquées.

## Contributeurs

- **[Mathys LYOEN--JARRY](https://github.com/Maasaki)**
- **[Christophe Raffalli](https://github.com/craff)**
