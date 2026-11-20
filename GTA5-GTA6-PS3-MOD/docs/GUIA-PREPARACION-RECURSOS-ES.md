# Guía de preparación de recursos — español

**Objetivo:** preparar un inventario técnico de los recursos de la copia propia de GTA V para PS3, sin modificar el juego y sin compartir archivos protegidos.

> Esta guía no instala el mod. El mod todavía no tiene recursos nativos integrados ni PKG.

## Antes de empezar

- Debes trabajar únicamente con tu propia copia de GTA V y su actualización legítima.
- El objetivo declarado del proyecto es PS3, Europa, título `NPEB01283`; la actualización 1.27 sigue pendiente de confirmación.
- No descargues ni compartas un `update.rpf` de terceros.
- No subas al repositorio archivos del juego, ejecutables, licencias, RAP/RIF, EBOOT ni paquetes del juego.
- No reemplaces archivos originales. Conserva una copia de seguridad aparte.

## Qué necesitamos comprobar

1. En la PS3, confirmar que el juego instalado es el título europeo `NPEB01283`.
2. Confirmar la versión de actualización que realmente está instalada. No asumir 1.27 por el nombre de un archivo.
3. Preparar, en un ordenador, una carpeta de trabajo con los recursos de tu propia instalación que hayas extraído con herramientas compatibles.
4. Ejecutar el inventario de solo lectura descrito abajo.
5. Compartir únicamente el informe JSON resultante, nunca los archivos RPF/CTD/GFX del juego.

## Ejecutar el inventario en Windows

1. Descarga el repositorio desde GitHub como ZIP y descomprímelo.
2. Abre la carpeta `GTA5-GTA6-PS3-MOD/tools`.
3. En el Explorador de archivos, haz clic en la barra de dirección, escribe `cmd` y pulsa Enter.
4. Ejecuta el inventario indicando la carpeta de trabajo que contiene los recursos ya extraídos:

```bat
python inventory_game_resources.py "C:\\GTA5-PS3-RECURSOS" -o "resource-inventory.json"
```

5. El programa crea `resource-inventory.json` con rutas relativas, tamaños, los primeros 16 bytes en hexadecimal y hashes SHA-256 de los archivos candidatos.
6. Abre ese JSON y comprueba que solo contiene metadatos. Ese informe es lo único que debes compartir para que podamos revisar la estructura.

Si Windows dice que `python` no se reconoce, instala Python desde su sitio oficial o usa un ordenador que ya tenga Python 3. No ejecutes archivos desconocidos descargados de páginas de mods.

## Ejecutar el inventario en Linux

Desde la carpeta `tools`:

```sh
python3 inventory_game_resources.py "/ruta/a/tu/carpeta-de-recursos" -o resource-inventory.json
```

## Qué hace y qué no hace la herramienta

**Sí hace:**
- Busca archivos con extensiones RPF, CTD y GFX, además de `hudcolor.dat`.
- Registra ruta relativa, tamaño, los primeros 16 bytes como huella hexadecimal y SHA-256.
- Evita seguir enlaces simbólicos.
- No escribe dentro de la carpeta de recursos.\n- No interpreta esa huella como prueba de compatibilidad: solo permite comparar cabeceras y reconocer candidatos.

**No hace:**
- No extrae ni abre archivos RPF.
- No descifra archivos.
- No identifica por sí sola la versión instalada.
- No convierte SVG a CTD ni crea recursos Scaleform/GFX.
- No instala nada ni genera un PKG.

## Qué sigue después del informe

Con el inventario y la versión confirmada se podrá decidir qué recurso estudiar primero. La primera prueba deberá ser pequeña, reversible y sobre una copia de trabajo. No se tocará el juego original hasta demostrar que el formato se puede reconstruir sin errores.

## Capturas e instrucciones visuales

Las capturas paso a paso para la instalación final se prepararán cuando exista un instalador real y se haya verificado el procedimiento en PS3 HEN. No sería correcto inventar capturas de una instalación que todavía no existe.
