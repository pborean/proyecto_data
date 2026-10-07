"""
01_construir_panel.py: arma el panel mensual a partir de los datos crudos.

Entradas (datos/crudos/):
    ipc_mensual.csv       IPC nivel general, base dic-2016 = 100 (INDEC)
    tasas_interes.csv     tasas de interés activas, TNA % (BCRA)
    indice_salarios.csv   índice de salarios por sector, oct-2016 = 100 (INDEC)

Salida:
    datos/procesados/panel_mensual.csv   (enero 2017 a julio 2026, 115 meses)

Columnas del panel:
    pi             inflación mensual
    i_personales, i_tarjetas   tasa nominal mensual efectiva
    w_priv_reg, w_publico, w_no_reg   aumento nominal del salario
    r_personales, r_tarjetas   tasa REAL mensual  (Fisher)
    g_priv_reg, g_publico, g_no_reg   crecimiento REAL del salario

Uso:  python3 scripts/01_construir_panel.py
"""
from inicio import pd, ruta_datos

# --- Inflación mensual ---
ipc = pd.read_csv(ruta_datos("ipc_mensual.csv"), parse_dates=["indice_tiempo"]).set_index("indice_tiempo").iloc[:, 0]
pi = ipc.pct_change().dropna().rename("pi")

# --- Tasas: de TNA (%) a tasa mensual efectiva ---
tas = pd.read_csv(ruta_datos("tasas_interes.csv"), parse_dates=["indice_tiempo"]).set_index("indice_tiempo")
tna = tas[["tasas_interes_activas_personales", "tasas_interes_activas_tarjetas"]].copy()
tna.columns = ["personales", "tarjetas"]
i_m = (1 + tna / (100 * 365)) ** 30 - 1

# --- Salarios: el CSV usa ';' de separador, ',' decimal y fechas d/m/aaaa ---
IS = pd.read_csv(ruta_datos("indice_salarios.csv"), sep=";", decimal=",", na_values="NA")
IS["periodo"] = pd.to_datetime(IS["periodo"], format="%d/%m/%Y")
IS = IS.set_index("periodo")[["IS_sector_privado_registrado", "IS_sector_publico", "IS_sector_no_registrado"]]
IS.columns = ["priv_reg", "publico", "no_reg"]
dIS = IS.pct_change()

# --- Unir por mes y calcular tasas reales (Fisher) ---
df = pd.concat([pi, i_m.add_prefix("i_"), dIS.add_prefix("w_")], axis=1, sort=True).loc["2017-01-01":"2026-07-01"].dropna()
for p in ["personales", "tarjetas"]:
    df[f"r_{p}"] = (1 + df[f"i_{p}"]) / (1 + df["pi"]) - 1
for s in ["priv_reg", "publico", "no_reg"]:
    df[f"g_{s}"] = (1 + df[f"w_{s}"]) / (1 + df["pi"]) - 1

salida = ruta_datos("panel_mensual.csv", crudo=False)
df.to_csv(salida)
print(f"Panel guardado en {salida}")
print(df.shape, df.index.min().date(), "a", df.index.max().date())
