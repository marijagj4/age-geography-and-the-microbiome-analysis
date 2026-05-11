import matplotlib.pyplot as plt
import seaborn as sns


def run_correlation_analysis(
        merged,
        bacteria_columns
):

    print("\n========== CORRELATION ANALYSIS ==========\n")

    top_bacteria = bacteria_columns[:10]

    correlation_matrix = merged[
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