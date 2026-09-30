---
description: Construye un notebook Jupyter desde cero y publica un visor HTML interactivo para revisarlo
---

Quiero que construyas un notebook de Jupyter (`.ipynb`) desde cero sobre: $ARGUMENTS

**Para el notebook:**
1. Estructúralo en secciones claras con celdas markdown de título antes de cada bloque de código (Introducción, Carga de datos, Análisis, Resultados, Conclusiones — ajusta según el tema).
2. Cada celda de código debe ejecutarse y producir su output real (tablas, gráficas, prints) antes de guardarlo — no dejes celdas sin ejecutar.
3. Usa buenas prácticas: imports al principio, funciones documentadas con un comentario breve si algo no es obvio, nombres de variables claros.
4. Guarda el notebook como `.ipynb` en el repo/carpeta de trabajo.

**Para visualizarlo (estilo lector de PDF, no carrusel de tarjetas):**
5. Exporta el notebook a HTML (`jupyter nbconvert --to html --template classic`). Si tiene fórmulas LaTeX (`$...$` / `$$...$$`), renderízalas localmente a PNG con `matplotlib.mathtext` e insértalas inline antes de continuar — no dependas de MathJax por CDN (puede no haber red). Al hacer el reemplazo por regex, descarta cualquier coincidencia que contenga una etiqueta HTML (`<`/`>`), salto de línea, o sea demasiado larga: evita que dos signos `$` sueltos de texto normal (p. ej. dos menciones de "$100,000") se emparejen por error.
6. Inyecta CSS de impresión que (a) evite que las celdas se corten entre páginas (`break-inside: avoid` en `.cell`), y (b) aplane el estilo "cuadriculado" por defecto de Jupyter (fondo gris y bordes duros en las celdas de código) por algo más limpio y con aspecto de papel impreso.
7. Genera un PDF real con Playwright (`page.pdf(width="8.5in", height="11in", print_background=True, ...)` tras `page.emulate_media(media="print")`) — esto pagina el contenido de verdad, como una impresión real.
8. Rasteriza cada página del PDF a PNG (con `pymupdf`/`fitz`, ~165 dpi) más una miniatura JPEG pequeña por página.
9. Construye un visor HTML autocontenido tipo lector de PDF: fondo gris, páginas blancas centradas en scroll vertical continuo (nunca una imagen a la vez con botones), riel de miniaturas fijo a la izquierda (oculto en móvil), barra superior con contador de página que se sincroniza al scroll (IntersectionObserver), y atajos de teclado (flechas arriba/abajo, Home/End) para saltar de página.
10. Publícalo como Artifact para tener un link que pueda abrir y compartir.

**Para cambios futuros:**
11. Cada vez que te pida modificar el notebook, aplica el cambio, vuelve a ejecutar el notebook completo, regenera las páginas, y republica el MISMO Artifact (mismo link, no uno nuevo).
12. Después de cada cambio, dime cuántas celdas/secciones tiene el notebook ahora, cuántas páginas generó el visor, y qué modificaste.
