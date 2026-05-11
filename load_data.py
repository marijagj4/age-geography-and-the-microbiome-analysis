import pandas as pd


def load_data():

    metadata = pd.read_csv(
        "sample_metadata (2).tsv",
        sep="\t"
    )

    tags = pd.read_csv(
        "tags (1).tsv.gz",
        sep="\t",
        compression="gzip",
        low_memory=False
    )

    taxonomy = pd.read_csv(
        "taxonomic_table.csv.gz",
        compression="gzip",
        low_memory=False,
        nrows=5000
    )

    taxonomy["srr"] = taxonomy["sample"].str.split("_").str[1]

    age_data = tags[
        tags["tag"] == "age"
    ][["srr", "value"]].copy()

    age_data["value"] = pd.to_numeric(
        age_data["value"],
        errors="coerce"
    )

    age_data = age_data[
        (age_data["value"] >= 0) &
        (age_data["value"] <= 120)
    ]

    age_data = age_data.rename(
        columns={"value": "age"}
    )

    metadata_small = metadata[
        ["srr", "region", "iso"]
    ]

    merged = taxonomy.merge(
        metadata_small,
        on="srr",
        how="left"
    )

    merged = merged.merge(
        age_data,
        on="srr",
        how="left"
    )

    bacteria_columns = taxonomy.select_dtypes(
        include="number"
    ).columns

    bacteria_columns = bacteria_columns.drop(
        ["Unnamed: 0"],
        errors="ignore"
    )

    return merged, tags, bacteria_columns