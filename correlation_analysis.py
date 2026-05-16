import matplotlib.pyplot as plt
import seaborn as sns


def run_correlation_analysis(
        merged,
        bacteria_columns
):

    sampled = merged.sample(
        5000,
        random_state=42
    )

    print("\n========== CORRELATION ANALYSIS ==========\n")

    top_bacteria = bacteria_columns[:10]

    correlation_matrix = sampled[
        top_bacteria
    ].corr()

    print(correlation_matrix)

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm"
    )

    plt.title(
        "Correlation Heatmap of Top Bacteria"
    )

    plt.show()