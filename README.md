GDD — Juego de Estrategia por Turnos (WWII) 
Multijugador LAN con Semillas 
Documento de Diseño de Juego (GDD) — Versión 1.0 
Autoría: Equipo de Diseño 
Propósito: Definir reglas, contenido, parámetros numéricos y lógica integral para implementar el 
videojuego. 
1. Visión General 
Género: Estrategia por turnos sobre tablero hexagonal para 2–4 jugadores en red local (LAN). 
Ambientación: Inspiración en la Segunda Guerra Mundial, con foco en maniobra terrestre, 
artillería y blindados. Se prioriza claridad táctica sobre simulación compleja. 
Semillas: El mapa se genera proceduralmente a partir de una semilla compartida para 
reproducibilidad y justicia. 
1.1 Objetivo y Condiciones de Victoria 
• Cada jugador comienza en una Ciudad Capital. Si un jugador pierde su Capital (capturada por 
una unidad rival), queda eliminado y todas sus unidades pasan al control del conquistador. Gana 
el último jugador en pie. 
• Alternativamente (modo opcional futuro): puntos de victoria por control de ciudades y 
objetivos durante N rondas. 
1.2 Filosofía de Diseño 
• Estrategia clara, gestión simplificada: los recursos se calculan y se restan sin cadenas de 
suministro. 
• Partidas dinámicas: límites de tiempo por turno configurables, resolución transparente del 
combate. 
• Determinismo: misma semilla ⇒ mismo mapa; eventos reproducibles para depuración y 
fairness. 
2. Reglas Base y Flujo de Rondas 
Inicio de partida: 
• Cada jugador recibe 1000 de Dinero y 500 de Petróleo. 
• Ciudad Capital inicial por jugador. 
• Unidades iniciales: 1 Reconocimiento blindado y 1 Infantería básica sobre o adyacentes a la 
Capital. 
2.1 Secuencia de Turno (por jugador) 
1. Fase de Administración: revisión de recursos y colas de producción; uso de Estrellas. 
2. Fase de Construcción y Producción: los Ingenieros construyen; los edificios producen según 
sus colas. 
3. Fase de Movimiento: gastar Petróleo según tasa de cada unidad y terreno. 
4. Fase de Combate: ataques a distancia, cuerpo a cuerpo, artillería; resolución determinista. 
5. Fase de Cierre: cálculo automático de ingresos (Dinero y Petróleo) por todos los objetos 
controlados. 
2.2 Economía por Ronda 
Ingresos en Dinero (fin de la ronda): 
• +50 por Capital controlada. 
• +30 por cada Ciudad Grande. 
• +15 por cada Ciudad Pequeña. 
• +3 por cada hex de territorio controlado (sin contar ciudades). 
Producción de Petróleo (fin de la ronda): 
• +10 por cada Pozo de Petróleo controlado. 
• +10% al total de Petróleo producido si controlas una Estación Ferroviaria (acumulativo por 
estación). 
Estrellas: Se obtienen al destruir unidades enemigas. Se gastan para curar/reparar, ascender 
unidades, ataques especiales (p. ej., bombardeo) y despliegues aerotransportados. 
3. Terreno y Generación Procedural 
Cuadrícula: hexagonal. Tipos de terreno: Llanura, Colina, Montaña, Bosque, Pantano, Río, 
Carretera, Vía férrea, Ruinas, Ciudad (Capital/Grande/Pequeña). 
Costes de movimiento (PM base): Llanura 1; Carretera 0.5; Colina 1.5; Bosque 2 (vehículos 3); 
Pantano 3 (vehículos 4); Montaña (solo Alpinos/Ingenieros con penalización); Río: atravesable 
solo por puente o vado designado. 
Apilamiento: hasta 3 unidades diferentes por hex. No se permite apilar 3 del mismo tipo si se 
especifica 'únicas por tipo' en reglas avanzadas (opcional). 
3.1 Semillas y Parámetros del Mapa 
• Semilla compartida (host) genera: alturas, ríos, biomas y distribución de 
ciudades/pozos/estaciones. 
• Tamaños (S/M/L) y densidades configurables en el lobby del anfitrión. 
• Simetría de spawns para 2, 3 o 4 jugadores (espejos o radial). 
3.2 Colocación de Puntos de Interés 
• Ciudades cerca de ríos/vías para rutas verosímiles. 
• Pozos de petróleo en cuencas estratégicas, disputables. 
• Estaciones ferroviarias en nodos de cruce, alto valor por el bonus al Petróleo. 
4. Recursos y Fórmulas 
Los recursos se calculan automáticamente al final de cada ronda. No existen líneas de suministro 
obligatorias ni consumo por distancia a depósitos. 
4.1 Dinero (D) 
D_ronda = 50×Capital + 30×CiudadesGrandes + 15×CiudadesPequeñas + 3×HexTerritorio 
4.2 Petróleo (P) 
P_ronda = 10×Pozos × (1 + 0.10×EstacionesFerroviarias)  [el bonus del 10% por estación se 
acumula]. 
4.3 Estrellas (★) 
★ obtenidas por destruir unidades. Por simplicidad inicial: ★ = ceil(ValorUnidad/10). Se 
emplean para: curar/reparar, ascender, ataque aéreo (si existe la estructura habilitante), o 
despliegue de paracaidistas. 
4.4 Costes de Movimiento (Petróleo) 
Consumo de Petróleo al mover: Consumo = PM_usados × tasa_petroleo_unidad. Infantería 
básica no consume petróleo al desplazarse; vehículos y artillería autopropulsada sí. 
5. Unidades — Listado y Estadísticas 
Cada unidad tiene: Coste en Dinero (C$), Coste en Petróleo de PRODUCCIÓN (CP), Tasa de 
Petróleo de MOVIMIENTO por PM (TPM), PM, Rango (R), Ataque vs. Infantería (AI), Ataque vs. 
Vehículos (AV), Blindaje (B), Vida/HP (HP), Visión (LoS), Rol y Notas. 
ID 
INF_BASIC 
Nombre 
Infantería 
básica 
C$ C
 P 
TP
 M 
P
 M 
R A
 I 
A
 V 
Rol 
B H
 P 
Lo
 S 
60 0 0.0 4 1 4 2 1 10 2 Captura; 
barata; 
fuerte en 
ciudad 
INF_HEAVY Infantería 
pesada 
90 0 0.0 3 1 6 3 2 12 2 Ataque 
superior; 
lenta 
SNIPER Francotirador 11
 0 
0 0.0 3 3 5 1 1 8 3 Precisión; 
elimina 
apoyo 
MG_TEAM Ametralladora 10
 0 
0 0.0 3 2 5 2 2 12 2 Supresión; 
defensiva 
MORTAR Mortero (art. 
ligera) 
12
 0 
1
 0 
0.0 3 3 6 2 1 10 3 Indirecta 
ligera; 
requiere 
visión 
ENGINEER Ingenieros 13
 0 
0 0.0 3 1 3 2 1 10 2 Construcció
 n y 
reparación 
de 
estructuras 
ART_LT Artillería ligera 
remolcada 
14
 0 
1
 0 
0.0 2 3 7 3 2 12 3 Indirecta; 
móvil con 
transporte 
ART_HW Artillería 
pesada 
remolcada 
20
 0 
2
 0 
0.0 2 4 9 4 2 14 3 Alto daño; 
lenta 
SPG Artillería 
autopropulsad
 a 
26
 0 
4
 0 
0.5 4 3 8 4 4 16 3 Movilidad y 
fuego 
indirecto 
MLRS Lanzacohetes 
múltiples 
28
 0 
5
 0 
0.6 4 4 7 5 3 16 3 Área 
amplia; 
impreciso 
AT_GUN Antitanque 
remolcado 
15
 0 
1
 0 
0.0 2 2 2 8 3 12 2 Defensa 
anti
blindaje 
AA_GUN Antiaéreo 
remolcado 
14
 0 
1
 0 
0.0 2 2 5 2 2 12 3 Defensa 
contra 
ataques 
aéreos 
RECON Reconocimient
 o blindado 
13
 0 
1
 5 
0.2 6 1 3 2 2 10 4 Rápido; 
visión 
elevada 
APC Transporte de 
tropas 
16
 0 
2
 0 
0.3 5 1 1 1 3 14 3 Transporte; 
sin gran 
ataque 
LT_TANK Tanque ligero 22
 0 
3
 0 
0.4 6 1 5 5 3 14 3 Rápido; 
frágil 
MD_TANK Tanque medio 30
 0 
4
 5 
0.6 5 1 6 7 6 20 3 Polivalente; 
columna 
vertebral 
HVY_TANK Tanque pesado 42
 0 
7
 0 
0.9 4 1 7 9 8 26 3 Muy 
resistente y 
potente 
TD Cazacarros 34
 0 
5
 5 
0.7 4 2 4 10 5 18 3 Alto daño 
contra 
tanques 
REPAIR_VE
 H 
Vehículo de 
reparación 
18
 0 
1
 5 
0.3 5 1 0 0 2 12 2 Repara 
blindados 
(Dinero/★) 
FUEL_TRUC
 K 
Cisterna de 
suministros 
15
 0 
1
 0 
0.3 5 1 0 0 2 12 2 Reabastece 
Petróleo en 
campo 
Notas numéricas: Los valores son punto de partida para balance. AI/AV representan el potencial 
de daño contra infantería y vehículos; el daño real depende de la fórmula de combate y 
modificadores. TPM=0 indica que la unidad no consume Petróleo al moverse (p. ej., infantería a 
pie). 
  
6. Estructuras — Generadas y Construibles 
6.1 Estructuras generadas por el mapa (no construibles) 
ID Nombre Ingreso/Efecto HP Notas 
CAPITAL Ciudad Capital +50 Dinero/ronda 60 Pérdida ⇒ eliminación 
del jugador; transfiere 
unidades 
CITY_L Ciudad Grande +30 Dinero/ronda 40 Alto valor económico 
CITY_S Ciudad Pequeña +15 Dinero/ronda 30 Valor económico 
moderado 
OIL_WELL Pozo de Petróleo +10 Petróleo/ronda 30 Capturable; objetivo 
prioritario 
RAIL_ST Estación Ferroviaria +10% Petróleo total 30 Bonus acumulativo 
por estación 
BRIDGE Puente — 25 Cruce sobre río; 
destruible y reparable 
RUINS Ruinas/Fortín Cobertura defensiva 20 Mejora defensa; 
buena guarnición 
6.2 Estructuras construibles por jugadores (requieren Ingenieros) 
ID Nombre Costo 
$ 
Tiempo 
(turnos) 
HP Efecto 
TRAIN_CAMP Campo de 
entrenamiento 
180 1 28 Produce infantería y 
morteros 
FACT_LT Fábrica ligera 260 2 32 Produce recon, 
transporte, artillería 
ligera 
FACT_HVY Fábrica pesada 360 3 36 Produce tanques, 
cazacarros, art. 
pesada/autoprop 
REFINERY Refinería 220 2 30 +10 Petróleo/pozo 
cercano (máx. +20 por 
pozo) 
BUNKER Búnker 200 2 45 Defensa fija; admite 
guarnición; +25% defensa 
AA_FIXED Antiaéreo fijo 170 1 26 Defensa AA en radio 3 
HOSP Hospital de campaña 150 1 24 Cura infantería por 
Dinero (barato) 
WORKSHOP Taller blindado 190 1 26 Repara vehículos por 
Dinero 
OBS Observatorio/Radar 160 1 22 +1–2 LoS a unidades 
amigas cercanas 
DEPOT Depósito logístico 140 1 24 +10 Dinero/ronda 
MINEFIELD Campo de minas 100 1 12 Ralentiza e inflige daño al 
entrar 
BRIDGE_YD Taller de puentes 160 1 24 Repara/construye 
puentes más rápido 
AA_NET Red AA (local) 120 1 20 Pequeñas piezas AA 
integradas; radio 2 
BARRICADE Barricadas 80 1 18 Penaliza 
movimiento/asalto del 
enemigo 
HQ_OUT Puesto de mando 
avanzado 
240 2 30 Punto de reaparición 
limitado y control de zona 
  
7. Producción y Árbol de Desbloqueo 
Relación edificio → unidades disponibles. 'Cuanto más grande la fábrica, mejores unidades 
produce'. 
• Campo de entrenamiento: INF_BASIC, INF_HEAVY, SNIPER, MG_TEAM, MORTAR, ENGINEER. 
• Fábrica ligera: RECON, APC, ART_LT, AA_GUN, AT_GUN. 
• Fábrica pesada: LT_TANK, MD_TANK, HVY_TANK, TD, SPG, MLRS. 
Coste en petróleo de PRODUCCIÓN (CP) y coste en petróleo de MOVIMIENTO (TPM) están 
diferenciados para permitir tácticas de ahorro o golpe decisivo. 
Colas de producción: cada edificio administra su propia cola. Unidades aparecen en un hex 
adyacente libre; si no hay espacio, la unidad queda en espera. 
8. Movimiento y Combate 
Movimiento: Cada unidad consume Petróleo al moverse según su TPM × PM usados (excepto 
infantería a pie). Los costes por terreno modifican los PM consumidos. 
Combate: Resolución determinista con tirada porcentual transparente. Fórmulas sugeridas: 
• Probabilidad de impacto (a rango R): P = clamp(P_base − k_dist×(R−1) − CoberturaTerreno, 0.1, 
0.95) 
• Daño neto por impacto: Daño = max(1, AtaqueTipo × ModifTerreno − BlindajeObjetivo) 
• Crítico: 10% de probabilidad; reduce el Blindaje efectivo del objetivo en 50% para ese impacto. 
Cobertura de terreno: Ciudad +25% defensa para infantería; Bosque +10% defensa; Colina +1 
visión y +10% al ataque a distancia. 
8.1 Artillería y Visión 
• Artillería remolcada/autopropulsada y MLRS requieren visión o coordenadas observadas por 
aliados. 
• El Observatorio/Radar otorga detección y contrarresta ocultamiento en bosques/ruinas. 
9. Acciones Especiales con Estrellas (★) 
Acción 
Curar/Rep. táctica 
Ascenso de unidad 
Bombardeo aéreo 
Paracaidistas 
Costo ★ 
1–3 
2 
4–5 
4 
10. Configuración de Partida y LAN 
• Jugadores: 2, 3 o 4. 
Efecto 
Restaura 30–50% HP según tamaño; elimina 
estados negativos 
+10% HP y +10% Ataque; máx. 3 ascensos por 
unidad 
Daño en área; chequear AA cercana reduce o 
anula 
Despliegue de escuadra en hex visible o neutral 
no densamente boscoso 
• Tamaño de mapa: S (60×40), M (80×60), L (100×80). 
• Semilla del mapa (seed): configurable por el anfitrión. 
• Tiempo por turno: 90–180 s recomendado. 
• Condiciones de victoria: Último en pie (por defecto). 
Red: Descubrimiento en la subred local y sincronización de órdenes/estado por turnos. 
Determinismo mediante RNG semillado por (seed del mapa, número de turno e ID de evento). 
11. Correcciones de Lógica — Decisiones de Diseño 
• No hay líneas de suministro ni radios de abasto: los recursos solo se suman/restan 
globalmente. 
• Apilamiento permitido hasta 3 unidades por hex (diferentes para evitar monocultivo 
extremo). 
• Transmisión de control de unidades al conquistar Capital: estado consistente y cierre de 
exploit de 'unidades huérfanas'. 
• Consumo de Petróleo separado entre producción (CP) y movimiento (TPM). 
• Estaciones ferroviarias bonifican Petróleo total (+10% por estación). 
• Capital y ciudades otorgan ingresos fijos por ronda (50/30/15) + territorio a +3/hex. 
12. Balance Inicial — Guías y Ajustes 
El siguiente conjunto de coeficientes está pensado para pruebas alfa. Ajustar tras telemetría y 
feedback: 
• Infantería domina ciudades y bosques; tanques dominan llanuras y carreteras. 
• Artillería disuade apilamientos densos; introducir dispersión para mitigar daño en área. 
• Costes CP altos para blindados fuerzan decisiones: producir menos pero determinantes. 
• Economía de territorio (3/hex) asegura que expandirse siempre importe, aún sin capturar 
ciudades pronto. 
13. Ejemplos Numéricos — Costes y Consumos 
Escenario: Jugador A controla 1 Capital, 1 Ciudad Grande, 2 Ciudades Pequeñas, 24 hex de 
territorio, 2 Pozos y 1 Estación Ferroviaria. 
Dinero: 50 + 30 + (2×15) + (24×3) = 50 + 30 + 30 + 72 = 182 por ronda. 
Petróleo base: 2 Pozos × 10 = 20; Bonus ferroviario: +10% ⇒ 22 por ronda. 
Si produce 1 Tanque Medio (C$=300, CP=45), su Petróleo disponible al principio de la siguiente 
ronda será: 22 − 45 + producción nueva (según timing de colas). Recomendación: programar 
producción en momentos de ahorro de movimiento para evitar quedarse sin Petróleo de 
maniobra. 
14. Interfaz y Experiencia de Usuario 
• HUD con recursos (Dinero, Petróleo, Estrellas) y desglose de ingresos por fuente al final de la 
ronda. 
• Mini-mapa con capas de control territorial y ubicaciones de ciudades/pozos/estaciones. 
• Panel de producción por edificio con tiempo restante y cola clara. 
• Indicadores visuales de % de impacto antes de confirmar ataques. 
• Avisos: 'Capital bajo asedio', 'Búnker guarnecido', 'Petróleo bajo'. 
• Registro de combate por turno, exportable para replay. 
15. Pseudocódigo de Reglas Clave 
Cálculo de ingresos al final de cada ronda: 
 
func calcular_ingresos(jugador): 
    dinero = 50*capitales(j) + 30*ciudades_grandes(j) + 15*ciudades_peq(j) + 3*hex_territorio(j) 
    petroleo_base = 10*pozos(j) 
    multiplicador = 1 + 0.10*estaciones(j) 
    petroleo = round(petroleo_base * multiplicador) 
    return dinero, petroleo 
 
Consumo de Petróleo por movimiento: 
 
func mover_unidad(u, camino): 
    pm_usados = costo_pm(camino, terreno) 
    petroleo_necesario = pm_usados * u.TPM 
    assert jugador.petroleo >= petroleo_necesario 
    jugador.petroleo -= petroleo_necesario 
    u.hex = destino 
 
Captura de Capital y transferencia de unidades: 
 
func capturar_capital(atacante, capital_objetivo): 
    if unidad_atacante_en_hex(capital_objetivo) and sin_enemigos_adyacentes(): 
        perdedor = capital_objetivo.propietario 
        transferir_unidades(perdedor, atacante.propietario) 
        eliminar_jugador(perdedor) 
  
16. IA y Pruebas 
• IA básica: heurística de captura de ciudades/pozos, preservación de blindados, uso de 
artillería para suprimir apilamientos. 
• Pruebas automáticas: simulaciones de 100 seeds por tamaño, ver dispersión de ingresos y 
rutas a Capital. 
• Detección de OOS: validación de hashes de estado por ronda para garantizar sincronización 
en LAN. 
17. Tablas de Daño — Referencia Rápida 
Modificadores de terreno (aplican a defensa del objetivo): Ciudad +25% (infantería); Bosque 
+10%; Ruinas +10%; Colina: atacante a distancia +10%. 
Atacante 
Infantería 
Infantería 
AT Remolcado 
Tanque pesado 
Artillería 
Lanzacohetes 
Objetivo 
Infantería 
Vehículo 
Vehículo 
Infantería 
Apilamientos 
Apilamientos 
Modif Base Notas 
×1.0 
×0.7 
×1.4 
×1.1 
×1.2 
×1.4 
Sin penalización 
Blindaje reduce más 
Especialista anti-blindaje 
Daño por explosivo/HE 
Efecto en área 
Gran área; impreciso 
18. Listas Exhaustivas Faltantes (Cumplimiento) 
• Tropas: 20 unidades definidas arriba (infantería, artillería, blindados, soporte). 
• Estructuras generadas: Capital, Ciudades grandes/pequeñas, Estaciones ferroviarias, Pozos de 
petróleo, Puentes, Ruinas/Fortines. 
• Estructuras construibles: 15 listadas (Campos de entrenamiento, Fábricas, Refinería, Búnker, 
AA, Hospital, Taller, Observatorio, Depósito, Campo de minas, Taller de puentes, Red AA, 
Barricadas, Puesto de mando avanzado). 
19. Roadmap de Implementación 
6. Generador por semilla (terreno, ríos, ciudades, pozos, estaciones, puentes). 
7. Estados base, turnos, apilamiento y captura de Capital. 
8. Economía: ingresos por ronda y colas de producción. 
9. Movimiento con consumo de Petróleo y límites por terreno. 
10. Combate: LoS, probabilidades, artillería y apilamientos. 
11. Acciones con Estrellas y estructuras defensivas. 
12. LAN por turnos: órdenes, validación y sincronización determinista. 
13. Pruebas de balance y QA de 100+ seeds por tamaño. 
20. Anexos — Parámetros Ajustables (sugeridos) 
Parámetro 
Tiempo por turno 
Límite apilamiento 
Crit chance 
k_dist (penalización por rango) 
Bonus estación ferroviaria 
Dinero por territorio 
Valor por defecto 
120 s 
3 unidades 
10% 
10%/anillo 
+10% Petróleo 
+3/hex 
Rango recomendado 
60–180 s 
2–3 
5–15% 
5–15% 
+5–15% 
+2–4/hex 
