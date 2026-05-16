from load_data import load_data
from taxonomy_analysis import run_taxonomy_analysis
from age_analysis import run_age_analysis
from correlation_analysis import run_correlation_analysis
from region_analysis import run_region_analysis
from pca_clustering import run_pca_clustering
from diversity_analysis import run_diversity_analysis

# load data
merged, tags, bacteria_columns = load_data()

# age analysis
merged = run_age_analysis(
    tags,
    merged,
    bacteria_columns
)

# region analysis
merged = run_region_analysis(
    merged,
    bacteria_columns
)

# taxonomy analysis
merged = run_taxonomy_analysis(
    merged,
    bacteria_columns
)

# correlation analysis
run_correlation_analysis(
    merged,
    bacteria_columns
)

# PCA + clustering
merged = run_pca_clustering(
    merged,
    bacteria_columns
)

# diversity analysis
run_diversity_analysis(
    merged,
    bacteria_columns
)