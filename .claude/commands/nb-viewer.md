---
description: Construye un notebook Jupyter desde cero y publica un visor HTML interactivo para revisarlo
---

Quiero que construyas un notebook de Jupyter (`.ipynb`) desde cero sobre: $ARGUMENTS

**Para el notebook:**
1. Estructúralo en secciones claras con celdas markdown de título antes de cada bloque de código (Introducción, Carga de datos, Análisis, Resultados, Conclusiones — ajusta según el tema).
2. Cada celda de código debe ejecutarse y producir su output real (tablas, gráficas, prints) antes de guardarlo — no dejes celdas sin ejecutar.
3. Usa buenas prácticas: imports al principio, funciones documentadas con un comentario breve si algo no es obvio, nombres de variables claros.
4. Guarda el notebook como `.ipynb` en el repo/carpeta de trabajo.

**Para visualizarlo:**
5. Renderiza el notebook completo a imágenes (una por celda relevante o por sección agrupada), en buena resolución.
6. Construye una página HTML autocontenida que embeba esas imágenes en base64, con navegación anterior/siguiente, atajos de teclado, tira de miniaturas y contador de página.
7. Publícalo como Artifact para tener un link que pueda abrir y compartir.

**Para cambios futuros:**
8. Cada vez que te pida modificar el notebook, aplica el cambio, vuelve a ejecutar el notebook completo, regenera las imágenes, y republica el MISMO Artifact (mismo link, no uno nuevo).
9. Después de cada cambio, dime cuántas celdas/secciones tiene el notebook ahora y cuáles modificaste.
