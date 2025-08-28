# Husqvarna Automower Data Fetcher (Python)

## 🇬🇧 English

A simple Python script to authenticate against the Husqvarna Automower API and fetch data for each mower:
- `/mowers/{id}` → mower details
- `/mowers/{id}/messages` → mower messages/notifications

Results are saved in a JSON file with a common timestamp.

### Requirements
- Python 3.8+
- `requests` library

Install dependencies:
```bash
pip install requests
```

### Configuration

Create a config.json file in the same folder as the script:

```
{
  "app_key": "YOUR_APP_KEY",
  "app_secret": "YOUR_APP_SECRET"
}
```

You can generate the app_key and app_secret from your [Husqvarna Developer account](https://developer.husqvarnagroup.cloud).

### Usage

Run the script:
```
# Default (reads config.json, writes to mowers_details_messages.json)
python husqvarna_file_auth.py

# Custom config and output file
python husqvarna_file_auth.py my_config.json output.json
```

### Example output

Example output.json:
```
[
  {
    "mower_id": "12345678-abcd-efgh-ijkl-1234567890ab",
    "timestamp": "2025-08-28T14:52:00.123456+00:00",
    "detail": {
      "data": {
        "id": "12345678-abcd-efgh-ijkl-1234567890ab",
        "type": "mower",
        "attributes": {
          "model": "AUTOMOWER® 315X",
          "name": "HusqyCoxy",
          "status": "IN_OPERATION",
          "battery": {
            "percent": 87,
            "charging": false
          },
          "location": {
            "latitude": 45.123456,
            "longitude": 5.987654
          }
        }
      }
    },
    "messages": {
      "data": [
        {
          "id": "msg-001",
          "type": "message",
          "attributes": {
            "timestamp": "2025-08-28T14:30:00Z",
            "message": "Démarrage de la tonte",
            "severity": "INFO"
          }
        },
        {
          "id": "msg-002",
          "type": "message",
          "attributes": {
            "timestamp": "2025-08-28T14:40:00Z",
            "message": "Capteur de levage déclenché",
            "severity": "WARNING"
          }
        }
      ]
    }
  }
]
```

---

## 🇫🇷 Français

Un script Python simple pour se connecter à l’API Husqvarna Automower, s’authentifier avec votre clé et secret d’application et récupérer des informations utiles sur vos tondeuses.
Pour chaque tondeuse associée à votre compte Husqvarna, le script extrait :

- Les détails (`/mowers/{id}`)
- Les messages (`/mowers/{id}/messages`)

Les résultats sont enregistrés dans un fichier JSON avec un horodatage commun.

### Prérequis

- Python 3.8+
- Bibliothèque `requests`

Installer les dépendances :
```
bash
pip install requests
```

### Configuration

Créez un fichier config.json dans le même dossier que le script :
```
{
  "app_key": "VOTRE_APP_KEY",
  "app_secret": "VOTRE_APP_SECRET"
}
```

Vous pouvez générer app_key et app_secret depuis votre [compte développeur Husqvarna](https://developer.husqvarnagroup.cloud)..

### Utilisation

Exécutez le script :
```
# Par défaut (lit config.json, écrit dans mowers_details_messages.json)
python husqvarna_file_auth.py

# Config et fichier de sortie personnalisés
python husqvarna_file_auth.py mon_config.json sortie.json
```

### Exemple de résultat

Exemple de output.json :

```[
  {
    "mower_id": "12345678-abcd-efgh-ijkl-1234567890ab",
    "timestamp": "2025-08-28T14:52:00.123456+00:00",
    "detail": {
      "data": {
        "id": "12345678-abcd-efgh-ijkl-1234567890ab",
        "type": "mower",
        "attributes": {
          "model": "AUTOMOWER® 315X",
          "name": "HusqyCoxy",
          "status": "IN_OPERATION",
          "battery": {
            "percent": 87,
            "charging": false
          },
          "location": {
            "latitude": 45.123456,
            "longitude": 5.987654
          }
        }
      }
    },
    "messages": {
      "data": [
        {
          "id": "msg-001",
          "type": "message",
          "attributes": {
            "timestamp": "2025-08-28T14:30:00Z",
            "message": "Démarrage de la tonte",
            "severity": "INFO"
          }
        },
        {
          "id": "msg-002",
          "type": "message",
          "attributes": {
            "timestamp": "2025-08-28T14:40:00Z",
            "message": "Capteur de levage déclenché",
            "severity": "WARNING"
          }
        }
      ]
    }
  }
]
```
