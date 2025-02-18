# Higgs Boson Discovery using ATLAS Open Data (15005)

## Overview
This project analyzes ATLAS Open Data (record 15005) to rediscover the Higgs boson via the decay channel:
\[
H \to ZZ^* \to 4l
\]
using ROOT and Python. The script reconstructs Z bosons from lepton pairs and selects Higgs candidates based on invariant mass calculations.

## Dataset
The data consists of multiple ROOT files containing 4-lepton events:
- `dataA4lep.root`
- `dataB4lep.root`
- `dataC4lep.root`
- `dataD4lep.root`

## Installation
Ensure you have **ROOT** installed. If not, install it using:
```bash
sudo apt update && sudo apt install root-system
```
Alternatively, use Conda:
```bash
conda install -c conda-forge root
```

## Running the Analysis
1. Clone the repository:
```bash
git clone https://github.com/yourusername/HiggsDiscovery.git
cd HiggsDiscovery
```
2. Download ATLAS Open Data (15005):
```bash
cernopendata-client get -r 15005
```
3. Run the script:
```bash
python analyze_higgs.py
```

## Code Highlights
- **Data Loading:** Uses `TChain` to process multiple ROOT files.
- **Lepton Selection:** Applies acceptance cuts (
\( |\eta| < 2.5 \)).
- **Z Boson Reconstruction:** Pairs opposite-charge leptons within a Z mass window.
- **Higgs Candidate Selection:** Selects events where both Z candidates are valid and calculates invariant mass.
- **Histogramming:** Plots the mass distribution of Higgs candidates.

## Output
- Number of Higgs candidates identified.
- Histogram of invariant mass distribution saved as `refined_mass_distribution.png`.


## Acknowledgments
- ATLAS Open Data ([opendata.cern.ch](https://opendata.cern.ch))
- CERN Open Data Portal
- ROOT Framework

