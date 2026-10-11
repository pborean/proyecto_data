"""
15_waffle_hogares.py
Waffle de 100 cuadraditos: de cada 100 hogares, cuántos recurrieron en los últimos 3 meses a cada fuente de crédito,
para el decil 1 (el más pobre), el decil 5 (medio) y el decil 10 (el más rico).
Fuente: INDEC, EPH continua, base de hogares (V14, V15 y V16), ya procesada por scripts/09_eph_endeudamiento_decil.py.
Entrada: resultados/tablas/eph_endeudamiento_decil.csv
Salida:  resultados/graficos/waffle_hogares.png/.svg
Cada cuadradito es 1 de cada 100 hogares. Las fuentes no se excluyen entre sí: un hogar puede usar más de una,
por eso cada waffle se lee por separado y no suman 100.
"""
from inicio import np, pd, mpl, plt, CARPETA
from matplotlib.patches import Rectangle

mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS, VACIO = "#FAF8F3", "#2B2B2B", "#8A8680", "#E5E1D8"
FUENTES = [("V15", "Préstamo de\nbanco o financiera", "#2F6F7A"),
           ("V16", "Cuotas o fiado\n(tarjeta o libreta)", "#C07F12"),
           ("V14", "Préstamo de\nfamilia o amigos", "#8A8680")]
DECILES = [(1, "Decil 1\n(10% más pobre)"), (5, "Decil 5\n(medio)"), (10, "Decil 10\n(10% más rico)")]

tabla = pd.read_csv(CARPETA / "resultados/tablas/eph_endeudamiento_decil.csv", index_col=0, encoding="utf-8-sig")

def dibujar_waffle(ax, pct, color):
    """100 cuadraditos en una grilla 10x10, llenando de abajo hacia arriba y de izquierda a derecha."""
    n = int(round(pct))
    for k in range(100):
        fila, col = divmod(k, 10)
        ax.add_patch(Rectangle((col, fila), .88, .88, facecolor=color if k < n else VACIO, edgecolor="none"))
    ax.set_xlim(-.1, 10); ax.set_ylim(-.1, 10)
    ax.set_aspect("equal"); ax.axis("off")

fig, ejes = plt.subplots(3, 3, figsize=(9.5, 10.5), facecolor=FONDO)
for i, (var, etiqueta, color) in enumerate(FUENTES):
    for j, (decil, titulo) in enumerate(DECILES):
        ax = ejes[i, j]
        ax.set_facecolor(FONDO)
        pct = float(tabla.loc[decil, var])
        dibujar_waffle(ax, pct, color)
        ax.text(5, -1.45, f"{pct:.0f}".replace(".", ",") + " de cada 100", ha="center", va="center",
                fontsize=11, fontweight="bold", color=color if var != "V14" else TINTA)
        if i == 0:
            ax.set_title(titulo, fontsize=11, color=TINTA, pad=10, fontweight="bold")
        if j == 0:
            ax.text(-1.2, 5, etiqueta, ha="right", va="center", fontsize=10.5, color=TINTA)

fig.suptitle("De cada 100 hogares, cuántos recurrieron a cada fuente de crédito",
             x=0.02, y=0.985, ha="left", fontsize=14, fontweight="bold", color=TINTA)
fig.text(0.02, 0.012,
         "Fuente: INDEC, EPH continua, base de hogares (V14, V15 y V16: últimos 3 meses), trimestres de 2024 a 1T2026; elaboración propia.\n"
         "Cada cuadradito es 1 de cada 100 hogares del decil de ingreso per cápita familiar. Un hogar puede usar más de una fuente, por eso cada fila se lee por separado.\n"
         "Mide si el hogar recurrió a la fuente, no cuánto debe ni si está en mora. No incluye hogares sin ingreso declarado.",
         fontsize=8, color=GRIS, va="bottom")
fig.subplots_adjust(left=0.22, right=0.97, top=0.92, bottom=0.115, hspace=0.35, wspace=0.08)
for ext in ("png", "svg"):
    fig.savefig(CARPETA / f"resultados/graficos/waffle_hogares.{ext}", dpi=200, facecolor=FONDO)
print(tabla.loc[[d for d, _ in DECILES]].round(1))
print("Guardado.")
