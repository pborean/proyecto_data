# Contar con Datos 2026: costo real del crédito con tarjeta

¿Cuándo fue cara y cuándo barata la deuda de tarjeta de crédito frente a la inflación?
Análisis mensual de enero de 2017 a julio de 2026.

## Resultado principal

La tasa real de las tarjetas (tasa nominal descontada la inflación) pasa por cuatro regímenes,
detectados con PELT y con segmentación por mínimos cuadrados y BIC:

| Régimen | Tasa real media mensual |
|---|---|
| Hasta agosto de 2020 | +1,6% |
| Septiembre de 2020 a marzo de 2023 | −0,3% |
| Abril de 2023 a marzo de 2024 | −3,0% |
| Desde abril de 2024 | +4,6% |

En diciembre de 2023 la tasa real llegó a −12,0%: la inflación fue de 25% en el mes y la tasa
nominal de las tarjetas apenas superó el 10%.

Los tres quiebres de fecha aparecen en 5 de 5 configuraciones de PELT. La duración del tramo
más negativo depende del largo mínimo de régimen que se fije (12 meses en el análisis base;
con 6 meses el tramo se acorta a unos 8).

## Estructura

```
contar-datos-2026/
├── datos/
│   ├── crudos/          datos tal como se descargaron
│   └── procesados/      panel_mensual.csv (generado por scripts/01)
├── scripts/             código, numerado en el orden en que se corre
├── resultados/
│   ├── graficos/        grafico_2023.png, tasa_real_media.png, quiebres_r_tarjetas.png
│   └── tablas/          resumen_por_periodo.csv, puntos_de_cambio.csv
├── docs/                bases y condiciones del concurso
├── requirements.txt
└── README.md
```

## Cómo correrlo

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 scripts/01_construir_panel.py     # arma el panel a partir de los datos crudos
python3 scripts/02_analisis_basico.py     # media y desvío por período, y detalle de 2023
python3 scripts/03_tasa_real_media.py     # gráfico de la tasa real de tarjetas
python3 scripts/04_puntos_de_cambio.py    # detección de regímenes (PELT y BIC)
```

Cada script se puede correr desde cualquier carpeta. `scripts/inicio.py` concentra las
librerías, los colores, las rutas y las funciones comunes.

## Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `datos/crudos/ipc_mensual.csv` | IPC nivel general, base dic-2016 = 100 | INDEC, vía datos.gob.ar (serie 148.3_INIVELNAL_DICI_M_26) |
| `datos/crudos/tasas_interes.csv` | Tasas de interés activas (TNA %); se usa la columna de tarjetas | BCRA, vía datos.gob.ar |
| `datos/crudos/indice_salarios.csv` | Índice de salarios por sector, oct-2016 = 100 | INDEC |
| `datos/crudos/ripte.csv` | RIPTE, remuneración imponible promedio (no usado todavía) | Secretaría de Seguridad Social, vía datos.gob.ar |

## Método, en resumen

- Tasa nominal mensual: `i = (1 + TNA / (100 * 365)) ** 30 - 1`
- Tasa real (Fisher): `r = (1 + i) / (1 + pi) - 1`
- Regímenes: PELT y segmentación por mínimos cuadrados con selección por BIC
  (en el espíritu de Bai-Perron, sin los tests sup-F ni los intervalos de confianza).

## Limitaciones

- Es la tasa promedio del sistema informada al BCRA, no la de una entidad ni la de una persona.
- No incluye comisiones, seguros ni cargos.
- La conversión de TNA a tasa mensual (capitalización cada 30 días) es una convención propia.
- 115 observaciones mensuales y un único episodio de alta inflación.
- Los quiebres detectados dependen de parámetros (largo mínimo de régimen, penalización).
