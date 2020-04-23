# nx_creative
Lead dispatch script

# Script de récupération de leads

Ce script permet d'extraire les leads dans les googlesheet rapidement

## Installation

Pour que le script fonctionne, entrez ces commandes dans votre shell après avoir cloné le repo:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Extraction simple (sélection des leads les plus anciens):
```python
python sheets NOM_DUCLIENT
```

Extraction simple (sélection des leads les plus récents):
```python
python sheets NOM_DUCLIENT --premium
```

Extraction simple (sélection des leads aléatoirement):
```python
python sheets NOM_DUCLIENT --rand
```