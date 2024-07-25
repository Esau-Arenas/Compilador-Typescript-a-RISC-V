<h1 align="center"> OLCSCRIP </h1>

<p align="center">
   <img src="https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green">
   </p>
<h3>UNIVERSIDAD DE SAN CARLOS DE GUATEMALA

LABORATORIO DE COMPILADORES 2
PRIMER SEMESTRE 2024</h3>

Se desarrollo un compilador para el lenguaje de programación OLCScript que abarca la fase
de análisis, comprendiendo la estructura del código fuente y aplicando la traducción dirigida
por la sintaxis utilizando herramientas adecuadas para la generación de analizadores
léxicos y sintácticos, además se genera una traducción equivalente en un lenguaje
ensamblador para la arquitectura RISC-V.

## 👀 Editor

El editor de código construye el núcleo del entorno de trabajo, permitiendo al
usuario ingresar y modificar el código fuente. Entre sus características destacadas
se incluyen:

#### Funcionalidades

* Creación de archivos en blanco.
* Apertura de archivos con extensión .olc.
* Guardado de archivos con extensión .olc.
* Soporte para múltiples archivos abiertos simultáneamente.
* Visualización de la línea actual en el código.
* Guardar traducción a Ensamblador.
* El usuario deberá de ser capaz de guardar la traducción generada en un archivo con extensión “.s” Ej: calculadora.s

#### Herramientas

Este conjunto de herramientas proporciona funcionalidades adicionales para facilitar el desarrollo y análisis del código OLCScript.

* Ejecución del Compilador: Llamada al compilador OLCScript para llevar a cabo los análisis léxico, sintáctico y semántico del código. Además deberá generar una traducción equivalente en código Assembler.

#### Reportes

* Reporte de Errores: Se muestran todos los errores encontrados al realizar el análisis léxico, sintáctico y semántico.
* Reporte de Tabla de Símbolos: Se muestran todas las variables, métodos y funciones que han sido declarados dentro del flujo del programa, así como el entorno en el que fueron declarados.

#### Consola

La consola proporciona un espacio dedicado para visualizar notificaciones, errores, advertencias e impresiones generadas durante el proceso de análisis del código de entrada.

* Impresión de Traducción a Ensamblador:
Después de completar la traducción del código OLCScript a código ensamblador
para la arquitectura RISC-V, la traducción resultante se imprimirá en la consola para
que el usuario pueda revisar y validar la salida.

## :smile:Tecnologias Utilizadas

* PLY
* Python3
* HTML
* Css
* Flask

**Acceder a configuraciones**
```python
enable
configure terminal
```

## ✒️ Autor

* **Alvaro Esaú Arenas** - *Desarrollador* - [Contacto](https://github.com/esau-arenas).