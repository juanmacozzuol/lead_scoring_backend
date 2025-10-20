import pandas as pd
import joblib
import os


def predecir_cross_selling(cliente: dict):
    """
    recibe un diccionario con los datos del cliente y devuelve
    su score, nivel y los productos recomendados por el modelo (logica de negocio)
    """

    try:
        # cargo el modelo entrenado que está guardado en la carpeta ai_models
        MODEL_PATH = os.path.join(
            os.path.dirname(__file__),
            "..",
            "ai_models",
            "modelo_cross_selling_1.joblib"
        )
        bundle = joblib.load(MODEL_PATH)

        # separo los componentes del modelo
        model_score = bundle["model_score"]       # modelo que predice el puntaje
        model_product = bundle["model_product"]   # modelo que predice el producto
        label_encoders = bundle["label_encoders"] # encoders para variables categóricas
        encoder_target = bundle["encoder_target"] # encoder de las clases de producto
        features = bundle["feature_names"]        # nombres de las columnas usadas al entrenar

        # convierto los datos del cliente a un dataframe
        X_new = pd.DataFrame([cliente])

        # normalizo el texto (paso todo a minúsculas y sin espacios)
        for col in X_new.select_dtypes(include=["object"]).columns:
            X_new[col] = X_new[col].str.lower().str.strip()

        # aplico los encoders para las variables categóricas
        for col, le in label_encoders.items():
            if col in X_new.columns:
                try:
                    X_new[col] = le.transform(X_new[col].astype(str))
                except ValueError:
                    # si el valor no fue visto durante el entrenamiento, lo dejo en 0
                    X_new[col] = 0

        # me aseguro de que las columnas estén alineadas con las del modelo
        for col in features:
            if col not in X_new.columns:
                X_new[col] = 0
        X_new = X_new[features]

        # predigo el score general del cliente
        score = model_score.predict(X_new)[0]

        # obtengo las probabilidades de cada producto
        proba = model_product.predict_proba(X_new)[0]
        clases = encoder_target.classes_
        proba_dict = dict(zip(clases, proba))

        # elimino la categoría "ninguno" si existe
        if "ninguno" in proba_dict:
            proba_dict.pop("ninguno")

        # filtro los productos que el cliente ya tiene
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

        # defino el nivel y los productos recomendados según el score
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

        # retorno la respuesta con los datos principales
        return {
            "score": round(float(score), 2),
            "nivel": nivel,
            "productos_recomendados": productos_recomendados
        }

    except Exception as e:
        print(f"❌ error al ejecutar la predicción: {e}")
        raise e
