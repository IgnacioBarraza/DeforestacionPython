import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

sns.set(style="whitegrid")

class DeforestacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Deforestación - Tamarugal y Pica")
        self.data = None
        self.freq_table = None
        self.stats_table = None
        self.mensual = None

        self.build_gui()

    def build_gui(self):
        tk.Button(self.root, text="Cargar Excel", command=self.cargar_excel).pack(pady=5)

        self.tree = ttk.Treeview(self.root)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Guardar Resultados", command=self.guardar_resultados).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Gráfico de Frecuencia", command=self.graficar_frecuencias).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Análisis Mensual", command=self.analisis_mensual).grid(row=0, column=2, padx=5)

    def cargar_excel(self):
        path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not path:
            return

        try:
            self.data = pd.read_excel(path)

            # Verifica columnas esenciales
            columnas_necesarias = {'Tipo_Arbol', 'Cantidad', 'Fecha'}
            if not columnas_necesarias.issubset(self.data.columns):
                raise ValueError(f"El archivo debe contener las columnas: {columnas_necesarias}")

            self.generar_tabla_frecuencia()
            self.calcular_estadisticas()
            self.mostrar_en_treeview(self.freq_table, "Tabla de Frecuencia")
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    def generar_tabla_frecuencia(self):
        self.freq_table = self.data['Tipo_Arbol'].value_counts().reset_index()
        self.freq_table.columns = ['Tipo_Arbol', 'Frecuencia']

    def calcular_estadisticas(self):
        agrupado = self.data.groupby('Tipo_Arbol')['Cantidad']

        moda_dict = agrupado.apply(lambda x: stats.mode(x, keepdims=True).mode[0]).to_dict()

        estadisticas = agrupado.agg(['mean', 'median', 'std', 'var']).reset_index()
        estadisticas["Moda"] = estadisticas["Tipo_Arbol"].map(moda_dict)

        self.stats_table = estadisticas[["Tipo_Arbol", "mean", "median", "Moda", "std", "var"]]
        self.stats_table.columns = ['Tipo_Arbol', 'Media', 'Mediana', 'Moda', 'Desv.Std', 'Varianza']

    def mostrar_en_treeview(self, df, titulo="Resultados"):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def guardar_resultados(self):
        if self.freq_table is None:
            messagebox.showwarning("Advertencia", "Primero debes cargar un archivo.")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if not ruta:
            return

        try:
            with pd.ExcelWriter(ruta) as writer:
                self.freq_table.to_excel(writer, sheet_name="Frecuencias", index=False)
                self.stats_table.to_excel(writer, sheet_name="Estadísticas", index=False)
                if self.mensual is not None:
                    self.mensual.to_excel(writer, sheet_name="Mensual", index=False)
            messagebox.showinfo("Éxito", "Archivo guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def graficar_frecuencias(self):
        if self.freq_table is None:
            return
        plt.figure(figsize=(10, 6))
        sns.barplot(data=self.freq_table, x="Tipo_Arbol", y="Frecuencia", palette="Greens_r")
        plt.title("Frecuencia por Tipo de Árbol")
        plt.xlabel("Tipo de Árbol")
        plt.ylabel("Frecuencia")
        for i, row in self.freq_table.iterrows():
            plt.text(i, row["Frecuencia"] + 0.2, str(row["Frecuencia"]), ha="center")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def analisis_mensual(self):
        if self.data is None:
            return

        df = self.data.copy()
        df['Mes'] = pd.to_datetime(df['Fecha']).dt.month
        self.mensual = df.groupby(['Mes', 'Tipo_Arbol'])['Cantidad'].sum().reset_index()

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=self.mensual, x="Mes", y="Cantidad", hue="Tipo_Arbol", marker="o")
        plt.title("Cantidad de árboles talados por mes - 2024")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad")
        plt.xticks(range(1, 13))
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = DeforestacionApp(root)
    root.mainloop()
