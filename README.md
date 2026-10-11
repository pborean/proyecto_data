# Contar con Datos 2026: costo real del crédito con tarjeta

¿Cuándo fue cara y cuándo barata la deuda de tarjeta de crédito frente a la inflación?
Análisis mensual de enero de 2017 a julio de 2026, más un análisis de quién se endeuda.

## Resultado principal

La tasa real de las tarjetas (tasa nominal descontada la inflación) pasa por cuatro regímenes,
detectados con PELT y con segmentación por mínimos cuadrados y BIC (largo mínimo de régimen: 6 meses):

| Régimen | Meses | Tasa real media mensual | Inflación media mensual |
|---|---|---|---|
| Enero de 2017 a agosto de 2020 | 44 | +1,6% | 2,8% |
| Septiembre de 2020 a julio de 2023 | 35 | −0,3% | 4,9% |
| Agosto de 2023 a marzo de 2024 | 8 | −4,4% | 14,6% |
| Abril de 2024 a julio de 2026 | 28 | +4,6% | 3,0% |

El detalle está en `resultados/tablas/inflacion_por_regimen.csv`. En diciembre de 2023 la tasa
real llegó a −12,0%: la inflación fue de 25% en el mes y la tasa nominal apenas superó el 10%.

**Robustez de las fechas.** Septiembre de 2020 y abril de 2024 aparecen en todas las configuraciones
probadas. El corte de 2023 se mueve entre julio y agosto según el largo mínimo de régimen (con 6 u 8
meses sale agosto; con 12 meses sale abril de 2023). Un posible corte en diciembre de 2018 aparece solo
con penalizaciones bajas y no se usa.

## Quién se endeuda

- Por edad: `scripts/08_deuda_por_edad.py` (BCRA, Central de Deudores). Compara diciembre de 2024 con
  diciembre de 2025 porque en julio de 2024 cambió el umbral de la Central de Deudores.

## Estructura

```
contar-datos-2026/
├── datos/
│   ├── crudos/          datos tal como se descargaron
│   └── procesados/      panel_mensual.csv (generado por scripts/01)
├── scripts/             código, numerado en el orden en que se corre
├── resultados/
│   ├── graficos/        regimenes_tarjetas, deuda_por_edad, tasa_real_media, quiebres_r_tarjetas, etc.
│   └── tablas/          inflacion_por_regimen.csv, puntos_de_cambio.csv, deuda_por_edad.csv, etc.
├── docs/                bases del concurso
├── requirements.txt
└── README.md
```

## Cómo correrlo

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 scripts/01_construir_panel.py          # arma el panel a partir de los datos crudos
python3 scripts/02_analisis_basico.py          # media y desvío por período, y detalle de 2023
python3 scripts/03_tasa_real_media.py          # gráfico de la tasa real de tarjetas
python3 scripts/04_puntos_de_cambio.py         # detección de regímenes (PELT y BIC)
python3 scripts/05_inflacion_por_regimen.py    # inflación y tasa real por régimen
python3 scripts/06_grafico_regimenes.py        # gráfico de regímenes (PNG y SVG)
python3 scripts/08_deuda_por_edad.py           # deuda por edad (BCRA)
```

`scripts/inicio.py` concentra las librerías, los colores, las rutas y las funciones comunes.

## Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `datos/crudos/ipc_mensual.csv` | IPC nivel general, base dic-2016 = 100 | INDEC, vía datos.gob.ar (serie 148.3_INIVELNAL_DICI_M_26) |
| `datos/crudos/tasas_interes.csv` | Tasas de interés activas (TNA %); se usa la columna de tarjetas | BCRA, vía datos.gob.ar |
| `datos/crudos/indice_salarios.csv` | Índice de salarios por sector, oct-2016 = 100 | INDEC |
| `datos/crudos/ripte.csv` | RIPTE, remuneración imponible promedio (no usado todavía) | Secretaría de Seguridad Social, vía datos.gob.ar |
| `datos/crudos/bcra_deudores_sfa_asistencia_rango_etario.xlsx` | Porcentaje de cada edad con al menos un crédito, por producto | BCRA, Indicadores de Inclusión Financiera, tabla 4.2.3 |

## Método, en resumen

- Tasa nominal mensual: `i = (1 + TNA / (100 * 365)) ** 30 - 1`
- Tasa real (Fisher): `r = (1 + i) / (1 + pi) - 1`
- Regímenes: PELT y segmentación por mínimos cuadrados con selección por BIC
  (en el espíritu de Bai-Perron, sin los tests sup-F ni los intervalos de confianza).
- En el gráfico de regímenes la curva está suavizada (media móvil de 5 meses); los números
  grandes salen de los datos mensuales sin suavizar.

## Limitaciones

- Es la tasa promedio del sistema informada al BCRA, no la de una entidad ni la de una persona.
- No incluye comisiones, seguros ni cargos.
- La conversión de TNA a tasa mensual (capitalización cada 30 días) es una convención propia.
- 115 observaciones mensuales y un único episodio de alta inflación.
- Los quiebres detectados dependen de parámetros (largo mínimo de régimen, penalización).
- La serie de tarjetas cubre entidades financieras reguladas; los proveedores no bancarios no entran.
