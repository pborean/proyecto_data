"""
03_acumulado_deuda.py: nivel 2, deuda sin amortizar respecto del ingreso.
Factor acumulado  prod (1+r)/(1+g)  por sector, desde enero de 2017 (= 1), escala log.
Supuesto: la deuda no se paga y los intereses se capitalizan.

Salida: resultados/graficos/acumulado_<producto>.png
"""
from inicio import pd, plt, cargar_panel, SEGMENTOS, NOMBRES, COLORES, ruta_grafico

df = cargar_panel()

prod = "personales"          # cambiar a "tarjetas" para ver tarjetas
factor = pd.DataFrame({
    s: ((1 + df[f"r_{prod}"]) / (1 + df[f"g_{s}"])).cumprod()
    for s in SEGMENTOS
})
print(factor.iloc[-1].round(2))

fig, ax = plt.subplots(figsize=(9, 5))
for s in SEGMENTOS:
    ax.plot(factor.index, factor[s], color=COLORES[f"g_{s}"], label=NOMBRES[f"g_{s}"])
ax.axhline(1, color="black", linewidth=0.8)
ax.set_yscale("log")
ax.set_ylabel("Deuda / ingreso (enero 2017 = 1)")
ax.set_title(f"Deuda sin amortizar respecto del ingreso, préstamos {prod}")
ax.legend()
plt.tight_layout()
plt.savefig(ruta_grafico(f"acumulado_{prod}.png"), dpi=150)
