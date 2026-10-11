"""
17_donut_cartera_vs_mora.py
Dos donuts de la cartera de las familias en julio de 2026: de cada $100 prestados, cuánto es de cada línea (izquierda),
y de cada $100 en mora (cartera irregular), cuánto es de cada línea (derecha).
Fuente: BCRA, Anexo estadístico del Informe sobre Bancos, hoja "Calidad de Cartera (por líneas)", bloque "2. Familias - Total":
"Saldo total de financiaciones" (mill. de $ corrientes) y "Ratio de irregularidad" (%). Solo entidades financieras.
Cartera irregular de cada línea = ratio de irregularidad x saldo de la línea. Archivo: datos/crudos/bcra_informe_bancos_anexo.xlsx
Salida: resultados/tablas/cartera_vs_mora_por_linea.csv y resultados/graficos/donut_cartera_vs_mora.png/.svg
"""
from inicio import np, pd, mpl, plt, CARPETA
import datetime as dt
import openpyxl

XLSX = CARPETA / "datos/crudos/bcra_informe_bancos_anexo.xlsx"
FECHAS = [pd.Timestamp("2020-09-01"), pd.Timestamp("2026-07-01")]
F_MOSTRAR = FECHAS[1]
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
LINEAS = ["Personales", "Tarjetas de crédito", "Con garantía hipotecaria", "Con garantía prendaria", "Otros"]
COLORES = {"Personales": "#C07F12", "Tarjetas de crédito": "#2F6F7A", "Con garantía hipotecaria": "#7B5EA7",
           "Con garantía prendaria": "#B8B2A7", "Otros": "#5B5650"}
ETQ = {"Personales": "Personales", "Tarjetas de crédito": "Tarjetas", "Con garantía hipotecaria": "Hipotecarios",
       "Con garantía prendaria": "Prendarios", "Otros": "Otros"}

# ---- 1. leer los bloques "Ratio de irregularidad" y "Saldo total de financiaciones" de Familias - Total ----
ws = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)["Calidad de Cartera (por líneas)"]
filas = list(ws.iter_rows(min_row=1, max_row=100, max_col=210, values_only=True))
ini = next(i for i, r in enumerate(filas) if r[0] and str(r[0]).startswith("2. Familias - Total"))

def leer_bloque(titulo):
    """Devuelve un DataFrame fecha x línea del bloque que empieza en la fila con ese título."""
    t = next(i for i in range(ini, ini + 25) if filas[i][0] and str(filas[i][0]).startswith(titulo))
    enc = next(i for i in range(t, t + 3) if any(isinstance(c, dt.datetime) for c in filas[i]))
    cols = [(j, pd.Timestamp(c)) for j, c in enumerate(filas[enc]) if isinstance(c, dt.datetime)]
    datos = {}
    for r in filas[enc + 1: enc + 8]:
        if r[0] is None or str(r[0]).startswith("Fuente"):
            break
        datos[str(r[0]).strip()] = pd.Series({f: float(r[j]) for j, f in cols if r[j] is not None})
    return pd.DataFrame(datos)

ratio = leer_bloque(".. Ratio de irregularidad")
saldo = leer_bloque(".. Saldo total de financiaciones")
irregular = ratio[LINEAS] * saldo[LINEAS] / 100

# ---- 2. tabla: peso de cada línea en la cartera y en la mora ----
filas_t = []
for f in FECHAS:
    c = saldo.loc[f, LINEAS]; m = irregular.loc[f, LINEAS]
    for l in LINEAS:
        filas_t.append({"fecha": f.strftime("%Y-%m"), "línea": l, "peso_en_cartera_%": 100 * c[l] / c.sum(),
                        "peso_en_mora_%": 100 * m[l] / m.sum(), "mora_de_la_línea_%": ratio.loc[f, l]})
tabla = pd.DataFrame(filas_t)
tabla.round(1).to_csv(CARPETA / "resultados/tablas/cartera_vs_mora_por_linea.csv", index=False, encoding="utf-8-sig")
print(tabla.round(1).to_string(index=False))

# ---- 3. gráfico ----
cartera = 100 * saldo.loc[F_MOSTRAR, LINEAS] / saldo.loc[F_MOSTRAR, LINEAS].sum()
mora = 100 * irregular.loc[F_MOSTRAR, LINEAS] / irregular.loc[F_MOSTRAR, LINEAS].sum()
mora_total = irregular.loc[F_MOSTRAR].sum() / saldo.loc[F_MOSTRAR, LINEAS].sum() * 100

def coma(x, d=0):
    return f"{x:.{d}f}".replace(".", ",")

def donut(ax, valores, centro, subcentro):
    ancho = .42
    ang = 90.0                                    # empieza arriba y avanza en sentido horario
    for l in LINEAS:
        v = valores[l]
        a0, a1 = ang, ang - 360 * v / 100
        ax.add_patch(mpl.patches.Wedge((0, 0), 1, a1, a0, width=ancho, facecolor=COLORES[l], edgecolor=FONDO, lw=2))
        mid = np.deg2rad((a0 + a1) / 2)
        if v >= 6:                                # etiqueta dentro del anillo
            r = 1 - ancho / 2
            ax.text(r * np.cos(mid), r * np.sin(mid), f"{coma(v)}%", ha="center", va="center",
                    fontsize=10.5, fontweight="bold", color="white" if l != "Con garantía prendaria" else TINTA)
        else:                                     # etiqueta chica, afuera
            ax.text(1.12 * np.cos(mid), 1.12 * np.sin(mid), f"{coma(v)}%", ha="left" if np.cos(mid) >= 0 else "right",
                    va="center", fontsize=9, color=TINTA)
        ang = a1
    ax.text(0, .08, centro, ha="center", va="center", fontsize=15, fontweight="bold", color=TINTA)
    ax.text(0, -.17, subcentro, ha="center", va="center", fontsize=9, color=GRIS)
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.2, 1.2); ax.set_aspect("equal"); ax.axis("off")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 6.4), facecolor=FONDO)
donut(a1, cartera, "$100", "prestados a las familias")
donut(a2, mora, "$100", f"en mora (mora total: {coma(mora_total, 1)}%)")
a1.set_title("Dónde están los préstamos", loc="center", fontsize=12.5, fontweight="bold", color=TINTA, pad=6)
a2.set_title("Dónde está la mora", loc="center", fontsize=12.5, fontweight="bold", color=TINTA, pad=6)

handles = [mpl.patches.Patch(color=COLORES[l], label=ETQ[l]) for l in LINEAS]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=10, bbox_to_anchor=(.5, .1))
fig.suptitle("Los préstamos personales pesan más en la mora que en la cartera; los hipotecarios, mucho menos",
             x=0.02, y=0.975, ha="left", fontsize=13.5, fontweight="bold", color=TINTA)
fig.text(0.02, 0.012,
         "Fuente: BCRA, Anexo estadístico del Informe sobre Bancos (saldos e irregularidad por línea, familias, sistema financiero), julio de 2026; elaboración propia.\n"
         "Cartera irregular = situaciones 3 a 6. Peso en la mora = ratio de irregularidad de la línea x saldo de la línea. \"Otros\" es una línea chica con mora muy alta.",
         fontsize=8, color=GRIS, va="bottom")
fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.17, wspace=0.05)
for ext in ("png", "svg"):
    fig.savefig(CARPETA / f"resultados/graficos/donut_cartera_vs_mora.{ext}", dpi=200, facecolor=FONDO)
print("Guardado.")
