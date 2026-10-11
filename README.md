# Contar con Datos 2026: costo real del crédito con tarjeta

¿Cuándo fue cara y cuándo barata la deuda de tarjeta de crédito frente a la inflación?
Análisis mensual de enero de 2017 a julio de 2026, más un análisis de quién se endeuda
en el régimen actual (desde abril de 2024).

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

## Quién se endeuda (régimen actual)

**Por edad** (`scripts/08_deuda_por_edad.py`). Porcentaje de cada grupo de edad con al menos un crédito,
por tipo de producto (tarjetas y préstamos personales). Se compara diciembre de 2024 con diciembre de 2025
porque en julio de 2024 cambió el umbral de la Central de Deudores. Fuente: BCRA, Indicadores de Inclusión
Financiera, sección 4.2.

**Por nivel de ingreso** (`scripts/09_eph_endeudamiento_decil.py`). Porcentaje de hogares que, en los últimos
tres meses, pidieron un préstamo a un banco o financiera (V15), compraron en cuotas o al fiado con tarjeta o libreta
(V16) o pidieron un préstamo a familiares o amigos (V14), según el decil de ingreso per cápita familiar.
Trimestres 2T2024 a 1T2026 (el 1T2024 aparece como referencia en el gráfico por trimestre).
Estratos según INDEC: bajo = deciles 1 a 4, medio = 5 a 8, alto = 9 y 10.

- Cuotas o fiado con tarjeta o libreta: sube con el ingreso, de 36% en el decil 1 a 65% en el decil 10.
- Préstamo de familia o amigos: baja con el ingreso, de 31% en el decil 1 a 7% en el decil 10.
- Préstamo de banco o financiera: entre 10% y 16% en todos los deciles; el más bajo es el decil 10.
- En todos los hogares, el préstamo bancario pasa de 12,5% (1T2024) a 16,4% (4T2025) y 15,6% (1T2026).

La EPH registra si el hogar recurrió a cada fuente, no cuánto debe ni si está en mora. El 31,6% de los hogares
(ponderados) no tiene decil de ingreso porque no declaró ingresos y queda afuera de este análisis.
Tablas: `resultados/tablas/eph_endeudamiento_decil.csv` y `eph_endeudamiento_trimestre.csv`.

## Estructura

```
contar-datos-2026/
├── datos/
│   ├── crudos/          datos tal como se descargaron (la EPH no se sube al repo, ver más abajo)
│   └── procesados/      panel_mensual.csv (generado por scripts/01)
├── scripts/             código, numerado en el orden en que se corre
├── resultados/
│   ├── graficos/        regimenes_tarjetas, deuda_por_edad, eph_endeudamiento_decil, etc.
│   └── tablas/          inflacion_por_regimen.csv, puntos_de_cambio.csv, deuda_por_edad.csv,
│                        eph_endeudamiento_decil.csv, eph_endeudamiento_trimestre.csv, etc.
├── docs/                bases del concurso
├── requirements.txt
└── README.md
```

## Cómo correrlo

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 scripts/01_construir_panel.py            # arma el panel a partir de los datos crudos
python3 scripts/02_analisis_basico.py            # media y desvío por período, y detalle de 2023
python3 scripts/03_tasa_real_media.py            # gráfico de la tasa real de tarjetas
python3 scripts/04_puntos_de_cambio.py           # detección de regímenes (PELT y BIC)
python3 scripts/05_inflacion_por_regimen.py      # inflación y tasa real por régimen
python3 scripts/06_grafico_regimenes.py          # gráfico de regímenes (PNG y SVG)
python3 scripts/08_deuda_por_edad.py             # deuda por edad (BCRA)
python3 scripts/09_eph_endeudamiento_decil.py    # endeudamiento por decil de ingreso (EPH)
```

La numeración salta del 06 al 08: no hay script 07.
`scripts/inicio.py` concentra las librerías, los colores, las rutas y las funciones comunes.

## Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `datos/crudos/ipc_mensual.csv` | IPC nivel general, base dic-2016 = 100 | INDEC, vía datos.gob.ar (serie 148.3_INIVELNAL_DICI_M_26) |
| `datos/crudos/tasas_interes.csv` | Tasas de interés activas (TNA %); se usa la columna de tarjetas | BCRA, vía datos.gob.ar |
| `datos/crudos/indice_salarios.csv` | Índice de salarios por sector, oct-2016 = 100 | INDEC |
| `datos/crudos/ripte.csv` | RIPTE, remuneración imponible promedio (no usado todavía) | Secretaría de Seguridad Social, vía datos.gob.ar |
| `datos/crudos/bcra_deudores_sfa_asistencia_rango_etario.xlsx` | Porcentaje de cada edad con al menos un crédito, por producto | BCRA, Indicadores de Inclusión Financiera, tabla 4.2 (https://www.bcra.gob.ar/en/indicators-financial-inclusion/) |
| `datos/crudos/eph/EPH_usu_*_Trim_*_txt/` | EPH continua, base de hogares, 1T2024 a 1T2026 (no se sube al repo por su tamaño) | INDEC, Bases de datos: https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos |

### Cómo conseguir la EPH

1. Entrar a https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos y bajar, en formato txt,
   la base individual y hogar de los trimestres 1T2024 a 1T2026 (nueve archivos `EPH_usu_{trimestre}_Trim_{año}_txt.zip`,
   publicados en https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/).
2. Descomprimir cada uno en su propia carpeta dentro de `datos/crudos/eph/`. El script busca el archivo `usu_hogar_*.txt`
   dentro de cada carpeta.
3. Descargado el 10 de octubre de 2026. El INDEC reemplazó el archivo del 4T2024 el 7 de mayo de 2025: se usa la versión vigente.

Documentación de referencia:
- Diseño de registro y estructura de la EPH, 1T2026 (variables V14, V15, V16, PONDERA, DECCFR):
  https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_registro_1T2026.pdf
- INDEC, "Evolución de la distribución del ingreso (EPH)", segundo trimestre de 2026, Informes técnicos, vol. 10, n.º 243,
  1 de octubre de 2026 (definición de estratos por decil).

## Método, en resumen

- Tasa nominal mensual: `i = (1 + TNA / (100 * 365)) ** 30 - 1`
- Tasa real (Fisher): `r = (1 + i) / (1 + pi) - 1`
- Regímenes: PELT y segmentación por mínimos cuadrados con selección por BIC
  (en el espíritu de Bai-Perron, sin los tests sup-F ni los intervalos de confianza).
- En el gráfico de regímenes la curva está suavizada (media móvil de 5 meses); los números
  grandes salen de los datos mensuales sin suavizar.
- EPH: porcentaje ponderado de hogares con respuesta "sí" entre los que contestaron sí o no. Ponderador `PONDERA`
  (según el diseño de registro, `PONDIH` se usa solo para ingresos). Decil: `DECCFR`, decil nacional del ingreso per cápita familiar.

## Limitaciones

- Es la tasa promedio del sistema informada al BCRA, no la de una entidad ni la de una persona.
- No incluye comisiones, seguros ni cargos.
- La conversión de TNA a tasa mensual (capitalización cada 30 días) es una convención propia.
- 115 observaciones mensuales y un único episodio de alta inflación.
- Los quiebres detectados dependen de parámetros (largo mínimo de régimen, penalización).
- La serie de tarjetas cubre entidades financieras reguladas; los proveedores no bancarios no entran.
- La EPH cubre los 31 aglomerados urbanos y mide si el hogar recurrió al crédito, no el monto adeudado ni la mora.
- Un tercio de los hogares no declara ingresos y no entra en el análisis por decil.
- Los datos de edad del BCRA no incluyen mora y cada persona cuenta una vez por producto.
