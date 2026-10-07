from inicio import np, pd, plt, cargar_panel, ruta_grafico

df = cargar_panel()

# Dos índices acumulados, ambos en base 100 (dic 2016)
inicio = df.index[0] - pd.offsets.MonthBegin(1)
def acumular(serie):
    s = 100 * (1 + serie).cumprod()
    return pd.concat([pd.Series([100.0], index=[inicio]), s])

credito = acumular(df["r_personales"])          # costo real acumulado del crédito
sueldos = {
    "Salario privado registrado": ("g_priv_reg", "#1f9a74"),
    "Salario público":            ("g_publico",  "#8a4fb5"),
    "Salario no registrado":      ("g_no_reg",   "#b8860b"),
}

fig, ax = plt.subplots(figsize=(10, 5.5))

ax.plot(credito.index, credito, color="#2a6fbb", linewidth=2.8, label="Deuda por préstamo personal (sin pagar)")
for nombre, (col, color) in sueldos.items():
    s = acumular(df[col])
    ax.plot(s.index, s, color=color, linewidth=2.0, label=nombre)

ax.axhline(100, color="black", linewidth=0.8)
ax.set_yscale("log")
ax.set_yticks([50, 100, 200, 400])
ax.set_yticklabels(["50", "100", "200", "400"])
ax.set_ylabel("Índice real (dic 2016 = 100, escala log)")
ax.set_title("Lo que debés crece más que lo que cobrás", fontsize=12, loc="left")
ax.legend(loc="upper left", frameon=False)

fig.text(0.01, 0.01, "Supuesto: la deuda no se paga y los intereses se acumulan. Salarios: índice de salarios INDEC; tasa: BCRA; precios: IPC INDEC.",
         fontsize=8, color="#555")
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig(ruta_grafico("credito_vs_salario.png"), dpi=150)
# plt.show()

print("Deuda:", round(credito.iloc[-1], 1))
