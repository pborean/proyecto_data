"""
16_mapa_calor_edad.py
Mapa de calor edad x mes: cuántos puntos porcentuales subió, respecto de julio de 2024, el porcentaje de cada grupo de edad
con al menos un crédito, en (a) bancos y compañías financieras y (b) proveedores no financieros de crédito.
Fuente: BCRA, Indicadores de Inclusión Financiera, tabla 4.3.4 (Central de Deudores, sistema financiero ampliado).
Archivo: datos/crudos/bcra_deudores_sfa_grupo_institucional_rango_etario.xlsx
Se parte de julio de 2024 porque ese mes la serie cambia de nivel en todos los grupos (ver 10_prestamistas.py).
Salida: resultados/tablas/mapa_calor_edad.csv y resultados/graficos/mapa_calor_edad.png/.svg
"""
from inicio import np, pd, mpl, plt, CARPETA
import datetime as dt
import openpyxl

XLSX = CARPETA / "datos/crudos/bcra_deudores_sfa_grupo_institucional_rango_etario.xlsx"
F_INI, F_FIN = pd.Timestamp("2024-07-01"), pd.Timestamp("2025-12-01")
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
GRUPOS = [("EEFF", "Bancos y compañías financieras"), ("PNFC", "Proveedores no financieros")]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

# ---- 1. leer (hoja 4.3.4: fila 5 = encabezado con fechas; col B = grupo, col C = edad) ----
ws = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)["4.3.4"]
filas = list(ws.iter_rows(min_row=1, max_row=130, max_col=140, values_only=True))
fechas = [(j, pd.Timestamp(c)) for j, c in enumerate(filas[4]) if isinstance(c, dt.datetime)]
datos, grupo = [], None
for r in filas[5:]:
    grupo = r[1] or grupo
    if r[2] is None:
        continue
    for j, f in fechas:
        datos.append((grupo.split("/")[0].strip(), r[2].strip(), f, r[j]))
df = pd.DataFrame(datos, columns=["grupo", "edad", "fecha", "pct"])
df = df[(df.edad != "TOTAL") & (df.fecha >= F_INI) & (df.fecha <= F_FIN)]

# ---- 2. cambio en puntos porcentuales respecto de jul-2024, por edad y mes ----
mat = {}
for g, _ in GRUPOS:
    nivel = df[df.grupo == g].pivot(index="edad", columns="fecha", values="pct").sort_index(axis=1)
    mat[g] = nivel.sub(nivel[F_INI], axis=0)
edades = list(mat["EEFF"].index)
etq = [e.replace(" - ", "–") for e in edades]
salida = pd.concat({g: m.T for g, m in mat.items()}, names=["grupo", "fecha"])
salida.columns = etq
salida.round(2).to_csv(CARPETA / "resultados/tablas/mapa_calor_edad.csv", encoding="utf-8-sig")
print((mat["PNFC"][F_FIN]).round(1).to_string())

# ---- 3. gráfico: dos mapas con la misma escala de color ----
vmax = float(np.ceil(max(m.values.max() for m in mat.values())))
cmap = mpl.colormaps["YlGnBu"].copy()
fig, ejes = plt.subplots(1, 2, figsize=(13.5, 6.6), facecolor=FONDO, sharey=True)
for ax, (g, nombre) in zip(ejes, GRUPOS):
    m = mat[g]
    im = ax.imshow(m.values, aspect="auto", cmap=cmap, vmin=0, vmax=vmax, interpolation="nearest")
    ax.set_facecolor(FONDO)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks(range(len(m.columns)))
    ax.set_xticklabels([f"{MESES[f.month - 1]}-{f.strftime('%y')}" for f in m.columns], rotation=60, ha="right", fontsize=8.5, color=TINTA)
    ax.set_yticks(range(len(etq))); ax.set_yticklabels(etq, fontsize=9, color=TINTA)
    ax.tick_params(length=0, labelleft=True)      # con sharey, el eje derecho oculta las edades: se las devolvemos
    ax.grid(False)
    ax.set_title(nombre, loc="left", fontsize=12, fontweight="bold", color=TINTA)
    ax.set_ylabel("Edad", color=TINTA)
cax = fig.add_axes([0.3, 0.135, 0.4, 0.02])
cb = fig.colorbar(im, cax=cax, orientation="horizontal")
cb.set_label("Puntos porcentuales de aumento respecto de julio de 2024", color=TINTA, fontsize=9)
cb.outline.set_visible(False); cb.ax.tick_params(colors=TINTA, labelsize=8.5)
fig.suptitle("Cuándo y en qué edades subió el acceso al crédito: bancos vs. proveedores no financieros",
             x=0.01, y=0.985, ha="left", fontsize=13.5, fontweight="bold", color=TINTA)
fig.text(0.01, 0.01,
         "Fuente: BCRA, Indicadores de Inclusión Financiera, tabla 4.3.4 (Central de Deudores, sistema financiero ampliado); elaboración propia.\n"
         "Cada celda es el porcentaje de la población de esa edad con al menos un crédito en el grupo, menos el mismo porcentaje en julio de 2024. "
         "Una persona cuenta una vez por grupo; los grupos no se suman.",
         fontsize=8, color=GRIS, va="bottom")
fig.subplots_adjust(left=0.06, right=0.985, top=0.9, bottom=0.28, wspace=0.12)
for ext in ("png", "svg"):
    fig.savefig(CARPETA / f"resultados/graficos/mapa_calor_edad.{ext}", dpi=200, facecolor=FONDO)
print("Guardado.")
