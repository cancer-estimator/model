def p_at_k(y_true, y_pred, k: int, decision_threshold: float):
    k_values = y_pred.sort_values(ascending=False).sort_index().head(k)
    y_true_sorted = y_true.loc[k_values.index]
    # Converter previsões contínuas para classes com base no limiar
    y_pred_class = (k_values >= decision_threshold).astype(int)
    tp = ((y_pred_class == 1) & (y_true_sorted == 1)).sum()
    fp = ((y_pred_class == 1) & (y_true_sorted == 0)).sum()
    p_at_k_alt = tp / (tp + fp)
    p_at_k = tp / k
    print(f"p@(k={k}) = {round(p_at_k, 3)} | TP = {tp} / FP={fp} | TP/(TP+FP) = {p_at_k_alt}")
    return p_at_k
