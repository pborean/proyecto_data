"""
03_tasa_real_media.py: tasa real mensual de las tarjetas de crédito.
Línea fina: dato de cada mes. Línea gruesa: media móvil de 12 meses.

Salida: resultados/graficos/tasa_real_media.png
"""
from inicio import pd, plt, cargar_panel, COLORES, ruta_grafico

df = cargar_panel()

r = df["r_tarjetas"] * 100            # tasa real, % por mes
media12 = r.rolling(12).mean()        # media del mes y los 11 anteriores
color = COLORES["r_tarjetas"]

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(r.index, r, color=color, linewidth=0.8, alpha=0.4, label="Dato del mes")
ax.plot(media12.index, media12, color=color, linewidth=2.4, label="Media móvil de 12 meses")
ax.axhline(0, color="black", linewidth=0.8)

mes_min = r.idxmin()
ax.annotate(f"Dic 2023: {r.min():.1f}%\n(inflación 25%)",
            xy=(mes_min, r.min()),
            xytext=(pd.Timestamp("2021-03-01"), -10.5),
            arrowprops=dict(arrowstyle="-", color="gray"), fontsize=9, color="#444")

ax.set_ylabel("Tasa real, % por mes")
ax.set_title("Tasa real mensual de las tarjetas de crédito", fontsize=11.5, loc="left")
ax.legend(loc="upper left", frameon=False)
plt.tight_layout()
plt.savefig(ruta_grafico("tasa_real_media.png"), dpi=150)
# plt.show()
