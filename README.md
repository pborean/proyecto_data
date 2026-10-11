# Contar con Datos 2026: costo real del crédito

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
y el 5% en julio de 2025. Es decir, sube con unos 12 a 15 meses de demora respecto del cambio de signo de la tasa real.
La serie muestra que las dos cosas ocurrieron en ese orden, no que una cause la otra. La mora también subió en 2021, con tasa real baja.
Tablas: `mora_por_producto.csv` y `mora_por_regimen.csv`.

### Dónde está la mora (`scripts/17_donut_cartera_vs_mora.py`)
Dos donuts de la cartera de las familias en julio de 2026 (entidades financieras): de cada $100 prestados y de cada $100 en mora. La cartera irregular de cada línea
es su ratio de irregularidad por su saldo. Los préstamos personales son 31% de la cartera y 41% de la mora; las tarjetas, 32% y 32%; los hipotecarios, 25% y 3%;
los prendarios, 5% y 3%; y "Otros", 7% y 22%. Las tarjetas no pesan más en la mora que en la cartera: lo hacen los personales y "Otros" (una línea chica, con 40% de mora).
En septiembre de 2020 las tarjetas eran 41% de la cartera y 25% de la mora. Tabla: `cartera_vs_mora_por_linea.csv`.

### Quién presta (`scripts/10_prestamistas.py`)
Porcentaje de los adultos con al menos un crédito en entidades financieras (bancos y compañías financieras) y en proveedores
no financieros de crédito (tarjetas no bancarias y otros). De julio de 2024 a diciembre de 2025, las entidades financieras pasan de
36,2% a 39,6% y los proveedores no financieros de 22,6% a 32,2%. Los proveedores no financieros crecen sobre todo entre los 20 y los
49 años (12 a 14 puntos); las entidades financieras, entre los mayores de 60 (7 a 9 puntos).
La serie del BCRA cambia de nivel en julio de 2024 en todos los grupos, por eso la comparación empieza ese mes.
En diciembre de 2024 hay un traspaso entre tarjetas no bancarias y otros proveedores: se usa solo el total de proveedores no financieros.
Una persona cuenta una vez por grupo, por lo que los grupos no se suman. Tablas: `prestamistas_grupo_institucional.csv` y `prestamistas_cambio_por_edad.csv`.

**Cuándo subió, por edad** (`scripts/16_mapa_calor_edad.py`). Mapa de calor de edad por mes con el aumento, en puntos porcentuales, respecto de julio de 2024, con la misma escala para
los dos grupos. En los proveedores no financieros el aumento es sostenido y se concentra entre los 20 y los 49 años: a los 25–39 es de +5 a +6 puntos en diciembre de 2024,
+9 a +10 en junio de 2025 y +13 a +14 en diciembre de 2025. En los bancos y compañías financieras el aumento está en los mayores de 60 (a los 65–79, de +4 en diciembre de 2024 a +9 en diciembre de 2025);
a los 25–39 llegó a +2,5 en junio de 2025 y bajó a entre +1,4 y +2,6 en diciembre. Tabla: `mapa_calor_edad.csv`.

### Quién se endeuda
**Por edad** (`scripts/08_deuda_por_edad.py`). Porcentaje de cada grupo de edad con al menos un crédito, por producto (tarjetas y préstamos personales).
Se compara diciembre de 2024 con diciembre de 2025 por el cambio de nivel de julio de 2024.

**Por nivel de ingreso** (`scripts/09_eph_endeudamiento_decil.py`). Porcentaje de hogares que, en los últimos tres meses, pidieron un préstamo a un banco o
financiera (V15) o a familiares o amigos (V14), y porcentaje de hogares que compran en cuotas o al fiado con tarjeta o libreta (V16; la pregunta no fija un plazo), según el decil de ingreso per cápita familiar.
Trimestres 2T2024 a 1T2026 (el 1T2024 aparece como referencia en el gráfico por trimestre). Estratos según INDEC: bajo = deciles 1 a 4, medio = 5 a 8, alto = 9 y 10.

- Cuotas o fiado con tarjeta o libreta: sube con el ingreso, de 36% en el decil 1 a 65% en el decil 10.
- Préstamo de familia o amigos: baja con el ingreso, de 31% en el decil 1 a 7% en el decil 10.
- Préstamo de banco o financiera: entre 10% y 16% en todos los deciles; el más bajo es el decil 10.
- En todos los hogares, el préstamo bancario pasa de 12,5% (1T2024) a 16,4% (4T2025) y 15,6% (1T2026).

`scripts/15_waffle_hogares.py` muestra esos mismos porcentajes para los deciles 1, 5 y 10 como 100 cuadraditos (cada uno es 1 de cada 100 hogares): cuotas o fiado,
de 35 a 66 de cada 100; préstamo de familia o amigos, de 30 a 7; préstamo bancario, 12, 16 y 9. Las tres fuentes no se excluyen entre sí, por lo que cada waffle se lee por separado.

La EPH registra si el hogar recurrió a cada fuente, no cuánto debe ni si está en mora. El 31,6% de los hogares (ponderados) no tiene decil de ingreso
porque no declaró ingresos y queda afuera. Tablas: `eph_endeudamiento_decil.csv` y `eph_endeudamiento_trimestre.csv`.

### Argentina frente a la región (`scripts/12_mora_regional.py`)
Mora de todos los préstamos bancarios (no solo familias), 2020 a 2025, para Argentina y otros nueve países (ocho de la región: Brasil, Chile, México, Colombia, Uruguay, Perú, Paraguay y Bolivia; y Estados Unidos como referencia). En 2025 Argentina tiene 5,3%, el valor más alto del grupo (los otros países tienen entre 1,0% y 4,0% en su último dato; Bolivia, Perú y Uruguay solo llegan a 2024). En 2024 había bajado a 1,6%. En el gráfico de la derecha, el rango de la región se calcula con los países de la región que tienen dato cada año (5 a 8; Estados Unidos no entra). Los años sin dato quedan vacíos. Tabla: `mora_bancaria_paises.csv`.

### Crédito de los bancos como porcentaje del PBI (`scripts/14_credito_pbi.py`)
Saldo de financiaciones de las entidades financieras (sector privado total, familias y tarjetas de las familias) a fin de cada trimestre, dividido por el PBI nominal de los últimos 12 meses, desde septiembre de 2020.
El PBI nominal se calcula como el promedio de los últimos cuatro trimestres, porque INDEC publica cada trimestre "a ritmo anual". Entre 2020-T3 y 2026-T2:
el crédito total pasa de 13,1% a 16,0% del PBI (con un piso de 10,7% en 2023-T1), el de las familias de 6,1% a 7,1% (piso de 4,9%) y el de tarjetas de las familias se queda entre 2,1% y 2,9%.
El aumento del crédito a las familias desde 2024 no vino de las tarjetas. Tabla: `credito_pbi.csv`. El PBI de 2025 y 2026 es preliminar.

## Estructura

```
contar-datos-2026/
├── datos/
│   ├── crudos/          datos tal como se descargaron (la EPH no se sube al repo, ver más abajo)
│   └── procesados/      panel_mensual.csv (generado por scripts/01)
├── scripts/             código, numerado en el orden en que se corre
├── resultados/
│   ├── graficos/        regimenes_tarjetas, credito_pbi, mora_por_producto, prestamistas_edad, eph_endeudamiento_decil, deuda_por_edad, mora_regional,
│   │                    waffle_hogares, mapa_calor_edad, donut_cartera_vs_mora, etc.
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
python3 scripts/14_credito_pbi.py                # crédito de los bancos como % del PBI (BCRA e INDEC)
python3 scripts/15_waffle_hogares.py             # waffle de hogares por fuente de crédito y decil (usa la tabla del 09)
python3 scripts/16_mapa_calor_edad.py            # mapa de calor edad por mes (BCRA)
python3 scripts/17_donut_cartera_vs_mora.py      # cartera y mora por línea de crédito (BCRA)
```

La numeración salta del 06 al 08 y del 12 al 14 (no hay scripts 07 ni 13).
El script 15 necesita que el 09 se haya corrido antes (lee `eph_endeudamiento_decil.csv`).
`scripts/inicio.py` concentra las librerías, los colores, las rutas y las funciones comunes.

## Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `datos/crudos/ipc_mensual.csv` | IPC nivel general, base dic-2016 = 100 | INDEC, vía datos.gob.ar (serie 148.3_INIVELNAL_DICI_M_26) |
| `datos/crudos/tasas_interes.csv` | Tasas de interés activas (TNA %); se usa la columna de tarjetas | BCRA, vía datos.gob.ar |
| `datos/crudos/indice_salarios.csv` | Índice de salarios por sector, oct-2015 a jul-2026 | INDEC |
| `datos/crudos/bcra_deudores_sfa_asistencia_rango_etario.xlsx` | Porcentaje de cada edad con al menos un crédito, por producto | BCRA, Indicadores de Inclusión Financiera, tabla 4.2 |
| `datos/crudos/bcra_deudores_sfa_grupo_institucional_rango_etario.xlsx` | Porcentaje de cada edad con al menos un crédito, por grupo de entidad | BCRA, Indicadores de Inclusión Financiera, hoja 4.3.4 |
| `datos/crudos/bcra_informe_bancos_anexo.xlsx` | Mora (cartera irregular) y saldo de financiaciones por línea de crédito, familias y empresas | BCRA, Anexo estadístico del Informe sobre Bancos, hoja "Calidad de Cartera (por líneas)" |
| `datos/crudos/indec_oferta_demanda_trimestral.xls` | PBI a precios corrientes, trimestral (cuadro 8, fila B1b) | INDEC, Series trimestrales de oferta y demanda globales, 2004-2026 |
| `datos/crudos/bm_mora_bancaria_paises.json` | Mora bancaria total, por país | Banco Mundial, indicador FB.AST.NPER.ZS (datos del FMI, Financial Soundness Indicators), licencia CC BY-4.0 |
| `datos/crudos/eph/EPH_usu_*_Trim_*_txt/` | EPH continua, base de hogares, 1T2024 a 1T2026 (no se sube al repo por su tamaño) | INDEC, Bases de datos |

## Citas y fuentes

Datos consultados entre el 7 y el 11 de octubre de 2026. Todos los gráficos y tablas de este repositorio son elaboración propia con los datos que se citan abajo; ningún dato fue modificado en su significado.

### Banco Central de la República Argentina (BCRA)
- Banco Central de la República Argentina. *Indicadores de Inclusión Financiera: deudores del sistema financiero ampliado, por rango etario y por grupo institucional* [archivos Excel]. https://www.bcra.gob.ar/indicadores-inclusion-financiera/
- Banco Central de la República Argentina. *Informe sobre Bancos, Anexo estadístico* (hoja "Calidad de Cartera (por líneas)": cartera irregular y saldo de financiaciones, mensual, 2010 a julio de 2026) [archivo Excel]. https://www.bcra.gob.ar/informe-sobre-bancos/
- Banco Central de la República Argentina. *Principales tasas de interés* (series de tasas activas), vía datos.gob.ar [CSV]. https://datos.gob.ar/dataset/sspm-principales-tasas-interes
- Condiciones de reutilización de los contenidos del BCRA (sección 3, "Propiedad intelectual y reutilización de contenidos"): https://www.bcra.gob.ar/aviso-legal/

### Instituto Nacional de Estadística y Censos (INDEC)
- Instituto Nacional de Estadística y Censos. *Índice de precios al consumidor (IPC) nacional, nivel general, base diciembre de 2016 = 100*, vía datos.gob.ar [CSV]. https://datos.gob.ar/dataset/sspm-indice-precios-al-consumidor-nacional-ipc-base-diciembre-2016
- Instituto Nacional de Estadística y Censos. *Índice de salarios: series, números índice, octubre de 2015 a julio de 2026* [CSV]. https://www.indec.gob.ar/ftp/cuadros/sociedad/indice_salarios.csv. Metadatos de las series: https://www.indec.gob.ar/ftp/cuadros/sociedad/metadatos_series_salarios.txt
- Instituto Nacional de Estadística y Censos. *Series trimestrales de oferta y demanda globales, 2004-2026*, cuadro 8 (producto interno bruto a precios corrientes) [archivo Excel]. https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-47
- Instituto Nacional de Estadística y Censos. *Encuesta Permanente de Hogares (EPH), base usuaria de hogares, 1.er trimestre de 2024 a 1.er trimestre de 2026* [microdatos]. https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos
- Instituto Nacional de Estadística y Censos. *EPH: diseño de registro y estructura, 1T2026* (variables V14, V15, V16, PONDERA, PONDIH, DECCFR). https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_registro_1T2026.pdf
- Instituto Nacional de Estadística y Censos (2026, 1 de octubre). *Evolución de la distribución del ingreso (EPH). Segundo trimestre de 2026* (Informes técnicos, vol. 10, n.º 243; Trabajo e ingresos, vol. 10, n.º 9; definición de estratos por decil). https://www.indec.gob.ar/uploads/informesdeprensa/ingresos2trim26B36ABAB2C6.pdf

### Banco Mundial
- Banco Mundial. *Bank nonperforming loans to total gross loans (%)*, indicador FB.AST.NPER.ZS, con datos del Fondo Monetario Internacional (Financial Soundness Indicators). https://data.worldbank.org/indicator/FB.AST.NPER.ZS

### Licencias y condiciones de uso
- **BCRA:** reutilización permitida con fines informativos, educativos o académicos, citando la fuente completa ("Banco Central de la República Argentina") y sin alterar el sentido de los contenidos (Aviso legal del BCRA, sección 3).
- **INDEC:** las publicaciones citadas indican que se permite su reproducción con atribución de la fuente (licencia Creative Commons).
- **Banco Mundial:** licencia CC BY-4.0 (según figura en la página del indicador FB.AST.NPER.ZS; fuente primaria: Fondo Monetario Internacional, Financial Soundness Indicators).
- **datos.gob.ar:** los datasets citados (IPC del INDEC y tasas de interés del BCRA) están publicados en el Portal Nacional de Datos Abiertos de la República Argentina; la licencia de cada uno es la que figura en su campo "Licencia" en el portal.

### Cómo citar este trabajo
Elaboración propia con datos del Banco Central de la República Argentina, el Instituto Nacional de Estadística y Censos y el Banco Mundial (ver fuentes arriba).

### Cómo conseguir la EPH
1. Entrar a https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos y bajar, en formato txt, la base individual y hogar de los trimestres 1T2024 a 1T2026
   (nueve archivos `EPH_usu_{trimestre}_Trim_{año}_txt.zip`, publicados en https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/).
2. Descomprimir cada uno en su propia carpeta dentro de `datos/crudos/eph/`. El script busca el archivo `usu_hogar_*.txt` dentro de cada carpeta.

### Cómo conseguir los datos del Banco Mundial
Una sola consulta a la API pública, que se guarda en `datos/crudos/bm_mora_bancaria_paises.json`:

```
curl -fL -o datos/crudos/bm_mora_bancaria_paises.json \
 "https://api.worldbank.org/v2/country/ARG;BRA;CHL;MEX;COL;URY;PER;PRY;BOL;USA;LCN;WLD/indicator/FB.AST.NPER.ZS?format=json&per_page=2000&date=2020:2025"
```

Los agregados de América Latina y el Caribe (LCN) y del Mundo (WLD) no tienen datos para este indicador y no aparecen en los resultados.

## Método, en resumen

- Tasa nominal mensual: `i = (1 + TNA / (100 * 365)) ** 30 - 1`
- Tasa real (Fisher): `r = (1 + i) / (1 + pi) - 1`
- Regímenes: PELT y segmentación por mínimos cuadrados con selección por BIC
  (en el espíritu de Bai-Perron, sin los tests sup-F ni los intervalos de confianza).
- En el gráfico de regímenes la curva está suavizada (media móvil de 5 meses); los números
  grandes salen de los datos mensuales sin suavizar.
- Mora: cartera irregular (situaciones 3 a 6) sobre cartera total; familias = personas humanas sin destino comercial (definiciones de la hoja "Metodología y Referencias" del archivo del BCRA).
- Crédito/PBI: saldo a fin de trimestre dividido por el promedio de los últimos cuatro trimestres del PBI nominal (valores a ritmo anual). Solo entidades financieras.
- EPH: porcentaje ponderado de hogares con respuesta "sí" entre los que contestaron sí o no. Ponderador `PONDERA` (la "Ponderación" de la base de hogar; el registro reserva `PONDIH` para el ingreso total familiar y el per cápita familiar). Con `PONDIH` los porcentajes por decil cambian en 1 punto o menos. Decil: `DECCFR`, decil nacional del ingreso per cápita familiar.

## Limitaciones

- Es la tasa promedio del sistema informada al BCRA, no la de una entidad ni la de una persona. No incluye comisiones, seguros ni cargos.
- La conversión de TNA a tasa mensual (capitalización cada 30 días) es una convención propia.
- 115 observaciones mensuales (enero de 2017 a julio de 2026) y pocos episodios de tasa real extrema: cada régimen se apoya en un solo ciclo. Los quiebres detectados dependen de parámetros (largo mínimo de régimen, penalización).
- La tasa real es ex post: usa la inflación efectivamente ocurrida en el mes (IPC nacional del INDEC), no la esperada al momento de endeudarse, y no refleja la inflación particular de cada hogar.
- La serie de tarjetas cubre entidades financieras reguladas; los proveedores no bancarios no entran en la tasa ni en la mora.
- La mora que se muestra coincide en el tiempo con la tasa real alta; no demuestra que una cause la otra. También influyen salarios, empleo y expansión previa del crédito.
- La EPH cubre los 31 aglomerados urbanos y mide si el hogar recurrió al crédito (en los últimos tres meses para los préstamos, V14 y V15), no el monto adeudado ni la mora. La variable V16 pregunta si el hogar compra en cuotas o al fiado, sin plazo explícito, e incluye tarjeta de crédito y libreta, por lo que no es solo deuda de tarjeta. Un tercio de los hogares no declara ingresos y no entra en el análisis por decil.
- Los datos de edad y de grupo de entidad del BCRA no incluyen mora, cada persona cuenta una vez por producto o grupo, y la serie cambia de nivel en julio de 2024 (la causa no figura en las notas del archivo).
- El crédito/PBI cubre solo las entidades financieras que informan al BCRA (no fintech ni otros no bancarios) y usa el PBI nominal preliminar de 2025 y 2026; no se compara con series de otras fuentes (por ejemplo BIS), que definen el crédito de otra manera.
- En el gráfico de cartera y mora por línea, "Otros" es una línea chica (7% de la cartera) con una mora muy alta; los porcentajes redondeados pueden sumar 101.
- La comparación regional usa la mora de todos los préstamos bancarios, con definiciones que pueden diferir entre países; el conjunto de ocho países de la región lo definimos nosotros (Estados Unidos se agrega como referencia, pero no entra en el rango regional), y algunos tienen dato solo hasta 2024.

## Uso de inteligencia artificial

Se usó Claude (Anthropic) como asistente, bajo supervisión de los autores, en estas etapas: exploración de los datos, escritura y revisión del código de análisis y de los gráficos de este repositorio, revisión de fuentes y redacción de esta documentación. Las cifras provienen de las fuentes citadas arriba.
[CONFIRMAR: indicar cómo se hizo la visualización final presentada al concurso y que fue elaborada por los autores, sin IA generativa.]
La declaración completa del uso de IA figura en el Formulario de Inscripción del concurso.
