"""
02_analisis_basico.py: nivel 1, estadística descriptiva.
Media y desvío de las 4 variables finales, muestra completa y por subperíodo,
y el detalle de 2023 (inflación contra tasa nominal).

Salidas: resultados/tablas/resumen_por_periodo.csv, resultados/graficos/grafico_2023.png
"""
from inicio import pd, plt, cargar_panel, COLS, ruta_grafico, ruta_tabla

df = cargar_panel()
print(df.shape, df.index.min().date(), df.index.max().date())

# ---------- Muestra completa ----------
tabla = pd.DataFrame({"media_%": df[COLS].mean() * 100, "desvio_%": df[COLS].std() * 100})
print("\n--- Muestra completa ---")
print(tabla.round(2))

# ---------- Por subperíodo ----------
periodos = {
    "2017-2022": df.loc[:"2022-12"],
    "2023":      df.loc["2023-01":"2023-12"],
    "2024-2026": df.loc["2024-01":],
}
resumen = pd.concat(
    {nombre: sub[COLS].agg(["mean", "std"]).T * 100 for nombre, sub in periodos.items()},
    names=["periodo", "variable"],
)
resumen.columns = ["media_%", "desvio_%"]
n = {nombre: len(sub) for nombre, sub in periodos.items()}
resumen["n_meses"] = resumen.index.get_level_values("periodo").map(n)
print("\n--- Por período ---")
print(resumen.round(2))
resumen.round(4).to_csv(ruta_tabla("resumen_por_periodo.csv"), encoding="utf-8-sig")

# ---------- Qué pasó en 2023 ----------
d23 = df.loc["2023-01":"2023-12", ["pi", "i_tarjetas", "r_tarjetas"]] * 100
print("\n--- 2023 mes a mes (%) ---")
print(d23.round(2))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
ax1.plot(d23.index, d23["pi"], marker="o", label="Inflación mensual")
ax1.plot(d23.index, d23["i_tarjetas"], marker="o", label="Tasa nominal mensual (tarjetas)")
ax1.set_ylabel("% mensual")
ax1.legend()
ax1.set_title("2023: inflación vs tasa nominal")
ax2.bar(d23.index, d23["r_tarjetas"], width=20)
ax2.axhline(0, color="black", linewidth=0.8)
ax2.set_ylabel("% mensual")
ax2.set_title("Tasa real que resulta")
plt.tight_layout()
plt.savefig(ruta_grafico("grafico_2023.png"), dpi=150)
