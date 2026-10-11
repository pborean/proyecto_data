"""
12_mora_regional.py
Mora bancaria de Argentina frente a la región y el mundo, 2020 en adelante.
Indicador: Banco Mundial, FB.AST.NPER.ZS "Bank nonperforming loans to total gross loans (%)"
(datos del FMI, Financial Soundness Indicators; licencia CC BY 4.0). Es la mora de TODOS los préstamos
bancarios, no solo la de las familias.
Entrada: datos/crudos/bm_mora_bancaria_paises.json  (una consulta a la API del Banco Mundial, ver README)
Salida:  resultados/tablas/mora_bancaria_paises.csv y resultados/graficos/mora_regional.png/.svg
No se rellenan ni se estiman datos faltantes: si un país no tiene dato para un año, queda vacío.
"""
from inicio import np, pd, mpl, plt, CARPETA
import json

JSON = CARPETA / "datos/crudos/bm_mora_bancaria_paises.json"
DESDE = 2020
NOMBRES = {"ARG": "Argentina", "BRA": "Brasil", "CHL": "Chile", "MEX": "México", "COL": "Colombia", "URY": "Uruguay",
           "PER": "Perú", "PRY": "Paraguay", "BOL": "Bolivia", "USA": "Estados Unidos",
           "LCN": "América Latina y el Caribe", "WLD": "Mundo"}
PARES = ["BRA", "CHL", "MEX", "COL", "URY", "PER", "PRY", "BOL"]          # países de la región para la banda
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
C_ARG, C_PAR = "#2F6F7A", "#8A8680"

# ---- 1. leer la respuesta de la API (lista: [metadatos, [registros]]) ----
crudo = json.loads(JSON.read_text(encoding="utf-8"))
if not isinstance(crudo, list) or len(crudo) < 2 or crudo[1] is None:
    raise SystemExit("El archivo no tiene datos. Volvé a bajarlo (ver el comando en el README).")
reg = [(r["countryiso3code"] or r["country"]["id"], int(r["date"]), r["value"]) for r in crudo[1]]
df = pd.DataFrame(reg, columns=["iso3", "anio", "valor"]).dropna(subset=["valor"])
df = df[df.anio >= DESDE]
tabla = df.pivot(index="anio", columns="iso3", values="valor").sort_index()
tabla.columns = [NOMBRES.get(c, c) for c in tabla.columns]
tabla.round(2).to_csv(CARPETA / "resultados/tablas/mora_bancaria_paises.csv", encoding="utf-8-sig")
print("Años x países con dato (los vacíos NO se rellenan):")
print(tabla.round(1).to_string())

# ---- 2. último dato de cada país ----
ult = (df.sort_values("anio").groupby("iso3").tail(1).set_index("iso3"))
ult["nombre"] = [NOMBRES.get(i, i) for i in ult.index]
ult = ult.sort_values("valor")

# ---- 3. gráfico ----
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.6), facecolor=FONDO, gridspec_kw={"width_ratios": [1, 1.1]})
for a in (a1, a2):
    a.set_facecolor(FONDO)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRIS)
    a.tick_params(colors=TINTA); a.grid(axis="x" if a is a1 else "y", color="#E5E1D8", lw=.8); a.set_axisbelow(True)

# izquierda: último dato disponible de cada país
cols = [C_ARG if i == "ARG" else C_PAR for i in ult.index]
a1.barh(ult["nombre"], ult["valor"], color=cols)
for y, (v, an) in enumerate(zip(ult["valor"], ult["anio"])):
    a1.text(v + .08, y, f"{v:.1f}%".replace(".", ",") + f"  ({an})", va="center", fontsize=9, color=TINTA)
a1.set_xlabel("% de los préstamos bancarios en mora (último año con dato)", color=TINTA)
a1.set_title("Mora bancaria total, último dato", loc="left", color=TINTA, fontsize=12, fontweight="bold")
a1.set_xlim(0, ult["valor"].max() * 1.3)

# derecha: Argentina contra el rango de los países de la región
pares = [NOMBRES[i] for i in PARES if NOMBRES[i] in tabla.columns]
if "Argentina" in tabla.columns and pares:
    banda = tabla[pares]
    a2.fill_between(tabla.index, banda.min(axis=1), banda.max(axis=1), color="#E1DDD3", label=f"Rango de {len(pares)} países de la región")
    a2.plot(tabla.index, banda.median(axis=1), color=C_PAR, lw=2, label="Mediana de esos países")
    a2.plot(tabla.index, tabla["Argentina"], color=C_ARG, lw=2.6, marker="o", label="Argentina")
    a2.set_xticks(tabla.index)
a2.set_ylabel("% de los préstamos bancarios en mora", color=TINTA)
a2.set_title("Argentina frente a la región", loc="left", color=TINTA, fontsize=12, fontweight="bold")
a2.set_ylim(0, max(tabla.max().max() * 1.35, 1)); a2.legend(frameon=False, loc="upper left")   # deja lugar a la leyenda
fig.text(0.01, 0.012, "Fuente: Banco Mundial, indicador FB.AST.NPER.ZS, con datos del FMI (Financial Soundness Indicators), licencia CC BY 4.0. Elaboración propia.\n"
         "Es la mora de todos los préstamos bancarios (no solo familias). Los años sin dato quedan vacíos; no se estiman.", fontsize=8, color=GRIS, va="bottom")
fig.tight_layout(rect=(0, .07, 1, 1))
for ext in ("png", "svg"):
    fig.savefig(CARPETA / f"resultados/graficos/mora_regional.{ext}", dpi=200, facecolor=FONDO)
print("Guardado.")
