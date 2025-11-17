import pandas as pd
import joblib
import os

def predecir_cross_selling(cliente: dict):
    """
    Genera score, nivel y producto recomendado.
    """

    try:
        # Cargo el modelo entrenado
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

        # --- ARREGLADO: convierto SIEMPRE a string todo lo que sea categórico ---
        X_new = pd.DataFrame([cliente])

        for col in X_new.columns:
            if X_new[col].dtype == "object" or isinstance(X_new[col].iloc[0], str):
                X_new[col] = X_new[col].astype(str).str.lower().str.strip()

        # Aplico label encoding
        for col, le in label_encoders.items():
            if col in X_new.columns:
                try:
                    X_new[col] = le.transform(X_new[col].astype(str))
                except Exception:
                    X_new[col] = 0

        # Completo columnas faltantes
        for col in features:
            if col not in X_new.columns:
                X_new[col] = 0

        X_new = X_new[features]

        # Predigo score
        score = model_score.predict(X_new)[0]

        # Predigo productos
        proba = model_product.predict_proba(X_new)[0]
        clases = encoder_target.classes_
        proba_dict = dict(zip(clases, proba))

        # Saco "ninguno"
        proba_dict.pop("ninguno", None)

        # Productos que ya tiene
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

        # Selección según score
        if score <= 40:
            nivel = "Bajo"
            productos_recomendados = []
        else:
            nivel = "Medio" if score <= 70 else "Alto"
            productos_recomendados = (
                [max(proba_filtrada, key=proba_filtrada.get)]
                if proba_filtrada else []
            )

        return {
            "score": round(float(score), 2),
            "nivel": nivel,
            "productos_recomendados": productos_recomendados
        }

    except Exception as e:
        print(f"❌ error al ejecutar la predicción: {e}")
        raise e
