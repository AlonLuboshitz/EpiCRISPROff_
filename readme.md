# EpiCRISPROff




## Requirements


## 🚀 Quick Start

```bash
git clone <repo-url>
cd EpiCRISPROff
python main.py --argfile "Args.txt"
```

---

## 📄 `Args.txt` Configuration File

This file can be altered by the user to train/test/evaluate different model architectures and inputs.

### Arguments:

* `--model (int)`
  Values: `1-6`
  Model types. `6` is the GRU-Embedding model.

* `--cross_val (int)`
  Values:
  `2` – k-cross validation
  `3` – Ensemble

* `--features_method (int)`
  Values:
  `1` – Only sequence
  `2` – With features by columns

* `--features_columns (str)`
  Path to a JSON file with keys as feature descriptions and values as lists of features.

* `--job (str)`
  Options: `train`, `test`, `evaluation`

* `--exclude_guides (list)`
  Format: `[path, str]`
  Exclude sgRNAs from training.

  * `path`: CSV file containing guide sequences
  * `str`: Column name of the guides to exclude

* `--test_on_other_data (list)`
  Format: `[path, str]`

  * `path`: JSON file mapping data names to paths
  * `str`: Name of dataset to test on (must match a key in the JSON)

📁 *Examples can be found in the `Args_examples` folder.*

---
## Data

### Off-target data
The off-target sites (OTSs) the model will be trained on should have the following columns:
BULGES_COLUMN, MISMATCH_COLUMN, TARGET_COLUMN (sgRNA sequence), REALIGNED_COLUMN (sgRNA with bulges if), 
OFFTARGET_COLUMN (OTS sequence), CHROM_COLUMN (chromosome of the OTS), START_COLUMN (start position of the OTS)
END_COLUMN (end position of the OTS), BINARY_LABEL_COLUMN (1/0 label for the OTS), REGRESSION_LABEL_COLUMN.

**To set these spesific columns values one should set the ```Columns_dict``` values in Jsons\Data_columns_and_paths.json**
- if the sgRNA allignment has no alternations from the original sgRNA was can set the values in REALIGNED_COLUMN to TARGET_COLUMN.

### Epigenetic data
When training a model with sequence and epigenetic data the script assumes the epigenetic data is given in the off-target dataset csv file,
i.e, each epigenetic feature has a column with values for that OTS. 
Further explantion of how to train each type of model is below.
**To assign new epigenetic values to an OT dataset one should follow these steps:**
1. Have a valid bed formated epigenetic data: chromosome \t start \t end (at least).
2. Make sure the CHROM_COLUMN, START_COLUMN and END_COLUMN in the OT data are positioned first in this order.
3. Make sure the start and end coordiantes are ints.
4. Run the ```run_intersection``` function in the ```Data_labeling_and_processing.py``` script with paths to the off-target data and folder containing the wanted epigenetic data. The function will output a new off-target data: ```_withEpigenetic.csv``` with the intersection values.


## 🧠 Models

### 🔧 Training

By defualt training a new model will trains on the 78 GUIDE-seq experiments from the CHANGE-seq study.

**To change the training data change the `"Vivo-silico"` dataset path in Jsons/Data_columns_and_paths.json**

**To exclude spesific sgRNAS and their OTSs from the training data: set the `--exclude_guides` Arg in the 'Args.txt' file.**
- To train a model make sure to set the `--job` arg to `train`

#### ✅ Ensemble Training

* Defaults: 10 ensembles × 50 models
* Set `--cross_val` to `3`
* Excludes guides via `--exclude_guides`
* Training on the 78 GUIDE-seq experiments
* To change the training data, modify `"Vivo-silico"` path in `Jsons/Data_columns_and_paths.json`

#### ✅ K-Fold Training

* Set `--cross_val` to `2`
* Do **not** provide `--exclude_guides` or `--test_on_other_data`
* Internally uses 10 `train_guides.txt` files from `Data_sets/train_guides`

#### 📦 Saved Trained Models

* **K-Cross Example:**
  `Models/GRU-EMB/K_cross/Only_sequence/(k').keras`

* **Ensemble Example:**
  `Models/Exclude_Refined_TrueOT/GRU-EMB/Ensemble/With_features_by_columns/10_ensembels/50_models/Binary_epigenetics/H3K27me3/ensemble_(n)/model_(m).keras`

> ⚠️ ENSEMBLE:
> 8 individual features + 2 combinations + only sequence = 11 models
> 11 × 10 ensembles × 50 models = **5500 models**
> 🧠 Training takes time and \~14GB storage.

---

### 🧪 Testing

Use: `--job test`

Saves models predictions

#### ✅ Ensemble Testing

* `--test_on_other_data` **must** be provided
* If not given, ensemble is evaluated on training data
* Saves: `ensemble_(m).pkl` containing average predictions
  (Originally saved all 50 model predictions, now only average due to storage)

#### ✅ K-Cross Testing

* Set `--cross_val` to `2`
* Do **not** provide `--exclude_guides` or `--test_on_other_data`
* Internally uses 10 `test_guides.txt` from `Data_sets/test_guides`

#### 📂 Test Output Paths

* **K-Cross Example:**
  `ML_results/GRU-EMB/K_cross/With_features_by_columns/Feature_name/raw_scores.pkl`

* **Ensemble Example:**
  `ML_results/Exclude_Refined_TrueOT/on_Refined_TrueOT_shapiro_park/GRU-EMB/Ensemble/With_features_by_columns/10_ensembels/50_models/Binary_epigenetics/H3K27me3/Scores/ensemble_m.pkl`

---

### 📈 Evaluation

Evaluates AUROC, AUPRC, and other metrics.
Use: `--job evaluation`

#### ✅ Ensemble Evaluation

* Set `--cross_val` to `3`
* Evaluates each ensemble `.pkl` score file
* Saves:

  * `all_features.pkl`: Dictionary with feature → \[ensemble\_n, metric values]
  * `mean_std.pkl`, `mean_std.csv`
  * `p_val.pkl`, `p_val.csv` (used in `Figures/ROC_PR_figs.py`)

#### ✅ K-Cross Evaluation

* Set `--cross_val` to `2`
* Saves:

  * `results_summary.xlsx`: Partition-wise metrics (in `Plots/GRU-EMB/K_cross/All_partitions`)
  * `averaged_results.csv`, `p_vals.csv`: Averaged metrics + significance test
  * AUROC/AUPRC plots (in `Figures/`)

> 📌 *P-values from Wilcoxon rank-sum test comparing "only sequence" to features*

---

## 🧬 Sequence Models

### 🔹 Only Sequence Model

* Set `features_method = 1` in `Args.txt`

### 🔹 Sequence + Features

* Set `features_method = 2`
* Set `--features_columns` to a valid path, e.g.:

  * `Jsons/feature_columns_dict_change_seq.json`
  * For HSPC testing: `Jsons/feature_columns_dict_hspc.json`

> ⚠️ Make sure feature names in the JSON file match the column names in corresponding dataset.

---

## 🧠 Interpretation

To interpret the **All-epigenetic model** trained on 72 GUIDE-seq experiments:

```bash
python interpertation.py
```

* Evaluates the **first ensemble** trained on all epigenetic features

* Saves SHAP object to:
  `Plots/Interpertability/SHAP_values/all_guides.pkl`

* To interpret a different ensemble:

  * Change the path in `interpertation.py`
  * Modify `run_shap()` feature list to match the trained features

You can run:

```bash
python Figures/EpiCRISPROff_interpertability_plot.py
```

To create a **beeswarm plot** of epigenetic feature importances.

```

## Software

