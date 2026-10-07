"""
puntos_de_cambio.py: detecta quiebres en la tasa real de endeudamiento.

Dos métodos, ambos sobre el CAMBIO EN EL NIVEL MEDIO de la serie:

  1) PELT (librería ruptures). Se prueba con varias "penalizaciones": cuanto mayor
     es la penalización, menos quiebres detecta. Si una fecha aparece con muchas
     penalizaciones distintas, es robusta.

  2) Segmentación óptima por mínimos cuadrados + criterio BIC, en el espíritu de
     Bai-Perron: para cada cantidad k de quiebres (0, 1, 2, ...) busca las fechas que
     minimizan la suma de cuadrados, y elige k con el menor BIC.
     OJO: es la versión "mínimos cuadrados + BIC". No incluye los tests sup-F ni los
     intervalos de confianza del Bai-Perron completo (para eso existe el paquete
     `strucchange` de R). Hay que decirlo así en la metodología.

Uso:
    pip install ruptures
    python3 puntos_de_cambio.py
"""
from inicio import np, pd, plt, cargar_panel, ruta_grafico, ruta_tabla
import ruptures as rpt

# ---------------- Parámetros que podés tocar ----------------
SERIES = ["r_tarjetas"]   # series a analizar
MIN_TAMANO = 12          # un régimen dura al menos 12 meses
MAX_QUIEBRES = 4         # máximo de quiebres que prueba el método 2
PENALIZACIONES = [1, 2, 3, 5, 8]   # multiplicadores de la penalización de PELT (método 1)
TOLERANCIA = 3           # meses de margen para decir que "dos fechas son la misma"
# ------------------------------------------------------------

df = cargar_panel()


def a_fechas(indices, indice_temporal):
    """ruptures devuelve la posición donde TERMINA cada tramo; la última es el largo total.
    La fecha de un quiebre es el primer mes del régimen nuevo."""
    return [indice_temporal[i] for i in indices if i < len(indice_temporal)]


def ssr_por_tramos(x, quiebres):
    """Suma de cuadrados de los residuos si cada tramo se ajusta con su propia media."""
    limites = [0] + list(quiebres)
    total = 0.0
    for a, b in zip(limites[:-1], limites[1:]):
        tramo = x[a:b]
        total += ((tramo - tramo.mean()) ** 2).sum()
    return total


# ---------------- Método 1: PELT con distintas penalizaciones ----------------
def metodo_pelt(x, indice_temporal):
    n = len(x)
    # Varianza del ruido, estimada con las diferencias entre meses consecutivos
    # (no se contamina con los cambios de nivel)
    sigma2 = np.var(np.diff(x)) / 2
    algo = rpt.Pelt(model="l2", min_size=MIN_TAMANO, jump=1).fit(x)
    resultados = {}
    for c in PENALIZACIONES:
        pen = c * sigma2 * np.log(n)           # penalización estilo BIC
        quiebres = algo.predict(pen=pen)[:-1]  # el último elemento es el largo total
        resultados[c] = a_fechas(quiebres, indice_temporal)
    return resultados


# ---------------- Método 2: segmentación óptima + BIC ----------------
def metodo_bic(x, indice_temporal):
    n = len(x)
    algo = rpt.Dynp(model="l2", min_size=MIN_TAMANO, jump=1).fit(x)
    filas = []
    mejor = None
    for k in range(0, MAX_QUIEBRES + 1):
        quiebres = [] if k == 0 else algo.predict(n_bkps=k)[:-1]
        ssr = ssr_por_tramos(x, quiebres + [n])
        # BIC al estilo Bai-Perron: log(SSR/n) + (cantidad de parámetros) * log(n) / n
        # parámetros = (k+1) medias + k fechas de quiebre = 2k + 1
        bic = np.log(ssr / n) + (2 * k + 1) * np.log(n) / n
        filas.append({"k": k, "SSR": ssr, "BIC": bic, "quiebres": a_fechas(quiebres, indice_temporal)})
        if mejor is None or bic < mejor["BIC"]:
            mejor = filas[-1]
    return mejor, pd.DataFrame(filas)


# ---------------- Ejecutar y mostrar ----------------
def fmt(fechas):
    return ", ".join(f.strftime("%Y-%m") for f in fechas) if fechas else "(sin quiebres)"


resumen = []
for nombre in SERIES:
    x = (df[nombre] * 100).values
    idx = df.index
    print("=" * 70)
    print(f"Serie: {nombre}  ({len(x)} meses)")
    print("=" * 70)

    # Método 1
    pelt = metodo_pelt(x, idx)
    print("\n[Método 1] PELT, por penalización (más alta = más exigente):")
    for c, fechas in pelt.items():
        print(f"   penalización x{c}: {fmt(fechas)}")

    # Qué tan robusta es cada fecha: en cuántas penalizaciones aparece (±TOLERANCIA meses)
    todas = sorted({f for fechas in pelt.values() for f in fechas})
    print("\n   Robustez de cada fecha (en cuántas de las %d configuraciones aparece):" % len(PENALIZACIONES))
    agrupadas = []
    for f in todas:
        if agrupadas and (f - agrupadas[-1][0]).days <= 31 * TOLERANCIA:
            agrupadas[-1].append(f)
        else:
            agrupadas.append([f])
    for grupo in agrupadas:
        centro = grupo[len(grupo) // 2]
        cuantas = sum(
            any(abs((f - centro).days) <= 31 * TOLERANCIA for f in fechas)
            for fechas in pelt.values()
        )
        print(f"   ~{centro.strftime('%Y-%m')}: {cuantas}/{len(PENALIZACIONES)}")
        resumen.append({"serie": nombre, "metodo": "PELT", "fecha": centro.strftime("%Y-%m"),
                        "robustez": f"{cuantas}/{len(PENALIZACIONES)}"})

    # Método 2
    mejor, tabla = metodo_bic(x, idx)
    print("\n[Método 2] Segmentación óptima + BIC:")
    for _, fila in tabla.iterrows():
        marca = "  <-- elegido" if fila["k"] == mejor["k"] else ""
        print(f"   k={int(fila['k'])} quiebres: BIC={fila['BIC']:.3f}  {fmt(fila['quiebres'])}{marca}")
    for f in mejor["quiebres"]:
        resumen.append({"serie": nombre, "metodo": "BIC", "fecha": f.strftime("%Y-%m"), "robustez": ""})

    # Medias de cada régimen elegido por BIC
    limites = [0] + [idx.get_loc(f) for f in mejor["quiebres"]] + [len(x)]
    print("\n   Régimen (según BIC) y tasa real media mensual:")
    for a, b in zip(limites[:-1], limites[1:]):
        print(f"   {idx[a].strftime('%Y-%m')} a {idx[b-1].strftime('%Y-%m')}: media {x[a:b].mean():+.2f}%  ({b-a} meses)")

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(idx, x, color="#2a6fbb", linewidth=1.2, alpha=0.6, label="Tasa real mensual")
    for a, b in zip(limites[:-1], limites[1:]):
        ax.hlines(x[a:b].mean(), idx[a], idx[b - 1], color="#d9731a", linewidth=2.6)
    for f in mejor["quiebres"]:
        ax.axvline(f, color="black", linestyle="--", linewidth=0.9)
        ax.text(f, ax.get_ylim()[1], " " + f.strftime("%Y-%m"), va="top", fontsize=8.5)
    ax.axhline(0, color="black", linewidth=0.7)
    ax.set_ylabel("% por mes")
    ax.set_title(f"{nombre}: regímenes detectados (naranja = media del régimen)", fontsize=10.5, loc="left")
    plt.tight_layout()
    plt.savefig(ruta_grafico(f"quiebres_{nombre}.png"), dpi=150)
    plt.close(fig)

pd.DataFrame(resumen).to_csv(ruta_tabla("puntos_de_cambio.csv"), index=False, encoding="utf-8-sig")
print("\nGuardado: puntos_de_cambio.csv y un gráfico por serie (quiebres_<serie>.png)")
