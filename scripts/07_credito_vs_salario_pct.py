from inicio import np, pd, plt, cargar_panel, ruta_grafico
from matplotlib.ticker import FuncFormatter

df = cargar_panel()

# Variación acumulada en %: (1 + x_1)(1 + x_2)... - 1
inicio = df.index[0] - pd.offsets.MonthBegin(1)
def acumulado_pct(serie):
    s = 100 * ((1 + serie).cumprod() - 1)
    return pd.concat([pd.Series([0.0], index=[inicio]), s])

credito = acumulado_pct(df["r_personales"])
sueldos = {
    "Salario privado registrado": ("g_priv_reg", "#1f9a74"),
    "Salario público":            ("g_publico",  "#8a4fb5"),
    "Salario no registrado":      ("g_no_reg",   "#b8860b"),
}

fig, ax = plt.subplots(figsize=(10, 5.5))

ax.plot(credito.index, credito, color="#2a6fbb", linewidth=2.8,
        label="Deuda por préstamo personal (sin pagar)")
for nombre, (col, color) in sueldos.items():
    s = acumulado_pct(df[col])
    ax.plot(s.index, s, color=color, linewidth=2.0, label=nombre)

ax.axhline(0, color="black", linewidth=0.8)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:+.0f}%" if v != 0 else "0%"))
ax.set_ylabel("Variación real acumulada desde dic 2016")
ax.set_title("Lo que debés crece más que lo que cobrás", fontsize=12, loc="left")
ax.legend(loc="upper left", frameon=False)

fig.text(0.01, 0.01, "Supuesto: la deuda no se paga y los intereses se acumulan. Salarios: índice de salarios INDEC; tasa: BCRA; precios: IPC INDEC.",
         fontsize=8, color="#555")
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig(ruta_grafico("credito_vs_salario_pct.png"), dpi=150)
# plt.show()

print("Deuda: %+.0f%%" % credito.iloc[-1])
for nombre, (col, _) in sueldos.items():
    print(nombre, "%+.1f%%" % acumulado_pct(df[col]).iloc[-1])
