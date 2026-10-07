from inicio import np, pd, plt, cargar_panel, ruta_grafico

df = cargar_panel()

# Tasa real en % mensual
r = df[["r_personales", "r_tarjetas"]] * 100

# Media móvil de 12 meses (promedio del mes y los 11 anteriores)
media12 = r.rolling(12).mean()

colores = {"r_personales": "#2a6fbb", "r_tarjetas": "#d9731a"}
nombres = {"r_personales": "Préstamos personales", "r_tarjetas": "Tarjetas de crédito"}

fig, ax = plt.subplots(figsize=(10, 5.5))

for c in r.columns:
    # Dato mensual: línea fina y clara
    ax.plot(r.index, r[c], color=colores[c], linewidth=0.8, alpha=0.35)
    # Media móvil 12 meses: línea gruesa
    ax.plot(media12.index, media12[c], color=colores[c], linewidth=2.2, label=nombres[c])

ax.axhline(0, color="black", linewidth=0.8)

# Anotar el mes más extremo
mes_min = r["r_personales"].idxmin()
ax.annotate(f"Personales, dic 2023: {r['r_personales'].min():.1f}%\n(inflación 25%)",
            xy=(mes_min, r["r_personales"].min()),
            xytext=(pd.Timestamp("2021-03-01"), -9.5),
            arrowprops=dict(arrowstyle="-", color="gray"), fontsize=9, color="#444")

ax.set_ylabel("Tasa real, % por mes")
ax.set_title("Tasa real mensual de endeudamiento (línea fina: dato del mes; línea gruesa: media 12 meses)",
             fontsize=10.5, loc="left")
ax.legend(loc="upper left", frameon=False)

plt.tight_layout()
plt.savefig(ruta_grafico("tasa_real_media.png"), dpi=150)
# plt.show()
