"""
inicio.py: punto de entrada común del proyecto.

Al principio de cualquier script alcanza con:

    from inicio import *

o importar solo lo que necesites:

    from inicio import np, pd, plt, cargar_panel, COLS, COLORES

Qué trae:
  Librerías ....... np (numpy), pd (pandas), plt (matplotlib.pyplot), mpl, FuncFormatter, PercentFormatter
  Estadística ..... adfuller (test ADF), sm (statsmodels.api), stats (scipy.stats), rpt (ruptures)
  Datos ........... cargar_panel(), ruta_datos(), ruta_grafico(), ruta_tabla(), COLS, SEGMENTOS
  Nombres/colores . NOMBRES, COLORES (los mismos en todos los gráficos)
  Funciones ....... acumular_indice(), acumulado_pct(), adf_pvalor()

Las librerías de estadística son opcionales: si alguna no está instalada, queda en None
y te avisa cuál falta, sin romper el resto. Se instalan todas con:
    pip install -r requirements.txt
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter

# ---------------- Librerías opcionales (estadística) ----------------
_faltan = []

try:
    from statsmodels.tsa.stattools import adfuller
    import statsmodels.api as sm
except ImportError:
    adfuller, sm = None, None
    _faltan.append("statsmodels")

try:
    from scipy import stats
except ImportError:
    stats = None
    _faltan.append("scipy")

try:
    import ruptures as rpt
except ImportError:
    rpt = None
    _faltan.append("ruptures")

if _faltan:
    print("Aviso: faltan librerías opcionales:", ", ".join(_faltan),
          "-> instalalas con: pip install " + " ".join(_faltan))

# ---------------- Carpeta y reproducibilidad ----------------
# Este archivo vive en scripts/, así que la raíz del proyecto es una carpeta más arriba
CARPETA = Path(__file__).resolve().parent.parent
DATOS_CRUDOS = CARPETA / "datos" / "crudos"
DATOS_PROC = CARPETA / "datos" / "procesados"
GRAFICOS = CARPETA / "resultados" / "graficos"
TABLAS = CARPETA / "resultados" / "tablas"
for _d in (DATOS_CRUDOS, DATOS_PROC, GRAFICOS, TABLAS):
    _d.mkdir(parents=True, exist_ok=True)

SEMILLA = 42
np.random.seed(SEMILLA)

# ---------------- Estilo de gráficos ----------------
plt.rcParams.update({
    "figure.figsize": (9, 5),
    "figure.dpi": 100,
    "savefig.dpi": 150,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})

# ---------------- Variables del análisis ----------------
COLS = ["r_personales", "r_tarjetas", "g_priv_reg", "g_publico", "g_no_reg"]
SEGMENTOS = ["priv_reg", "publico", "no_reg"]

NOMBRES = {
    "r_personales": "Préstamos personales",
    "r_tarjetas":   "Tarjetas de crédito",
    "g_priv_reg":   "Salario privado registrado",
    "g_publico":    "Salario público",
    "g_no_reg":     "Salario no registrado",
}

# Colores validados para daltonismo; los mismos en todos los gráficos
COLORES = {
    "r_personales": "#2a6fbb",
    "r_tarjetas":   "#d9731a",
    "g_priv_reg":   "#1f9a74",
    "g_publico":    "#8a4fb5",
    "g_no_reg":     "#b8860b",
}


# ---------------- Funciones ----------------
def cargar_panel():
    """Lee datos/procesados/panel_mensual.csv con las fechas como índice."""
    return pd.read_csv(DATOS_PROC / "panel_mensual.csv", index_col=0, parse_dates=True)


def ruta_datos(nombre, crudo=True):
    """Ruta de un archivo en datos/crudos (o datos/procesados si crudo=False)."""
    return (DATOS_CRUDOS if crudo else DATOS_PROC) / nombre


def ruta_grafico(nombre):
    """Ruta donde guardar un gráfico (resultados/graficos/)."""
    return GRAFICOS / nombre


def ruta_tabla(nombre):
    """Ruta donde guardar una tabla (resultados/tablas/)."""
    return TABLAS / nombre


def acumular_indice(serie, base=100.0):
    """Índice acumulado: base * (1+x1)(1+x2)... Agrega una fila inicial igual a la base."""
    inicio = serie.index[0] - pd.offsets.MonthBegin(1)
    acumulado = base * (1 + serie).cumprod()
    return pd.concat([pd.Series([base], index=[inicio]), acumulado])


def acumulado_pct(serie):
    """Variación acumulada en %: 100 * ((1+x1)(1+x2)... - 1). Arranca en 0."""
    return acumular_indice(serie, base=100.0) - 100.0


def adf_pvalor(serie):
    """p-valor del test ADF. Menor a 0,05 => la serie es estacionaria."""
    if adfuller is None:
        raise ImportError("Falta statsmodels: pip install statsmodels")
    return adfuller(serie.dropna(), autolag="AIC", result_object=False)[1]


if __name__ == "__main__":
    # Prueba rápida: python3 inicio.py
    df = cargar_panel()
    print("numpy", np.__version__, "| pandas", pd.__version__, "| matplotlib", mpl.__version__)
    for nombre, mod in [("statsmodels", sm), ("scipy", stats), ("ruptures", rpt)]:
        print(f"{nombre}:", "ok" if mod is not None else "NO instalada")
    print("Panel:", df.shape, df.index.min().date(), "a", df.index.max().date())
