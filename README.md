# Contar con Datos 2026: costo del crédito y salario real

¿El costo real de un préstamo personal o de una tarjeta crece más rápido que el salario real
de quien lo paga, y varía según el sector? Análisis mensual de enero de 2017 a julio de 2026.

## Resultado principal

Sin amortizar, una deuda por préstamo personal crece **+327%** en términos reales desde
diciembre de 2016, mientras los salarios reales terminan **por debajo** de ese nivel
(privado registrado −20,5%, público −34,3%, no registrado −6,5%).
La tasa real de endeudamiento pasa por regímenes bien distintos: deuda cara hasta 2020 o 2021,
barata entre 2021 y 2023 (con un tramo muy negativo a fines de 2023) y muy cara desde 2024.

> El supuesto "sin amortizar" es un caso extremo (nadie deja de pagar por completo).
> Mide la presión del sistema, no la deuda de una persona real.

## Estructura

```
contar-datos-2026/
├── datos/
│   ├── crudos/          datos tal como se descargaron
│   └── procesados/      panel_mensual.csv (generado por scripts/01)
├── scripts/             código, numerado en el orden en que se corre
├── resultados/
│   ├── graficos/        figuras en PNG
│   └── tablas/          tablas en CSV
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
python3 scripts/02_analisis_basico.py     # media y desvío por período
python3 scripts/03_acumulado_deuda.py     # deuda sin amortizar contra ingreso, por sector
python3 scripts/04_tasa_real_media.py     # gráfico de la tasa real
python3 scripts/05_salario_real.py        # gráfico del salario real
python3 scripts/06_credito_vs_salario.py      # deuda contra salarios, base 100
python3 scripts/07_credito_vs_salario_pct.py  # igual, en variación porcentual
python3 scripts/08_puntos_de_cambio.py    # detección de regímenes (PELT y BIC)
```

Cada script se puede correr desde cualquier carpeta. `scripts/inicio.py` concentra las
librerías, los colores, las rutas y las funciones comunes.

## Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `datos/crudos/ipc_mensual.csv` | IPC nivel general, base dic-2016 = 100 | INDEC, vía datos.gob.ar (serie 148.3_INIVELNAL_DICI_M_26) |
| `datos/crudos/indice_salarios.csv` | Índice de salarios por sector, oct-2016 = 100 | INDEC |
| `datos/crudos/tasas_interes.csv` | Tasas de interés activas (TNA %), incluye personales y tarjetas | BCRA, vía datos.gob.ar |
| `datos/crudos/ripte.csv` | RIPTE, remuneración imponible promedio | Secretaría de Seguridad Social, vía datos.gob.ar (no usado todavía) |

## Método, en resumen

- Tasa nominal mensual: `i = (1 + TNA / (100 * 365)) ** 30 - 1`
- Tasa real (Fisher): `r = (1 + i) / (1 + pi) - 1`
- Salario real: `g = (1 + w) / (1 + pi) - 1`
- Deuda sin amortizar respecto del ingreso: producto acumulado de `(1 + r) / (1 + g)`
- Regímenes: PELT y segmentación por mínimos cuadrados con selección por BIC
  (en el espíritu de Bai-Perron, sin los tests sup-F ni los intervalos de confianza).

## Limitaciones

- Misma tasa de interés para todos los sectores; las diferencias salen solo del salario.
- La serie de salarios no registrados viene de la EPH, con suavizado y rezago de unos 5 meses.
- 115 observaciones mensuales y un único episodio de alta inflación.
- Los quiebres detectados dependen de parámetros (largo mínimo de régimen, penalización).
