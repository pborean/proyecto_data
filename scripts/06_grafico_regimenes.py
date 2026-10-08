"""
06_grafico_regimenes.py: tasa real de tarjetas desde 2020, por régimen, con curva suave.

Color de cada régimen según cuán cara es la deuda: celeste (barata) -> neutro -> rojo (cara).
La curva es la media móvil centrada de VENTANA meses, suavizada con interpolación PCHIP
(no inventa picos). La nota al pie del gráfico dice que está suavizada.
Las medias de cada régimen se calculan con los datos mensuales SIN suavizar.

Salida: resultados/graficos/regimenes_tarjetas.svg y .png (texto editable en Figma)
"""
from inicio import np, pd, mpl, plt, cargar_panel, ruta_grafico
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from scipy.interpolate import PchipInterpolator

INICIO = "2020-09"                              # primer mes que se grafica
QUIEBRES = ["2020-09", "2023-08", "2024-04"]    # mismos que 05_inflacion_por_regimen.py
VENTANA = 5                                     # meses de la media móvil (1 = sin suavizar)
TOPE = 5                                        # tasa real (%) en la que el color llega al extremo

mpl.rcParams["svg.fonttype"] = "none"           # texto editable en Figma

# Paleta: azul = deuda barata, ocre = cerca de cero, rojo = deuda cara
CMAP = LinearSegmentedColormap.from_list(
    "caro", ["#2F6F7A", "#C07F12", "#B3261E"])
NORM = TwoSlopeNorm(vmin=-TOPE, vcenter=0, vmax=TOPE)
FONDO = "#FAF8F3"                               # fondo del gráfico

df = cargar_panel()
mensual = (df["r_tarjetas"] * 100).loc[INICIO:]                      # dato real
suave = mensual.rolling(VENTANA, center=True, min_periods=1).mean()  # media móvil

# Curva suave: interpolación PCHIP sobre la serie suavizada
t = mensual.index.map(pd.Timestamp.toordinal).values.astype(float)
tt = np.linspace(t[0], t[-1], 600)
yy = PchipInterpolator(t, suave.values)(tt)
xx = pd.to_datetime([pd.Timestamp.fromordinal(int(round(v))) for v in tt])

# Tramos de régimen
cortes = [pd.Timestamp(q) for q in QUIEBRES if pd.Timestamp(q) > mensual.index[0]]
limites = [mensual.index[0]] + cortes + [mensual.index[-1] + pd.offsets.MonthBegin(1)]

fig, ax = plt.subplots(figsize=(10, 3.4), facecolor=FONDO)
ax.set_facecolor(FONDO)
for a, b in zip(limites[:-1], limites[1:]):
    media = mensual.loc[a:b - pd.offsets.MonthBegin(1)].mean()
    color = CMAP(NORM(media))
    ax.axvspan(a, b, color=color, alpha=0.16, linewidth=0, zorder=0)
    ax.fill_between(xx, yy, 0, where=(xx >= a) & (xx <= b), color=color, alpha=0.6,
                    linewidth=0, zorder=2)                        # bajo la curva: color del régimen
    ax.axvspan(a, b, ymin=0.97, ymax=1, color=color, linewidth=0, zorder=1)   # barra superior
    oscuro = color[:3]                                               # mismo color pleno para el texto
    centro = a + (b - a) / 2
    ax.text(centro, 0.91, f"{media:+.1f}%".replace(".", ",").replace("-", "−"),
            transform=ax.get_xaxis_transform(), fontsize=13, fontweight="bold",
            color=oscuro, va="center", ha="center")
    ax.text(centro, 0.835, "por mes", transform=ax.get_xaxis_transform(),
            fontsize=8.5, color=oscuro, va="center", ha="center")
for c in cortes:
    ax.axvline(c, color="#222", linewidth=0.9, zorder=2)

ax.plot(xx, yy, color="#1f1f1f", linewidth=2.2, solid_capstyle="round", zorder=4)
ax.axhline(0, color="#222", linewidth=1, zorder=3)

ax.set_xlim(limites[0], limites[-1])
ax.set_ylim(min(-6.5, yy.min() - 1), 10)
ax.set_yticks([-5, 0, 5])
ax.set_yticklabels(["−5%", "0", "+5%"], fontsize=9, fontweight="bold", color="#555")
ax.yaxis.grid(True, color="#999", linestyle=":", linewidth=0.7, alpha=0.6)
ax.set_axisbelow(True)
ax.tick_params(axis="both", length=0)
ax.xaxis.set_major_locator(mpl.dates.YearLocator())
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("%Y"))
plt.setp(ax.get_xticklabels(), fontsize=9, fontweight="bold", color="#555")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.text(0.01, 0.01,
         f"Tasa real mensual de las tarjetas de crédito (media móvil de {VENTANA} meses, curva suavizada).\n"
         "Color: azul = deuda barata, ocre = intermedio, rojo = deuda cara. Fuente: BCRA e INDEC; elaboración propia.",
         fontsize=7, color="#666")
plt.tight_layout(rect=(0, 0.07, 1, 1))
plt.savefig(ruta_grafico("regimenes_tarjetas.svg"))
plt.savefig(ruta_grafico("regimenes_tarjetas.png"), dpi=200)
print("Guardado: regimenes_tarjetas.svg y .png en resultados/graficos/")
