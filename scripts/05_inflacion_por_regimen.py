"""
05_inflacion_por_regimen.py: inflación y tasas promedio en cada régimen de la tarjeta.
Respalda los números del gráfico de 06_grafico_regimenes.py.

Para cada régimen calcula:
  - inflación mensual: media aritmética y geométrica, y anualizada
  - tasa nominal mensual de la tarjeta (media aritmética)
  - tasa real mensual de la tarjeta: media aritmética (la que muestra el gráfico 06),
    media geométrica (la que compone bien) y su equivalente anual

Los quiebres vienen de 04_puntos_de_cambio.py (con MIN_TAMANO = 6).
Si cambiás el análisis, actualizá QUIEBRES (y el mismo QUIEBRES en 06_grafico_regimenes.py).

Salida: resultados/tablas/inflacion_por_regimen.csv
"""
from inicio import np, pd, cargar_panel, ruta_tabla

# Primer mes de cada régimen nuevo
QUIEBRES = ["2020-09", "2023-08", "2024-04"]


def media_geometrica(tasa):
    """Tasa constante que da el mismo resultado acumulado que la serie (tasa en fracción)."""
    return np.exp(np.log1p(tasa).mean()) - 1


def anualizar(tasa_mensual):
    return (1 + tasa_mensual) ** 12 - 1


df = cargar_panel()
inicios = [df.index[0]] + [pd.Timestamp(q) for q in QUIEBRES]
fines = [pd.Timestamp(q) - pd.offsets.MonthBegin(1) for q in QUIEBRES] + [df.index[-1]]

filas = []
for a, b in zip(inicios, fines):
    t = df.loc[a:b]
    pi_geo = media_geometrica(t["pi"])
    r_geo = media_geometrica(t["r_tarjetas"])
    filas.append({
        "régimen": f"{a:%Y-%m} a {b:%Y-%m}",
        "meses": len(t),
        "inflación_media_%_mes": t["pi"].mean() * 100,
        "inflación_geom_%_mes": pi_geo * 100,
        "inflación_anualizada_%": anualizar(pi_geo) * 100,
        "tasa_nominal_tarjeta_%_mes": t["i_tarjetas"].mean() * 100,
        "tasa_real_media_%_mes": t["r_tarjetas"].mean() * 100,          # la del gráfico 06
        "tasa_real_geom_%_mes": r_geo * 100,
        "tasa_real_anualizada_%": anualizar(r_geo) * 100,
    })

tabla = pd.DataFrame(filas).set_index("régimen")
print(tabla.round(2).T.to_string())
tabla.round(4).to_csv(ruta_tabla("inflacion_por_regimen.csv"), encoding="utf-8-sig")
print("\nGuardado: resultados/tablas/inflacion_por_regimen.csv")
