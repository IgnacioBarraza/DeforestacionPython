# Análisis de Deforestación - Tamarugal y Pica 🌳

Este proyecto permite analizar datos de deforestación en la región de Tamarugal y Pica durante el año 2024.  
Incluye análisis estadístico, gráficos y una interfaz gráfica para facilitar la carga y visualización de datos.

---

## 👨‍💻 Autores

- Ignacio Barraza  
- Orlando Rojo

---

## 🚀 Instrucciones para clonar y ejecutar

1. **Clonar el repositorio**

```bash
git clone https://github.com/IgnacioBarraza/DeforestacionPython.git
cd DeforestacionPython
````

2. **Crear entorno virtual (opcional pero recomendado)**

```bash
python3 -m venv .venv
source .venv/bin/activate   # En Linux/macOS
# o
.venv\Scripts\activate      # En Windows
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Ejecutar el programa**

```bash
python deforestacion.py
```

---

## 📁 Requisitos del archivo Excel

El programa espera que el archivo Excel tenga las siguientes columnas:

* `Tipo_Arbol`
* `Cantidad`
* `Fecha`

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**, lo que significa que es de **código abierto y libre de uso**, siempre y cuando se mencione a los autores.

---

## 📝 Notas

* Desarrollado como parte de la asignatura de Inteligencia de Negocios.
* Se utilizó Python, pandas, matplotlib, seaborn, scipy y tkinter.
