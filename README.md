# nx_creative
Lead dispatch script

# Script de récupération de leads

Ce script permet d'extraire les leads dans les googlesheet rapidement

## Installation & Utilisation

Pour que le script fonctionne, entrez ces commandes dans votre shell après avoir cloné le repo:

Si vous avez cloné le repo dans 'Documents/script_lead':

Dans l'application iTerm, entrez:

```bash
Documents/script_lead
```
Une fois que vous vous trouvez dans le dossier du script:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Si votre venv est déjà présent, faites uniquement:

```bash
source .venv/bin/activate
```

## Usage

Extraction des leads les plus anciens:
```python
python distrib.py NOM_DU_CLIENT
```

Extraction des leads les plus récents:
```python
python distrib.py NOM_DU_CLIENT --premium
```

Extraction des leads aléatoirement:
```python
python distrib.py NOM_DU_CLIENT --rand
```