"""
14_credito_pbi.py
Saldo de crédito al sector privado (total, familias y tarjetas de las familias) como % del PBI, por trimestre, desde 2020-T3.
Crédito: BCRA, Anexo del Informe sobre Bancos, hoja "Calidad de Cartera (por líneas)", "Saldo total de financiaciones"
         (millones de $ corrientes, fin de mes, entidades financieras). Archivo: datos/crudos/bcra_informe_bancos_anexo.xlsx
PBI:     INDEC, Series trimestrales de oferta y demanda globales, cuadro 8 (PIB a precios corrientes, millones de $).
         Archivo: datos/crudos/indec_oferta_demanda_trimestral.xls
INDEC publica cada trimestre "a ritmo anual" (el total del año es casi el promedio de los trimestres, no la suma),
por eso el PBI de 12 meses es el PROMEDIO de los últimos 4 trimestres.
Razón_t = saldo a fin de trimestre / PBI de 12 meses.
Salida: resultados/tablas/credito_pbi.csv y resultados/graficos/credito_pbi.png/.svg
"""
from inicio import np, pd, mpl, plt, CARPETA
import datetime as dt
import openpyxl

XLSX_BCRA = CARPETA / "datos/crudos/bcra_informe_bancos_anexo.xlsx"
XLS_INDEC = CARPETA / "datos/crudos/indec_oferta_demanda_trimestral.xls"
INICIO = "2020-09"                      # primer fin de trimestre del período (igual que el resto: nada anterior)
QUIEBRES = ["2023-08", "2024-04"]
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
C_TOT, C_FAM, C_TARJ = "#7B5EA7", "#2F6F7A", "#C07F12"

# ---- 1. crédito: saldo total de financiaciones, fin de trimestre ----
ws = openpyxl.load_workbook(XLSX_BCRA, data_only=True, read_only=True)["Calidad de Cartera (por líneas)"]
filas = list(ws.iter_rows(min_row=1, max_row=150, max_col=210, values_only=True))


def saldo(titulo_bloque, linea):
    ini = next(i for i, r in enumerate(filas) if r[0] and str(r[0]).startswith(titulo_bloque))
    sub = next(i for i in range(ini, ini + 40) if filas[i][0] and "Saldo total de financiaciones" in str(filas[i][0]))
    enc = sub + 1
    fechas = [(j, pd.Timestamp(c)) for j, c in enumerate(filas[enc]) if isinstance(c, dt.datetime)]
    for r in filas[enc + 1: enc + 12]:
        if r[0] is None or str(r[0]).startswith("Fuente"):
            break
        if str(r[0]).strip() == linea:
            return pd.Series({f: float(r[j]) for j, f in fechas if r[j] is not None})
    raise ValueError(f"no encontré {linea} en {titulo_bloque}")


cred = pd.DataFrame({
    "Sector privado total": saldo("1. Total Sector Privado", "Cartera total"),
    "Familias (total)": saldo("2. Familias - Total", "Cartera total"),
    "Familias: tarjetas de crédito": saldo("2. Familias - Total", "Tarjetas de crédito"),
})
cred = cred[cred.index.month.isin([3, 6, 9, 12])]
cred.index = cred.index.to_period("Q")

# ---- 2. PBI nominal trimestral (cuadro 8, fila B1b) ----
d = pd.read_excel(XLS_INDEC, sheet_name="cuadro 8", header=None)
anio = d.iloc[3].ffill()
trim = d.iloc[4]
fila = d[d[0].astype(str).str.strip() == "B1b"].iloc[0]
pib = {}
for j in range(2, d.shape[1]):
    t = str(trim[j])
    if t[:1] in "1234" and "trimestre" in t and pd.notna(fila[j]):
        a = int(float(str(anio[j]).split()[0].replace("(", "")))
        pib[pd.Period(f"{a}Q{t[0]}")] = float(fila[j])
pib = pd.Series(pib).sort_index()
pib12 = pib.rolling(4).mean()          # promedio de 4 trimestres (valores a ritmo anual)
print("PBI 12m, último:", pib12.index[-1], round(pib12.iloc[-1] / 1e6, 1), "billones")

# ---- 3. razón ----
razon = cred.div(pib12, axis=0).dropna() * 100
razon = razon.loc[pd.Period(INICIO, "Q"):]
razon.index.name = "trimestre"
out = razon.copy()
out["pib_12m_millones"] = pib12.loc[razon.index]
out.round(2).to_csv(CARPETA / "resultados/tablas/credito_pbi.csv", encoding="utf-8-sig")
print(razon.round(2).to_string())

# ---- 4. gráfico ----
x = razon.index.to_timestamp(how="end")
fig, ax = plt.subplots(figsize=(11, 5.6), facecolor=FONDO)
ax.set_facecolor(FONDO)
cortes = [pd.Timestamp(q) for q in QUIEBRES]
lim = [x[0] - pd.offsets.QuarterEnd(1)] + cortes + [x[-1]]
tonos = ["#00000000", "#00000012", "#B3261E14"]
for k in range(3):
    ax.axvspan(lim[k], lim[k + 1], color=tonos[k], lw=0)
for c in cortes:
    ax.axvline(c, color=GRIS, lw=0.8, ls=":")
for col, color in zip(razon.columns, [C_TOT, C_FAM, C_TARJ]):
    ax.plot(x, razon[col], color=color, lw=2.2, marker="o", ms=4)
    ax.annotate(f"{razon[col].iloc[0]:.1f} %", (x[0], razon[col].iloc[0]), xytext=(-6, 0), textcoords="offset points",
                ha="right", va="center", fontsize=9, color=TINTA)
    ax.annotate(f"{col}: {razon[col].iloc[-1]:.1f} %", (x[-1], razon[col].iloc[-1]), xytext=(8, 0), textcoords="offset points",
                ha="left", va="center", fontsize=9.5, color=TINTA)
ax.set_xlim(x[0] - pd.Timedelta(days=260), x[-1] + pd.Timedelta(days=150))
ax.set_ylim(0, None)
ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(decimals=0))
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color="#D9D5CC", lw=0.6)
ax.set_axisbelow(True)
ax.tick_params(colors=TINTA, labelsize=9)
ax.set_title("Crédito de los bancos como % del PBI, desde 2020", loc="left", fontsize=14, color=TINTA, fontweight="bold")
fig.text(0.01, 0.01, "Fuente: BCRA (Informe sobre Bancos, saldo de financiaciones a fin de trimestre, entidades financieras) e INDEC (PIB a precios corrientes, "
         "promedio de 4 trimestres).\nSombreado: regímenes de tasa real (cortes ago-2023 y abr-2024).", fontsize=7.8, color=GRIS, va="bottom")
fig.subplots_adjust(left=0.07, right=0.76, top=0.9, bottom=0.17)
for ext in ("png", "svg"):
    fig.savefig(CARPETA / f"resultados/graficos/credito_pbi.{ext}", dpi=200, facecolor=FONDO)
print("Listo: resultados/graficos/credito_pbi.png")
