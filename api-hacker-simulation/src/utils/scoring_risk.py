import pandas as pd
from scipy.stats import zscore

def compute_group_risk(victims: list[dict]) -> pd.DataFrame:
    """
    Calculate a DataFrame with the metrics and risk score per group
    
    victims: dicts list, each whit at least:
      - 'group_name': str
      - 'country': str
      - 'tactic': str
    """
    # We build a DataFrame from the list of victims
    df = pd.DataFrame(victims)

    # Metric 1: Attack frequency per group
    freq = df.groupby("group_name").size().rename("freq")

    # Metric 2: Repeat targeting (number of distinct countries attacked)
    rec = df.groupby("group_name")["country"].nunique().rename("recurrence")

    # Metric 3: Diversity of tactics
    tac = df.groupby("group_name")["tactic"].nunique().rename("tactics")

    # We combine the three metrics into a single DataFrame.
    scores = pd.concat([freq, rec, tac], axis=1).fillna(0)

    # We normalize each metric using the z-score
    for col in ["freq", "recurrence", "tactics"]:
        scores[f"{col}_z"] = zscore(scores[col].astype(float).fillna(0))

    # We create the total score as the sum of z-scores.
    scores["risk_score"] = (
        scores["freq_z"] + scores["recurrence_z"] + scores["tactics_z"]
    )

    return scores.reset_index()  # Returns columns
