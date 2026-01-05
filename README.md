# 🌌 Quantum Entanglement: GHZ & W States

<div align="center">

![Qiskit](https://img.shields.io/badge/Qiskit-2.2+-6929C4?style=for-the-badge&logo=qiskit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![IBM Quantum](https://img.shields.io/badge/IBM_Quantum-Enabled-0F62FE?style=for-the-badge&logo=ibm&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Exploration des états intriqués maximalement avec 3 qubits**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Results](#-results) • [Theory](#-theory)

</div>

---

## 📖 Description

Ce projet implémente et analyse deux états quantiques intriqués fondamentaux sur **3 qubits** :
- **État GHZ** (Greenberger-Horne-Zeilinger) : superposition maximale |000⟩ + |111⟩
- **État W** : état intriqué symétrique |001⟩ + |010⟩ + |100⟩

L'expérience peut être exécutée sur :
- ✅ **Simulateur local** (Qiskit Aer)
- ✅ **Simulateur cloud IBM** (Qiskit Runtime)
- ✅ **QPU réel IBM** (ordinateur quantique physique)

## ✨ Features

- 🎯 **Circuits quantiques optimisés** pour les états GHZ et W
- 📊 **Analyse statistique complète** avec distance de variation totale (TVD)
- 🔬 **Calcul d'entropie de von Neumann** pour mesurer l'intrication
- 📈 **Visualisations automatiques** des histogrammes de mesure
- 🌐 **Support IBM Quantum Runtime** avec gestion automatique des backends
- 🔄 **Fallback intelligent** si aucun simulateur n'est disponible
- 🎨 **Interface CLI intuitive** avec options configurables

## 🚀 Installation

### Prérequis
- Python 3.9 ou supérieur
- Compte IBM Quantum (gratuit sur [quantum.ibm.com](https://quantum.ibm.com))

### Configuration

```bash
# Cloner le repository
git clone https://github.com/VOTRE_USERNAME/qiskit-3qubits-ghz-w.git
cd qiskit-3qubits-ghz-w

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les credentials IBM
cp .env.example .env
# Éditer .env et ajouter votre token IBM Quantum
```

### Configuration du token IBM

1. Créez un compte sur [IBM Quantum](https://quantum.ibm.com)
2. Récupérez votre token API depuis votre dashboard
3. Ajoutez-le dans le fichier `.env` :

```env
IBM_QUANTUM_TOKEN=votre_token_ici
IBM_QUANTUM_CHANNEL=ibm_quantum
```

## 💻 Usage

### Exécution locale (simulateur Aer)

```bash
python main.py --runner local --state all --shots 4096
```

### Exécution sur IBM Cloud (simulateur)

```bash
python main.py --runner ibm --state all --shots 4096
```

### Exécution sur un QPU réel

```bash
python main.py --runner ibm --real --state ghz --shots 4096
```

### Options disponibles

| Option | Description | Valeurs |
|--------|-------------|---------|
| `--runner` | Backend d'exécution | `local`, `ibm` |
| `--state` | État quantique à créer | `ghz`, `w`, `all` |
| `--shots` | Nombre de mesures | entier (défaut: 4096) |
| `--real` | Utiliser un QPU réel | flag (sans valeur) |
| `--backend-name` | Forcer un backend spécifique | nom du backend |
| `--outdir` | Dossier de sortie | chemin (défaut: `results`) |

### Exemples

```bash
# État GHZ uniquement sur simulateur local
python main.py --runner local --state ghz --shots 8192

# État W sur un backend IBM spécifique
python main.py --runner ibm --state w --backend-name ibm_kyoto

# Tous les états avec 1000 shots
python main.py --runner local --state all --shots 1000
```

## 📊 Results

Le programme génère automatiquement :

### 1. Statistiques de mesure
```
STATE: GHZ | runner=local | backend=aer_simulator | shots=4096
Counts: {'000': 2048, '111': 2048}
Measured probabilities: {'000': 0.5, '111': 0.5}
Expected probabilities: {'000': 0.5, '111': 0.5}
Total Variation Distance (TVD): 0.0
```

### 2. Entropie de von Neumann
```
Ideal entanglement (Von Neumann entropy, base 2):
{'S(qubit_0)': 1.0, 'S(qubit_1)': 1.0, 'S(qubit_2)': 1.0}
```
*Une entropie de 1.0 indique une intrication maximale*

### 3. Histogrammes de probabilité
Les visualisations sont sauvegardées dans `results/` :
- `ghz_local_aer_simulator.png`
- `w_ibm_backend_name.png`

## 🔬 Theory

### État GHZ (Greenberger-Horne-Zeilinger)

$$|\text{GHZ}\rangle = \frac{1}{\sqrt{2}}(|000\rangle + |111\rangle)$$

**Propriétés :**
- Intrication tripartite maximale
- Violations maximales des inégalités de Bell
- Superposition de tous les qubits dans le même état

**Circuit :**
```
q_0: ──H──●──────
          │
q_1: ─────●──●───
             │
q_2: ────────●───
```

### État W

$$|W\rangle = \frac{1}{\sqrt{3}}(|001\rangle + |010\rangle + |100\rangle)$$

**Propriétés :**
- État intriqué symétrique
- Robuste à la perte d'un qubit (reste intriqué)
- Classe d'équivalence différente de GHZ sous LOCC

**Circuit :**
```
q_0: ──RY(θ₁)──●──────────
               │
q_1: ──────────X──RY(θ₂)──●──
                           │
q_2: ──────────────────────X──
```

## 📁 Structure du projet

```
qiskit-3qubits-ghz-w/
├── main.py              # Point d'entrée principal
├── requirements.txt     # Dépendances Python
├── .env.example         # Template de configuration
├── README.md           # Ce fichier
├── src/
│   ├── __init__.py
│   ├── circuits.py     # Définition des circuits quantiques
│   ├── runners.py      # Exécution sur différents backends
│   ├── analysis.py     # Analyse statistique et entropie
│   └── plotting.py     # Génération des visualisations
└── results/            # Histogrammes générés (ignoré par git)
```

## 🛠️ Technologies

- **Qiskit 2.2+** - Framework de calcul quantique
- **Qiskit Aer** - Simulateur local haute performance
- **Qiskit IBM Runtime** - Accès aux QPU IBM via API
- **Matplotlib** - Génération de graphiques
- **NumPy** - Calculs numériques
- **Python-dotenv** - Gestion des variables d'environnement

## 🤝 Contributing

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Acknowledgments

- IBM Quantum pour l'accès aux QPU et simulateurs
- La communauté Qiskit pour les excellentes ressources
- Les pionniers de l'intrication quantique : Bell, Greenberger, Horne, Zeilinger, et al.

## 📚 Ressources

- [Documentation Qiskit](https://docs.quantum.ibm.com/)
- [IBM Quantum Experience](https://quantum.ibm.com/)
- [Entanglement Theory](https://en.wikipedia.org/wiki/Quantum_entanglement)
- [GHZ State Paper](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.64.1) (original)

---

<div align="center">

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile ! ⭐**

Fait avec ❤️ et ⚛️

</div>
