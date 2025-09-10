# 🏆 BAREC 2025 Shared Task - Championship Results

[![BAREC 2025](https://img.shields.io/badge/BAREC-2025-gold?style=for-the-badge)](https://barec.camel-lab.com/sharedtask2025)
[![First Place](https://img.shields.io/badge/🥇-FIRST_PLACE-FFD700?style=for-the-badge)](https://barec.camel-lab.com/sharedtask2025)

## 🎯 Overview

This repository contains our **championship-winning solution** for the **BAREC 2025 Shared Task on Arabic Readability Assessment** by the **!MSA Team**. We achieved exceptional performance across multiple tracks, demonstrating the effectiveness of our ensemble-based approach for Arabic text readability assessment.

### 🏅 Competition Results

| Track | Task | Ranking | Achievement |
|-------|------|---------|-------------|
| **Strict Track** | Sentence-level Readability Assessment | 🥇 **1st Place** | [CodaBench](https://www.codabench.org/competitions/9083/) |
| **Strict Track** | Document-level Readability Assessment | 🥇 **1st Place** | [CodaBench](https://www.codabench.org/competitions/9086/) |
| **Constrained Track** | Sentence-level Readability Assessment | 🥇 **1st Place** | [CodaBench](https://www.codabench.org/competitions/9084/) |
| **Constrained Track** | Document-level Readability Assessment | 🥇 **1st Place** | [CodaBench](https://www.codabench.org/competitions/9087/) |
| **Open Track** | Sentence-level Readability Assessment | 🥇 **1st Place** | [CodaBench](https://www.codabench.org/competitions/9085/) |
| **Open Track** | Document-level Readability Assessment | 🥇 **1nd Place** | [CodaBench](https://www.codabench.org/competitions/9088/) |

## 🚀 Key Achievements

- **5 First Place** positions across different tracks and tasks
- **1 Second Place** in the most competitive Open Track
- Comprehensive solution covering both sentence and document-level readability assessment
- State-of-the-art performance in Arabic text readability evaluation

## 📊 Track Descriptions

### 🔒 Strict Track
**Constraint:** Models trained exclusively on the BAREC Corpus training set
- **Sentence-level Assessment:** 🥇 **Champion**
- **Document-level Assessment:** 🥇 **Champion**

### ⚖️ Constrained Track  
**Constraint:** BAREC Corpus + SAMER Corpus (document, fragment, word-level) + SAMER Lexicon
- **Sentence-level Assessment:** 🥇 **Champion**
- **Document-level Assessment:** 🥇 **Champion**

### 🌐 Open Track
**Constraint:** No restrictions - any publicly available data allowed
- **Sentence-level Assessment:** 🥇 **Champion**
- **Document-level Assessment:** 🥇 **Champion**

## 🛠️ Technical Approach

Our winning solution leverages a sophisticated ensemble methodology combining multiple state-of-the-art Arabic language models:

### 🤖 Model Architecture
- **AraBERT v2** variants with different configurations
- **CAMeLBERT** for enhanced Arabic understanding
- **AraELECTRA** for improved efficiency
- **mALBERT** for multilingual capabilities

### 🧠 Ensemble Strategy
- **Confidence-based selection** for optimal predictions
- **Majority voting** for robust decision making
- **Weighted averaging** for balanced performance
- **Cross-validation** for reliable model assessment

### 📈 Key Features
- Advanced preprocessing for Arabic text normalization
- Multiple training strategies (ordinal, OLL-15)
- Data augmentation techniques
- Comprehensive evaluation metrics

## 📁 Repository Structure

```
BAREC2025/
├── 📊 DataSets/                    # Training and test datasets
│   ├── 72,000K_Train_Data.csv
│   ├── blind_test_dataset.csv
│   └── ...
├── 📚 Notebooks/                   # Model training notebooks
│   ├── ARAELECTRA.ipynb
│   ├── CAMELBERT.ipynb
│   ├── barec_arabert_oll15.ipynb
│   └── ...
├── 🔧 Core Scripts/
│   ├── ensemble_by_max_confidence.py
│   ├── voting.py
│   ├── avg.py
│   └── differentPrediction.py
└── 📋 Analysis Tools/
    ├── prediction_visualization.py
    └── combine_conf.py
```

## 🎛️ Key Components

### 1. Ensemble Methods (`ensemble_by_max_confidence.py`)
Implements confidence-based ensemble selection for optimal prediction accuracy.

```python
# Selects predictions based on model confidence scores
def ensemble_by_max_confidence_simple(file1_path, file2_path, output_path)
```

### 2. Voting Systems (`voting.py`)
Provides majority and average voting mechanisms for robust decision making.

```python
# Supports both majority and average voting strategies
def voting_ensemble(file_paths, output_file, method='majority')
```

### 3. Prediction Analysis (`differentPrediction.py`)
Analyzes prediction differences and model agreement patterns.

```python
# Comprehensive prediction comparison and analysis
def count_prediction_differences(file1, file2, show_diffs=False)
```

## 🏃‍♂️ Quick Start

### Prerequisites
```bash
pip install pandas numpy transformers torch scikit-learn
```

### Running the Ensemble
```python
# Confidence-based ensemble
from ensemble_by_max_confidence import ensemble_by_max_confidence_simple

result = ensemble_by_max_confidence_simple(
    "model1_predictions.csv", 
    "model2_predictions.csv", 
    "ensemble_output.csv"
)

# Voting ensemble
from voting import voting_ensemble

file_paths = ["pred1.csv", "pred2.csv", "pred3.csv"]
final_pred = voting_ensemble(file_paths, "final_prediction.csv", method='majority')
```


## 🤝 Contributing

We welcome contributions to improve Arabic readability assessment. Please feel free to:

- Open issues for bug reports or feature requests
- Submit pull requests for improvements
- Share your own strategies
- Contribute additional Arabic language models


## 🔗 Links

- **Competition Website:** [BAREC 2025 Shared Task](https://barec.camel-lab.com/sharedtask2025)
- **BAREC Corpus:** [Official Dataset](https://barec.camel-lab.com/)
- **SAMER Corpus:** [Additional Training Data](https://samer.camel-lab.com/)

### 🏆 CodaBench Competition Links

| Track | Task | CodaBench Link |
|-------|------|----------------|
| **Strict Track** | Sentence-level | [Competition 9083](https://www.codabench.org/competitions/9083/) |
| **Strict Track** | Document-level | [Competition 9086](https://www.codabench.org/competitions/9086/) |
| **Constrained Track** | Sentence-level | [Competition 9084](https://www.codabench.org/competitions/9084/) |
| **Constrained Track** | Document-level | [Competition 9087](https://www.codabench.org/competitions/9087/) |
| **Open Track** | Sentence-level | [Competition 9085](https://www.codabench.org/competitions/9085/) |
| **Open Track** | Document-level | [Competition 9088](https://www.codabench.org/competitions/9088/) |

## 🏆 Team

This championship solution was developed by the **MSA Team** - our dedicated team of researchers specializing in Arabic NLP and machine learning.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🎉 Celebrating Excellence in Arabic Readability Assessment 🎉**

*BAREC 2025 Champions - Advancing Arabic NLP Research*

[![GitHub stars](https://img.shields.io/github/stars/Mohamedbasem1/BAREC_2025?style=social)](https://github.com/Mohamedbasem1/BAREC_2025)
[![GitHub forks](https://img.shields.io/github/forks/Mohamedbasem1/BAREC_2025?style=social)](https://github.com/Mohamedbasem1/BAREC_2025)

</div>
