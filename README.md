# nabaztag-wpa2-aes

Firmware Nabaztag:tag (V2) avec support WPA2-AES (RSN/CCMP), compilé par GitHub Actions à partir de nabgcc (RedoX) + firmware_nabaztag.

## Contenu

- `patches/wpa2.patch` : RSN IE correct dans la requête d'association, handshake 4-way WPA2 (descriptor 2, MIC HMAC-SHA1, PTK 48 octets, GTK AES Key Wrap RFC 3394), parsing GTK KDE, chiffrement hardware AES (RT2501).
- `files/aes.{c,h}` : AES-128 decrypt + RFC 3394 key unwrap (validés FIPS-197 + vecteurs officiels RFC 3394 §4.1).
- Le mode `IEEE80211_CRYPT_WPA2_AES = 5` correspond à l'option "WPA-WPA2 encryption" du bootcode testwpa de RedoX.

## Récupérer le firmware

1. Onglet **Actions** -> dernier run "Build firmware" réussi.
2. En bas, section **Artifacts** -> télécharger `firmware-build`.
3. Dézipper : `firmware-42.sim.txt` est le fichier à flasher.

## Flasher le lapin

1. Lapin débranché. Appuyer sur le bouton de la tête et rebrancher en maintenant le bouton (mode configuration, ventre bleu).
2. Depuis un ordinateur connecté au même réseau (ou directement), ouvrir http://192.168.0.1
3. Page de configuration du bootcode -> "firmware upgrade" -> sélectionner `firmware-42.sim.txt` -> valider.
4. Le lapin redémarre avec le nouveau firmware.
5. Dans la config du bootcode, choisir l'option "WPA-WPA2 encryption" et mettre la clé WiFi.

## Prérequis box

Le SSID 2.4 GHz doit accepter WPA2-PSK (AES/CCMP). Sur Freebox Delta : mode de protection "WPA2-PSK/AES" (ou WPA/WPA2 mixte tant que le cipher pairwise CCMP est autorisé).

## Avertissement

Ce firmware est expérimental. Le bootcode n'est pas modifié : en cas d'échec, le lapin reste récupérable en mode configuration (bouton de tête au branchement).
