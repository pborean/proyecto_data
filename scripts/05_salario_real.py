from inicio import np, pd, plt, cargar_panel, ruta_grafico

df = cargar_panel()

segmentos = {
    "g_priv_reg": ("Privado registrado", "#1f9a74"),
    "g_publico":  ("Público",            "#8a4fb5"),
    "g_no_reg":   ("No registrado",      "#b8860b"),
}

# Índice de salario real: parte de 100 (dic 2016) y acumula (1 + g) mes a mes
base = pd.DataFrame(100.0, index=[df.index[0] - pd.offsets.MonthBegin(1)], columns=list(segmentos))
indice = pd.concat([base, 100 * (1 + df[list(segmentos)]).cumprod()])

print(indice.iloc[-1].round(1))   # valor final de cada sector

fig, ax = plt.subplots(figsize=(10, 5.5))

for col, (nombre, color) in segmentos.items():
    ax.plot(indice.index, indice[col], color=color, linewidth=2.2, label=nombre)

ax.axhline(100, color="black", linewidth=0.8)
ax.text(pd.Timestamp("2024-09-01"), 101.5, "Nivel de dic 2016 = 100", fontsize=8.5, color="#444")

ax.set_ylabel("Salario real (dic 2016 = 100)")
ax.set_title("Salario real por sector, 2017-2026", fontsize=11, loc="left")
ax.legend(loc="lower left", frameon=False)

plt.tight_layout()
plt.savefig(ruta_grafico("salario_real.png"), dpi=150)
# plt.show()
