# Alexandria House Prices — Data Mining Pipeline

Analysis and clustering of residential property listings in Alexandria, Egypt, using a full data mining pipeline from raw data to a fuzzy inference system.

## Dataset

`house_prices_dataset.csv` — apartment listings across 53 Alexandria neighborhoods with features covering area, price, amenities, location, and delivery status.

## Pipeline

### 1. Exploratory Data Analysis
- Distribution analysis of numerical features (Area, Price, amenities)
- Correlation heatmap identifying relationships between price and property attributes
- Categorical breakdown by Location, Type, Level, and Delivery_Term

### 2. Preprocessing
- Dropped the single row with a missing `Type` value
- Imputed `Level` and `Furnished` with mode
- Converted `Compound` (free-text, high-missing) to a binary `In_Compound` flag
- Parsed `Delivery_Date` into numeric `years_to_delivery`; flagged unknowns separately
- Applied IQR capping on `Area(SQM)` to limit extreme values
- Applied `log1p` transformation on `Price` (skewness reduced from 12.9 to 0.33)
- One-hot encoded nominal categories (Location, Type, Delivery_Term)
- Scaled continuous features with `RobustScaler`

### 3. Genetic Algorithm — Feature Selection
Optimizes the feature subset for clustering quality (silhouette score with K-Medoids/Manhattan distance).

| Parameter | Value | Description |
|---|---|---|
| Population | 30 | Chromosomes per generation |
| Generations | 30 | Total generations |
| Crossover rate | 0.8 | Single-point crossover probability |
| Mutation rate | 0.02 | Per-gene bit-flip probability |
| Min features | 3 | Minimum selected features per chromosome |
| Tournament size | 4 | Selection pressure |

Chromosome encoding: binary vector (1 = include feature, 0 = exclude). Fitness = silhouette score on the selected subset; penalty of -1 if fewer than 3 features are selected.

### 4. Hierarchical Clustering
Applied on GA-selected features using Ward, Complete, and Average linkage. Dendrograms and silhouette curves were used to select the best K. Final model: Ward linkage, K=2.

### 5. K-Medoids Clustering
Applied on GA-selected features with Manhattan distance. Best K determined by elbow method and silhouette analysis. Cluster profiles summarize mean Price, Area, Bedroom, and Bathroom counts per cluster.

### 6. Fuzzy Logic Inference System
Classifies listings into Low/High price categories using three inputs.

**Inputs:** Area (SQM), Bathroom count, KMedoids Cluster  
**Output:** Price category (Low / High)

Membership functions use triangular sets (small/large for area, few/many for bathrooms, budget/premium for cluster). 26 rules cover all input combinations; defuzzification produces a crisp category score.

## Requirements

```
pandas
numpy
matplotlib
seaborn
scikit-learn
scikit-learn-extra
scipy
skfuzzy
streamlit
pyngrok
```
