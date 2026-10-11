"""
11_mora_por_producto.py
Mora (cartera irregular / cartera total) de las familias en tarjetas de crédito y préstamos personales,
mes a mes, junto a la tasa real de tarjetas, con los regímenes marcados (desde septiembre de 2020).
Fuente de la mora: BCRA, Anexo estadístico del Informe sobre Bancos, hoja "Calidad de Cartera (por líneas)",
bloque "2. Familias - Total", "Ratio de irregularidad" (sistema financiero, en porcentaje).
Archivo: datos/crudos/bcra_informe_bancos_anexo.xlsx
Tasa real: datos/procesados/panel_mensual.csv (scripts 01 a 05).
Cartera irregular = situaciones 3, 4, 5 y 6; familias = personas humanas sin destino comercial (hoja "Metodología y Referencias" del mismo archivo).
Salida: resultados/tablas/mora_por_producto.csv, mora_por_regimen.csv y resultados/graficos/mora_por_producto.png/.svg
"""
from inicio import np, pd, mpl, plt, cargar_panel, CARPETA
import datetime as dt
import openpyxl

XLSX = CARPETA / "datos/crudos/bcra_informe_bancos_anexo.xlsx"
INICIO = "2020-09"                                  # igual que 06_grafico_regimenes.py: no se grafica nada anterior
QUIEBRES = ["2023-08", "2024-04"]                   # cortes dentro del período (el de 2020-09 es el inicio)
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
C_TARJ, C_PERS, C_REAL = "#2F6F7A", "#C07F12", "#B3261E"

# ---- 1. leer el bloque "2. Familias - Total" / "Ratio de irregularidad" ----
ws = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)["Calidad de Cartera (por líneas)"]
filas = list(ws.iter_rows(min_row=1, max_row=150, max_col=210, values_only=True))
ini = next(i for i, r in enumerate(filas) if r[0] and str(r[0]).startswith("2. Familias - Total"))
enc = next(i for i in range(ini, ini + 8) if any(isinstance(c, dt.datetime) for c in filas[i]))
fechas = [(j, pd.Timestamp(c)) for j, c in enumerate(filas[enc]) if isinstance(c, dt.datetime)]
bloque = {}
for r in filas[enc + 1: enc + 8]:
    if r[0] is None or str(r[0]).startswith("Fuente"):
        break
    bloque[str(r[0]).strip()] = pd.Series({f: float(r[j]) for j, f in fechas if r[j] is not None})
mora = pd.DataFrame(bloque).rename(columns={"Cartera irregular total": "Total familias"})
mora.index.name = "fecha"
mora = mora.loc[INICIO:]
mora.round(3).to_csv(CARPETA / "resultados/tablas/mora_por_producto.csv", encoding="utf-8-sig")
print(mora[["Total familias", "Tarjetas de crédito", "Personales"]].tail(3).round(2))

panel = cargar_panel()
r_tarj = panel["r_tarjetas"] * 100
# los dos están en meses; se alinea por mes
r_tarj.index = pd.to_datetime(r_tarj.index)

# ---- 2. tabla por régimen ----
cortes = [pd.Timestamp(q) for q in QUIEBRES]
lim = [mora.index[0]] + cortes + [mora.index[-1] + pd.offsets.MonthBegin(1)]
nombres = ["Sep-2020 a jul-2023", "Ago-2023 a mar-2024", "Abr-2024 a jul-2026"]
filas_t = []
for k in range(3):
    m = mora[(mora.index >= lim[k]) & (mora.index < lim[k + 1])]
    rr = r_tarj[(r_tarj.index >= lim[k]) & (r_tarj.index < lim[k + 1])]
    filas_t.append({"régimen": nombres[k], "tasa_real_media_%_mes": rr.mean(),
                    "mora_tarjetas_inicio": m["Tarjetas de crédito"].iloc[0], "mora_tarjetas_fin": m["Tarjetas de crédito"].iloc[-1],
                    "mora_personales_inicio": m["Personales"].iloc[0], "mora_personales_fin": m["Personales"].iloc[-1]})
tabla = pd.DataFrame(filas_t).set_index("régimen")
tabla.round(2).to_csv(CARPETA / "resultados/tablas/mora_por_regimen.csv", encoding="utf-8-sig")
print(tabla.round(2).to_string())

# ---- 3. gráfico: arriba tasa real, abajo mora (mismo eje de tiempo) ----
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 8), facecolor=FONDO, sharex=True, gridspec_kw={"height_ratios": [1, 1.25]})
sombras = ["#F0EDE5", "#EFE3E1", "#E3EEF0"]
for a in (a1, a2):
    a.set_facecolor(FONDO)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRIS)
    a.tick_params(colors=TINTA); a.grid(axis="y", color="#E5E1D8", lw=.8); a.set_axisbelow(True)
    for k in range(3):
        a.axvspan(lim[k], lim[k + 1], color=sombras[k], zorder=0)
    for c in cortes:
        a.axvline(c, color=GRIS, ls=":", lw=1)

a1.axhline(0, color=GRIS, lw=1)
a1.plot(r_tarj.index, r_tarj, color=C_REAL, lw=1.8)
a1.set_ylabel("Tasa real de tarjetas\n(% mensual)", color=TINTA)
a1.set_title("La mora de las familias se disparó después de que la tasa real pasó a ser alta", loc="left", color=TINTA, fontsize=13, fontweight="bold")
for k in range(3):
    mid = lim[k] + (lim[k + 1] - lim[k]) / 2
    a1.text(mid, a1.get_ylim()[1], f"media {tabla['tasa_real_media_%_mes'].iloc[k]:+.1f}%".replace(".", ",").replace("-", "−"), ha="center", va="top", fontsize=8.5, color=GRIS, bbox=dict(facecolor=FONDO, edgecolor="none", pad=1.5, alpha=.85))

a2.plot(mora.index, mora["Tarjetas de crédito"], color=C_TARJ, lw=2.2, label="Tarjetas de crédito")
a2.plot(mora.index, mora["Personales"], color=C_PERS, lw=2.2, label="Préstamos personales")
for col, c in (("Tarjetas de crédito", C_TARJ), ("Personales", C_PERS)):
    a2.text(mora.index[-1] + pd.Timedelta(days=15), mora[col].iloc[-1], f"{mora[col].iloc[-1]:.1f}%".replace(".", ","), color=TINTA, va="center", fontsize=9)
a2.set_ylabel("Mora de las familias\n(% de la cartera)", color=TINTA)
a2.legend(frameon=False, loc="upper left")
a2.set_xlim(mora.index[0], mora.index[-1] + pd.Timedelta(days=120))
fig.text(0.01, 0.008, "Fuente: BCRA, Anexo estadístico del Informe sobre Bancos (cartera irregular de familias sobre cartera total, sistema financiero) e INDEC / BCRA (tasa real, elaboración propia).\n"
         "Mora = cartera irregular (situaciones 3 a 6) sobre financiaciones totales; familias = personas humanas sin destino comercial. Solo entidades financieras.",
         fontsize=8, color=GRIS, va="bottom")
fig.tight_layout(rect=(0, .045, 1, 1))
for ext in ("png", "svg"):
    fig.savefig(CARPETA / f"resultados/graficos/mora_por_producto.{ext}", dpi=200, facecolor=FONDO)
print("Guardado.")
