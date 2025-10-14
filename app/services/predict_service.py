import pandas as pd
import joblib
import os


def predecir_cross_selling(cliente: dict):
    """
    Recibe un cliente (dict) y devuelve su score, nivel y productos recomendados.
    Filtra 'ninguno' y los productos que el cliente ya posee.
    """
    # 1️⃣ Cargar modelo entrenado
    MODEL_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "ai_models",
        "modelo_cross_selling_1.joblib"
    )
    bundle = joblib.load(MODEL_PATH)

    model_score = bundle["model_score"]
    model_product = bundle["model_product"]
    label_encoders = bundle["label_encoders"]
    encoder_target = bundle["encoder_target"]
    features = bundle["feature_names"]

    # 2️⃣ Convertir cliente a DataFrame
    X_new = pd.DataFrame([cliente])

    # 3️⃣ Normalizar texto (minúsculas, sin espacios)
    for col in X_new.select_dtypes(include=["object"]).columns:
        X_new[col] = X_new[col].str.lower().str.strip()

    # 4️⃣ Aplicar encoders (para variables categóricas)
    for col, le in label_encoders.items():
        if col in X_new.columns:
            try:
                X_new[col] = le.transform(X_new[col].astype(str))
            except ValueError:
                X_new[col] = 0  # valor neutro para categorías no vistas

    # 5️⃣ Alinear columnas con las del modelo
    for col in features:
        if col not in X_new.columns:
            X_new[col] = 0
    X_new = X_new[features]

    # 6️⃣ Predecir score y probabilidades
    score = model_score.predict(X_new)[0]
    proba = model_product.predict_proba(X_new)[0]
    clases = encoder_target.classes_
    proba_dict = dict(zip(clases, proba))

    # 7️⃣ Eliminar "ninguno" del resultado
    if "ninguno" in proba_dict:
        proba_dict.pop("ninguno")

    # 8️⃣ Filtrar productos que ya posee el cliente
    productos_cliente = {
        "auto": cliente.get("tiene_auto", 0),
        "hogar": cliente.get("tiene_hogar", 0),
        "vida": cliente.get("tiene_vida", 0),
        "salud": cliente.get("tiene_salud", 0),
    }

    proba_filtrada = {
        prod: prob for prod, prob in proba_dict.items()
        if productos_cliente.get(prod, 0) == 0
    }

    # selección de productos según score
    if score <= 40:
        nivel = "Bajo"
        productos_recomendados = []
    elif score <= 70:
        nivel = "Medio"
        productos_recomendados = sorted(
            proba_filtrada, key=proba_filtrada.get, reverse=True
        )[:3]
    else:
        nivel = "Alto"
        productos_recomendados = (
            [max(proba_filtrada, key=proba_filtrada.get)]
            if proba_filtrada else []
        )

    return {
        "score": round(float(score), 2),
        "nivel": nivel,
        "productos_recomendados": productos_recomendados
    }
