# 📘 Traduction Automatisée de Corpus en Malgache

Ce projet utilise le modèle [`google/madlad400-7b-mt`](https://huggingface.co/google/madlad400-7b-mt) pour traduire automatiquement des jeux de données textuels vers le malgache (`<2mg>`), avec support de quantification 4-bit pour une exécution optimisée sur GPU.

---

## 📁 Structure du projet

```
project-root/
├── scripts/             # Contient un script .sh pour chaque CSV
│   ├── ISEAR.sh
│   ├── imdb.sh
│   ├── ...
├── translate/translate.py   # Script principal de traitement
└── README.md
```

---

## 🚀 Lancement rapide

###  📦 Installation

```bash
pip install -r requirements.txt
```

**Modules requis :**
- `transformers`
- `pandas`
- `torch`
- `wandb`
- `tqdm`
- `bitsandbytes`

> Assurez-vous d’avoir un GPU compatible avec la quantification 4-bit (support `bitsandbytes`).

---


### 3. Datasets supportés

Les fichiers  :

- `ISEAR.csv`             6.027 lignes
- `imdb.csv`              25.000 lignes
- `movieReview.csv`       9.596 lignes
- `semEval2017.csv`       50.334 lignes
- `sentiment140.csv`      1.600.000 lignes
- `TwitterUSAirline.csv`  14.604 lignes

> Chaque fichier doit contenir une colonne `text` à traduire.

---

###  🛠️ Lancer la traduction

Exécutez le script correspondant, par exemple :

```bash

#
#python translate/translate.py \
#  --file imdb.csv \
#  --link  https://drive.google.com/file/d/#1qoi4MeKGQsMNDWd_oyWQil87E-paO9vv/view?usp=drive_link \
#  --start_index 0 \
 # --end_index 1000


bash translate/script/ISEAR.sh
```

Chaque script :
- traduit les 1000 premières lignes,
- logge un **artifact sur Weights & Biases**.

---


## 📤 Résultat

- Exemple de fichier généré :
  ```
  translated_ISEAR_0_1000.csv
  ```
- Artifact associé sur W&B :
  ```
  ISEAR_0_1000_output
  ```

---

## 📌 Remarques

- Nettoyage automatique du texte : suppression des URLs, parenthèses, tirets, etc.
- Traitement par batch (`batch_size=16`).
- Chargement du modèle optimisé avec `BitsAndBytesConfig` pour réduire l’utilisation mémoire.

---

## 🧠 Auteurs & Crédits

- Traduction basée sur [`google/madlad400-7b-mt`](https://huggingface.co/google/madlad400-7b-mt)
- Projet conçu pour le prétraitement NLP multilingue et la valorisation du corpus malgache 🇲🇬
