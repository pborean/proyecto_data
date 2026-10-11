"""
09_eph_endeudamiento_decil.py
Qué porcentaje de los hogares recurrió al crédito en los últimos 3 meses, según el
decil de ingreso per cápita familiar. Fuente: INDEC, EPH continua, base de hogares,
trimestres 2T2024 a 1T2026 (régimen actual, desde abril de 2024).
Variables del hogar (1 = sí, 2 = no):
  V15 = pidió préstamo a bancos o financieras
  V16 = compró en cuotas o al fiado con tarjeta de crédito o libreta
  V14 = pidió préstamo a familiares o amigos
Decil: DECCFR (ingreso per cápita familiar, decil nacional). Ponderador: PONDIH.
Entrada: datos/crudos/eph/EPH_usu_*_Trim_*  (carpetas descomprimidas o zips)
Salida:  resultados/tablas/eph_endeudamiento_decil.csv, eph_endeudamiento_trimestre.csv
         resultados/graficos/eph_endeudamiento_decil.png/.svg
"""
from pathlib import Path
import io, re, zipfile
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_EPH = RAIZ / "datos/crudos/eph"
mpl.rcParams["svg.fonttype"] = "none"
FONDO, TINTA, GRIS = "#FAF8F3", "#2B2B2B", "#8A8680"
C_BANCO, C_CUOTAS, C_FAMILIA = "#2F6F7A", "#C07F12", "#8A8680"
VARS = {"V15": "Préstamo de banco o financiera",
        "V16": "Cuotas o fiado (tarjeta o libreta)",
        "V14": "Préstamo de familia o amigos"}

# ---- 1. leer la base de hogares de cada trimestre (zip o carpeta ya descomprimida) ----
def leer_hogar(origen):
    """Devuelve el DataFrame de hogares de un zip o de una carpeta de la EPH."""
    if origen.is_file():
        with zipfile.ZipFile(origen) as zf:
            nombre = next(n for n in zf.namelist() if "hogar" in n.lower() and n.lower().endswith(".txt"))
            fuente = io.BytesIO(zf.read(nombre))
    else:
        archivos = [f for f in origen.rglob("*.txt") if "hogar" in f.name.lower()]
        if not archivos:
            print(f"AVISO: no encuentro la base de hogares en {origen.name}"); return None
        fuente = archivos[0]
    return pd.read_csv(fuente, sep=";", encoding="latin-1", low_memory=False)

partes = []
for o in sorted(CARPETA_EPH.glob("EPH_usu_*_Trim_*")):
    if o.name.startswith(".") or (o.is_file() and o.suffix != ".zip"):
        continue
    h = leer_hogar(o)
    if h is None:
        continue
    h.columns = [c.strip().upper() for c in h.columns]
    partes.append(h[["ANO4", "TRIMESTRE", "DECCFR", "PONDIH", *VARS]].copy())
    print("leído:", o.name)
if not partes:
    raise SystemExit(f"No hay carpetas ni zips de la EPH en {CARPETA_EPH}")
h = pd.concat(partes, ignore_index=True)
for c in h.columns:
    h[c] = pd.to_numeric(h[c], errors="coerce")
h["periodo"] = h["ANO4"].astype(int).astype(str) + "-T" + h["TRIMESTRE"].astype(int).astype(str)

# solo hogares con ingreso conocido (decil 1 a 10) y ponderador positivo
h = h[h["DECCFR"].between(1, 10) & (h["PONDIH"] > 0)]

def pct_si(g, v):
    """Porcentaje ponderado de hogares con respuesta 1 entre los que contestaron 1 o 2."""
    g = g[g[v].isin([1, 2])]
    return 100 * g.loc[g[v] == 1, "PONDIH"].sum() / g["PONDIH"].sum() if len(g) else np.nan

# ---- 2. por decil (todos los trimestres juntos) y por trimestre (todos los hogares) ----
por_decil = pd.DataFrame({v: h.groupby("DECCFR").apply(lambda g, v=v: pct_si(g, v)) for v in VARS})
por_decil.index = por_decil.index.astype(int); por_decil.index.name = "decil"
por_trim = pd.DataFrame({v: h.groupby("periodo").apply(lambda g, v=v: pct_si(g, v)) for v in VARS})
por_trim["hogares_muestra"] = h.groupby("periodo").size()
por_decil.round(2).to_csv(RAIZ / "resultados/tablas/eph_endeudamiento_decil.csv", encoding="utf-8-sig")
por_trim.round(2).to_csv(RAIZ / "resultados/tablas/eph_endeudamiento_trimestre.csv", encoding="utf-8-sig")
print(por_decil.round(1)); print(por_trim.round(1))

# ---- 3. gráfico ----
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.6), facecolor=FONDO, gridspec_kw={"width_ratios": [1.5, 1]})
for a in (a1, a2):
    a.set_facecolor(FONDO)
    for s in ("top", "right"): a.spines[s].set_visible(False)
    for s in ("left", "bottom"): a.spines[s].set_color(GRIS)
    a.tick_params(colors=TINTA); a.grid(axis="y", color="#E5E1D8", lw=.8); a.set_axisbelow(True)

x = np.arange(1, 11); w = .27
for k, (v, col) in enumerate(zip(("V15", "V16", "V14"), (C_BANCO, C_CUOTAS, C_FAMILIA))):
    a1.bar(x + (k - 1) * w, por_decil[v], w, color=col, label=VARS[v])
a1.set_xticks(x); a1.set_xlabel("Decil de ingreso per cápita (1 = más pobre, 10 = más rico)", color=TINTA)
a1.set_ylabel("% de los hogares", color=TINTA)
a1.set_title(f"Quién recurre al crédito, por decil ({h['periodo'].min()} a {h['periodo'].max()})",
             loc="left", color=TINTA, fontsize=12, fontweight="bold")
a1.legend(frameon=False, loc="upper left")

t = por_trim.index
for v, col in zip(("V15", "V16", "V14"), (C_BANCO, C_CUOTAS, C_FAMILIA)):
    a2.plot(t, por_trim[v], marker="o", color=col, lw=2)
    a2.text(len(t) - 1 + .1, por_trim[v].iloc[-1], f" {por_trim[v].iloc[-1]:.0f}%", color=TINTA, va="center", fontsize=9)
a2.set_title("Todos los hogares, por trimestre", loc="left", color=TINTA, fontsize=12, fontweight="bold")
a2.tick_params(axis="x", rotation=45); a2.set_ylim(bottom=0)
fig.text(0.01, 0.01, "Fuente: INDEC, EPH continua, base de hogares (preguntas V14, V15 y V16: últimos 3 meses). "
         "Elaboración propia con ponderador PONDIH.", fontsize=8, color=GRIS)
fig.tight_layout(rect=(0, .04, 1, 1))
for ext in ("png", "svg"):
    fig.savefig(RAIZ / f"resultados/graficos/eph_endeudamiento_decil.{ext}", dpi=200, facecolor=FONDO)
print("Guardado.")
