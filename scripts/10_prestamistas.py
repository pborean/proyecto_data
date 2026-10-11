"""
10_prestamistas.py
Quién presta: porcentaje de la población adulta con al menos un crédito en (a) entidades
financieras (bancos y compañías financieras, EEFF) y (b) proveedores no financieros de crédito
(PNFC: tarjetas no bancarias y otros), total y por rango etario.
Fuente: BCRA, Indicadores de Inclusión Financiera, tabla 4.3.4 (Central de Deudores, sistema
financiero ampliado). Archivo: datos/crudos/bcra_deudores_sfa_grupo_institucional_rango_etario.xlsx
Una persona cuenta una vez por grupo: los grupos NO se suman entre sí.
Quiebre de serie: en julio de 2024 todos los grupos bajan de nivel de golpe,
por eso el cambio del régimen actual se mide de julio de 2024 a diciembre de 2025.
Salida: resultados/tablas/prestamistas_grupo_institucional.csv y resultados/graficos/prestamistas_edad.png/.svg
"""
from pathlib import Path
import datetime as dt
import numpy as np
import openpyxl, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
XLSX = RAIZ / "datos/crudos/bcra_deudores_sfa_grupo_institucional_rango_etario.xlsx"
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
C_EEFF, C_PNFC = "#2F6F7A", "#7B5EA7"
F_QUIEBRE, F_INI, F_FIN = pd.Timestamp("2024-07-01"), pd.Timestamp("2024-07-01"), pd.Timestamp("2025-12-01")

# ---- 1. leer (hoja 4.3.4: fila 5 = encabezado con fechas; col B = grupo, col C = edad) ----
ws = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)["4.3.4"]
filas = list(ws.iter_rows(min_row=1, max_row=130, max_col=140, values_only=True))
fechas = [(j, c) for j, c in enumerate(filas[4]) if isinstance(c, dt.datetime)]
datos, grupo = [], None
for r in filas[5:]:
    grupo = r[1] or grupo
    if r[2] is None:
        continue
    for j, f in fechas:
        datos.append((grupo.split("/")[0].strip(), r[2].strip(), pd.Timestamp(f), r[j]))
df = pd.DataFrame(datos, columns=["grupo", "edad", "fecha", "pct"])
df.to_csv(RAIZ / "resultados/tablas/prestamistas_grupo_institucional.csv", index=False, encoding="utf-8-sig")

tot = df[df.edad == "TOTAL"].pivot(index="fecha", columns="grupo", values="pct")
def por_edad(g, f):
    return df[(df.grupo == g) & (df.fecha == f) & (df.edad != "TOTAL")].set_index("edad")["pct"]
edades = list(por_edad("EEFF", F_FIN).index)
etq = [e.replace(" - ", "–") for e in edades]
cambio = pd.DataFrame({g: por_edad(g, F_FIN) - por_edad(g, F_INI) for g in ("EEFF", "PNFC")})
cambio.round(2).to_csv(RAIZ / "resultados/tablas/prestamistas_cambio_por_edad.csv", encoding="utf-8-sig")
print(tot.loc[[F_INI, F_FIN], ["EEFF", "PNFC", "Bancos Privados", "Bancos Públicos", "Compañías Financieras"]].round(1))
print(cambio.round(1).T)

# ---- 2. gráfico ----
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.6), facecolor=FONDO, gridspec_kw={"width_ratios": [1.1, 1.3]})
for a in (a1, a2):
    a.set_facecolor(FONDO)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRIS)
    a.tick_params(colors=TINTA); a.grid(axis="y", color="#E5E1D8", lw=.8); a.set_axisbelow(True)

# izquierda: serie total desde el último quiebre de serie (jul-2024)
for g, col, nom in (("EEFF", C_EEFF, "Bancos y compañías financieras"), ("PNFC", C_PNFC, "Proveedores no financieros")):
    s = tot[g].loc[F_QUIEBRE:F_FIN]
    a1.plot(s.index, s, color=col, lw=2.4, label=nom)
    a1.text(s.index[-1] + pd.Timedelta(days=12), s.iloc[-1], f"{s.iloc[-1]:.0f}%", color=TINTA, va="center", fontsize=9)
    a1.text(s.index[0] - pd.Timedelta(days=12), s.iloc[0], f"{s.iloc[0]:.0f}%", color=TINTA, va="center", ha="right", fontsize=9)
a1.set_xticks(pd.to_datetime(["2024-07-01", "2025-01-01", "2025-07-01", "2025-12-01"]))
a1.set_xticklabels(["jul-2024", "ene-2025", "jul-2025", "dic-2025"])
a1.set_ylim(15, 45); a1.set_xlim(pd.Timestamp("2024-04-15"), pd.Timestamp("2026-02-15"))
a1.set_ylabel("% de la población adulta con al menos un crédito", color=TINTA)
a1.set_title("Quién presta: total de adultos, desde jul-2024", loc="left", color=TINTA, fontsize=12, fontweight="bold")
a1.legend(frameon=False, loc="upper left")

# derecha: cambio por edad, jul-2024 a dic-2025
x = np.arange(len(edades)); w = .38
a2.bar(x - w / 2, cambio["EEFF"], w, color=C_EEFF, label="Bancos y compañías financieras")
a2.bar(x + w / 2, cambio["PNFC"], w, color=C_PNFC, label="Proveedores no financieros")
a2.set_xticks(x); a2.set_xticklabels(etq, rotation=45, ha="right")
a2.set_xlabel("Edad", color=TINTA); a2.set_ylabel("Cambio en puntos porcentuales", color=TINTA)
a2.set_title("Cuánto creció cada edad, jul-2024 a dic-2025", loc="left", color=TINTA, fontsize=12, fontweight="bold")
a2.legend(frameon=False, loc="upper right")
fig.text(0.01, 0.012, "Fuente: BCRA, Indicadores de Inclusión Financiera, tabla 4.3.4 (Central de Deudores, sistema financiero ampliado). Elaboración propia.\n"
         "Cada persona cuenta una vez por grupo; los grupos no se suman. Se muestra desde julio de 2024 porque ese mes la serie cambia de nivel en todos los grupos y no es comparable con los meses anteriores.",
         fontsize=8, color=GRIS, va="bottom")
fig.tight_layout(rect=(0, .07, 1, 1))
for ext in ("png", "svg"):
    fig.savefig(RAIZ / f"resultados/graficos/prestamistas_edad.{ext}", dpi=200, facecolor=FONDO)
print("Guardado.")
