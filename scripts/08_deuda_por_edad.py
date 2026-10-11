"""
08_deuda_por_edad.py
Porcentaje de la población de cada rango etario con al menos un financiamiento,
por tipo de asistencia. Fuente: BCRA, Indicadores de Inclusión Financiera, tabla 4.2.3
(Central de Deudores, sistema financiero ampliado = bancos + proveedores no financieros).
Archivo: datos/crudos/bcra_deudores_sfa_asistencia_rango_etario.xlsx
Salida: resultados/graficos/deuda_por_edad.png/.svg y resultados/tablas/deuda_por_edad.csv
"""
from pathlib import Path
import datetime as dt
import openpyxl, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
XLSX = RAIZ / "datos/crudos/bcra_deudores_sfa_asistencia_rango_etario.xlsx"
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
C_TARJ, C_PERS = "#2F6F7A", "#C07F12"

# ---- 1. leer (hoja 4.2.3: fila 5 = encabezado con fechas) ----
ws = openpyxl.load_workbook(XLSX, data_only=True, read_only=True).worksheets[0]
filas = list(ws.iter_rows(min_row=1, max_row=100, max_col=140, values_only=True))
fechas = [(j, c) for j, c in enumerate(filas[4]) if isinstance(c, dt.datetime)]
datos, tipo = [], None
for r in filas[5:]:
    tipo = r[1] or tipo
    if r[2] is None:
        continue
    for j, f in fechas:
        datos.append((tipo.split("/")[0].strip(), r[2].strip(), f, r[j]))
df = pd.DataFrame(datos, columns=["tipo", "edad", "fecha", "pct"])
# la tabla cambia de rótulo ("Credit cards"/"Credit Cards") según el mes: se unifican
df = df.groupby(["tipo", "edad", "fecha"], as_index=False)["pct"].max()
df.to_csv(RAIZ / "resultados/tablas/deuda_por_edad.csv", index=False, encoding="utf-8-sig")

def corte(t, f):
    s = df[(df.tipo == t) & (df.fecha == pd.Timestamp(f)) & (df.edad != "TOTAL")]
    return s.set_index("edad")["pct"]

edades = list(corte("Personales", "2025-12-01").index)
etq = [e.replace(" - ", "–") for e in edades]
pers25, tarj25 = corte("Personales", "2025-12-01"), corte("Tarjetas de crédito", "2025-12-01")
pers24, tarj24 = corte("Personales", "2024-12-01"), corte("Tarjetas de crédito", "2024-12-01")

# control: caída por el cambio de umbral de la Central de Deudores (jul-2024)
tot = df[(df.tipo == "Personales") & (df.edad == "TOTAL")].set_index("fecha")["pct"]
print("Personales, total adultos:", {str(k.date()): v for k, v in tot["2024-04-01":"2025-01-01"].items()})

# ---- 2. gráfico ----
fig, (a, b) = plt.subplots(1, 2, figsize=(13.5, 6), facecolor=FONDO, gridspec_kw={"width_ratios": [1.15, 1]})
for ax in (a, b):
    ax.set_facecolor(FONDO)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRIS)
    ax.tick_params(colors=TINTA, length=0, labelsize=10)
    ax.grid(axis="y", color="#E4DFD3", lw=0.8)
    ax.set_axisbelow(True)
x = range(len(edades))
a.plot(x, tarj25.values, color=C_TARJ, lw=2.4, marker="o", ms=5)
a.plot(x, pers25.values, color=C_PERS, lw=2.4, marker="o", ms=5)
a.text(10.9, tarj25.iloc[11] + 4, "Tarjeta de crédito", color=C_TARJ, fontsize=12, fontweight="bold")
a.text(6.3, 28, "Préstamo personal", color=C_PERS, fontsize=12, fontweight="bold")
a.set_xticks(list(x)); a.set_xticklabels(etq, rotation=45, ha="right")
a.set_ylim(0, 62); a.set_yticks([0, 20, 40, 60]); a.set_yticklabels(["0%", "20%", "40%", "60%"])
a.set_title("Diciembre de 2025: de cada 100 personas de cada edad,\ncuántas tienen al menos una deuda", loc="left", fontsize=12.5, color=TINTA, fontweight="bold")

d_t, d_p = (tarj25 - tarj24).values, (pers25 - pers24).values
w = 0.38
b.bar([i - w / 2 for i in x], d_t, w, color=C_TARJ, label="Tarjeta de crédito")
b.bar([i + w / 2 for i in x], d_p, w, color=C_PERS, label="Préstamo personal")
b.legend(loc="lower right", frameon=False, fontsize=10.5, labelcolor=TINTA)
b.axhline(0, color=GRIS, lw=0.8)
b.set_xticks(list(x)); b.set_xticklabels(etq, rotation=45, ha="right")
b.set_ylim(-2.5, 9.5); b.set_yticks([0, 3, 6, 9]); b.set_yticklabels(["0", "+3", "+6", "+9"])
b.set_title("Cambio en un año (dic-2024 a dic-2025),\nen puntos porcentuales", loc="left", fontsize=12.5, color=TINTA, fontweight="bold")
b.text(0.2, 8.6, "Personales: de +5 a +7 puntos entre los 20 y los 70 años.\nTarjetas: de +1 a +3 puntos.", fontsize=10.5, color=TINTA, va="top")

fig.text(0.01, 0.01, "Adultos = 15 años o más. Cada persona cuenta una vez por producto, por eso no se suman. Se compara dic-2024 con dic-2025 porque en jul-2024 "
         "cambió el umbral de la Central de Deudores (de \\$1 mil a \\$25 mil).\nFuente: BCRA, Indicadores de Inclusión Financiera, tabla 4.2.3 (Central de Deudores, bancos y proveedores no financieros); elaboración propia.",
         fontsize=8.5, color=GRIS, ha="left", va="bottom")
fig.tight_layout(rect=(0, 0.07, 1, 1))
out = RAIZ / "resultados/graficos"
fig.savefig(out / "deuda_por_edad.png", dpi=200, facecolor=FONDO)
fig.savefig(out / "deuda_por_edad.svg", facecolor=FONDO)
print("ok")
print((pers25 - pers24).round(1).to_dict()); print((tarj25 - tarj24).round(1).to_dict())
