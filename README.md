# Contar con Datos 2026: costo real del crédito con tarjeta

¿Cuándo fue cara y cuándo barata la deuda de tarjeta de crédito frente a la inflación?
Análisis mensual de enero de 2017 a julio de 2026, más un análisis del régimen actual (desde abril de 2024):
quién se endeuda, quién presta, cómo evolucionó la mora y cómo se compara con la región.

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

## El régimen actual en detalle

### La mora de las familias (`scripts/11_mora_por_producto.py`)
Desde septiembre de 2020 se compara la tasa real con la mora de las familias en tarjetas y préstamos personales
(cartera irregular sobre cartera total, entidades financieras). Del inicio al fin de cada régimen:

| Régimen | Mora de tarjetas | Mora de personales |
|---|---|---|
| Sep-2020 a jul-2023 | 1,7% a 2,3% | 4,2% a 4,7% |
| Ago-2023 a mar-2024 | 2,0% a 1,8% | 4,7% a 4,3% |
| Abr-2024 a jul-2026 | 1,8% a 12,8% | 4,3% a 16,7% |

En el régimen actual la mora de tarjetas tiene su mínimo en octubre de 2024 (1,7%), supera el 3% en abril de 2025
y el 5% en julio de 2025. Es decir, sube con unos 8 a 12 meses de demora respecto del cambio de signo de la tasa real.
La serie muestra que las dos cosas ocurrieron en ese orden, no que una cause la otra. La mora también subió en 2021, con tasa real baja.
Tablas: `mora_por_producto.csv` y `mora_por_regimen.csv`.

### Quién presta (`scripts/10_prestamistas.py`)
Porcentaje de los adultos con al menos un crédito en entidades financieras (bancos y compañías financieras) y en proveedores
no financieros de crédito (tarjetas no bancarias y otros). De julio de 2024 a diciembre de 2025, las entidades financieras pasan de
36,2% a 39,6% y los proveedores no financieros de 22,6% a 32,2%. Los proveedores no financieros crecen sobre todo entre los 20 y los
49 años (12 a 14 puntos); las entidades financieras, entre los mayores de 60 (6 a 9 puntos).
La serie del BCRA cambia de nivel en julio de 2024 en todos los grupos, por eso la comparación empieza ese mes.
En diciembre de 2024 hay un traspaso entre tarjetas no bancarias y otros proveedores: se usa solo el total de proveedores no financieros.
Una persona cuenta una vez por grupo, por lo que los grupos no se suman. Tablas: `prestamistas_grupo_institucional.csv` y `prestamistas_cambio_por_edad.csv`.

### Quién se endeuda
**Por edad** (`scripts/08_deuda_por_edad.py`). Porcentaje de cada grupo de edad con al menos un crédito, por producto (tarjetas y préstamos personales).
Se compara diciembre de 2024 con diciembre de 2025 por el cambio de nivel de julio de 2024.

**Por nivel de ingreso** (`scripts/09_eph_endeudamiento_decil.py`). Porcentaje de hogares que, en los últimos tres meses, pidieron un préstamo a un banco o
financiera (V15), compraron en cuotas o al fiado con tarjeta o libreta (V16) o pidieron un préstamo a familiares o amigos (V14), según el decil de ingreso per cápita familiar.
Trimestres 2T2024 a 1T2026 (el 1T2024 aparece como referencia en el gráfico por trimestre). Estratos según INDEC: bajo = deciles 1 a 4, medio = 5 a 8, alto = 9 y 10.

- Cuotas o fiado con tarjeta o libreta: sube con el ingreso, de 36% en el decil 1 a 65% en el decil 10.
- Préstamo de familia o amigos: baja con el ingreso, de 31% en el decil 1 a 7% en el decil 10.
- Préstamo de banco o financiera: entre 10% y 16% en todos los deciles; el más bajo es el decil 10.
- En todos los hogares, el préstamo bancario pasa de 12,5% (1T2024) a 16,4% (4T2025) y 15,6% (1T2026).

La EPH registra si el hogar recurrió a cada fuente, no cuánto debe ni si está en mora. El 31,6% de los hogares (ponderados) no tiene decil de ingreso
porque no declaró ingresos y queda afuera. Tablas: `eph_endeudamiento_decil.csv` y `eph_endeudamiento_trimestre.csv`.

### Argentina frente a la región (`scripts/12_mora_regional.py`)
Mora de todos los préstamos bancarios (no solo familias), 2020 a 2025, para Argentina y otros nueve países. En 2025 Argentina tiene 5,3%, el valor más alto del grupo
(los otros países tienen entre 1,0% y 4,0%, algunos con dato de 2024). En 2024 había bajado a 1,6%. En el gráfico de la derecha, el rango de la región se calcula con los países que tienen dato cada año
(5 a 8). Los años sin dato quedan vacíos. Tabla: `mora_bancaria_paises.csv`.

## Estructura

```
contar-datos-2026/
├── datos/
│   ├── crudos/          datos tal como se descargaron (la EPH no se sube al repo, ver más abajo)
│   └── procesados/      panel_mensual.csv (generado por scripts/01)
├── scripts/             código, numerado en el orden en que se corre
├── resultados/
│   ├── graficos/        regimenes_tarjetas, mora_por_producto, prestamistas_edad, eph_endeudamiento_decil, deuda_por_edad, mora_regional, etc.
│   └── tablas/          una tabla por análisis (inflacion_por_regimen.csv, mora_por_regimen.csv, etc.)
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
python3 scripts/10_prestamistas.py               # quién presta (BCRA)
python3 scripts/11_mora_por_producto.py          # mora por producto y régimen (BCRA)
python3 scripts/12_mora_regional.py              # mora bancaria frente a la región (Banco Mundial)
```

La numeración salta del 06 al 08 (no hay script 07).
`scripts/inicio.py` concentra las librerías, los colores, las rutas y las funciones comunes.

## Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `datos/crudos/ipc_mensual.csv` | IPC nivel general, base dic-2016 = 100 | INDEC, vía datos.gob.ar (serie 148.3_INIVELNAL_DICI_M_26) |
| `datos/crudos/tasas_interes.csv` | Tasas de interés activas (TNA %); se usa la columna de tarjetas | BCRA, vía datos.gob.ar |
| `datos/crudos/indice_salarios.csv` | Índice de salarios por sector, oct-2016 = 100 | INDEC |
| `datos/crudos/ripte.csv` | RIPTE, remuneración imponible promedio (no usado todavía) | Secretaría de Seguridad Social, vía datos.gob.ar |
| `datos/crudos/bcra_deudores_sfa_asistencia_rango_etario.xlsx` | Porcentaje de cada edad con al menos un crédito, por producto | BCRA, Indicadores de Inclusión Financiera, tabla 4.2 |
| `datos/crudos/bcra_deudores_sfa_grupo_institucional_rango_etario.xlsx` | Porcentaje de cada edad con al menos un crédito, por grupo de entidad | BCRA, Indicadores de Inclusión Financiera, hoja 4.3.4 |
| `datos/crudos/bcra_informe_bancos_anexo.xlsx` | Mora (cartera irregular) por línea de crédito, familias y empresas | BCRA, Anexo estadístico del Informe sobre Bancos, hoja "Calidad de Cartera (por líneas)" |
| `datos/crudos/bm_mora_bancaria_paises.json` | Mora bancaria total, por país | Banco Mundial, indicador FB.AST.NPER.ZS (datos del FMI, Financial Soundness Indicators), licencia CC BY 4.0 |
| `datos/crudos/eph/EPH_usu_*_Trim_*_txt/` | EPH continua, base de hogares, 1T2024 a 1T2026 (no se sube al repo por su tamaño) | INDEC, Bases de datos |

Páginas de origen:
- BCRA, Indicadores de inclusión financiera: https://www.bcra.gob.ar/indicadores-inclusion-financiera/
- BCRA, Informe sobre Bancos (datos): https://www.bcra.gob.ar/informe-sobre-bancos/
- INDEC, Bases de datos: https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos
- Banco Mundial, indicador FB.AST.NPER.ZS: https://data.worldbank.org/indicator/FB.AST.NPER.ZS

Archivos descargados el 10 y 11 de octubre de 2026.

### Cómo conseguir la EPH
1. Entrar a https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos y bajar, en formato txt, la base individual y hogar de los trimestres 1T2024 a 1T2026
   (nueve archivos `EPH_usu_{trimestre}_Trim_{año}_txt.zip`, publicados en https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/).
2. Descomprimir cada uno en su propia carpeta dentro de `datos/crudos/eph/`. El script busca el archivo `usu_hogar_*.txt` dentro de cada carpeta.
3. El INDEC reemplazó el archivo del 4T2024 el 7 de mayo de 2025: se usa la versión vigente.

### Cómo conseguir los datos del Banco Mundial
Una sola consulta a la API pública, que se guarda en `datos/crudos/bm_mora_bancaria_paises.json`:

```
curl -fL -o datos/crudos/bm_mora_bancaria_paises.json \
 "https://api.worldbank.org/v2/country/ARG;BRA;CHL;MEX;COL;URY;PER;PRY;BOL;USA;LCN;WLD/indicator/FB.AST.NPER.ZS?format=json&per_page=2000&date=2020:2025"
```

Los agregados de América Latina y el Caribe (LCN) y del Mundo (WLD) no tienen datos para este indicador y no aparecen en los resultados.

Documentación de referencia:
- Diseño de registro y estructura de la EPH, 1T2026 (variables V14, V15, V16, PONDERA, DECCFR): https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_registro_1T2026.pdf
- INDEC, "Evolución de la distribución del ingreso (EPH)", segundo trimestre de 2026, Informes técnicos, vol. 10, n.º 243, 1 de octubre de 2026 (definición de estratos por decil).

## Método, en resumen

- Tasa nominal mensual: `i = (1 + TNA / (100 * 365)) ** 30 - 1`
- Tasa real (Fisher): `r = (1 + i) / (1 + pi) - 1`
- Regímenes: PELT y segmentación por mínimos cuadrados con selección por BIC
  (en el espíritu de Bai-Perron, sin los tests sup-F ni los intervalos de confianza).
- En el gráfico de regímenes la curva está suavizada (media móvil de 5 meses); los números
  grandes salen de los datos mensuales sin suavizar.
- Mora: cartera irregular (situaciones 3 a 6) sobre cartera total; familias = personas humanas sin destino comercial (definiciones de la hoja "Metodología y Referencias" del archivo del BCRA).
- EPH: porcentaje ponderado de hogares con respuesta "sí" entre los que contestaron sí o no. Ponderador `PONDERA` (según el diseño de registro, `PONDIH` se usa solo para ingresos).
  Decil: `DECCFR`, decil nacional del ingreso per cápita familiar.

## Limitaciones

- Es la tasa promedio del sistema informada al BCRA, no la de una entidad ni la de una persona. No incluye comisiones, seguros ni cargos.
- La conversión de TNA a tasa mensual (capitalización cada 30 días) es una convención propia.
- 115 observaciones mensuales y un único episodio de alta inflación. Los quiebres detectados dependen de parámetros (largo mínimo de régimen, penalización).
- La serie de tarjetas cubre entidades financieras reguladas; los proveedores no bancarios no entran en la tasa ni en la mora.
- La mora que se muestra coincide en el tiempo con la tasa real alta; no demuestra que una cause la otra. También influyen salarios, empleo y expansión previa del crédito.
- La EPH cubre los 31 aglomerados urbanos y mide si el hogar recurrió al crédito, no el monto adeudado ni la mora. Un tercio de los hogares no declara ingresos y no entra en el análisis por decil.
- Los datos de edad y de grupo de entidad del BCRA no incluyen mora, cada persona cuenta una vez por producto o grupo, y la serie cambia de nivel en julio de 2024 (la causa no figura en las notas del archivo).
- La comparación regional usa la mora de todos los préstamos bancarios, con definiciones que pueden diferir entre países; el conjunto de ocho países de la región lo definimos nosotros, y algunos tienen dato solo hasta 2024.

## Uso de inteligencia artificial

Se usó Claude (Anthropic) como asistente para escribir y revisar el código de análisis, explorar los datos y revisar fuentes. Las cifras provienen de las fuentes citadas arriba.
La declaración completa del uso de IA figura en el Formulario de Inscripción del concurso.
