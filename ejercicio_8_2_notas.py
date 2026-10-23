import math
import re
import tkinter as tk
from tkinter import messagebox, ttk


class Notas:

    CANTIDAD_NOTAS = 5

    def __init__(self):

        self.__lista_notas = [0.0] * Notas.CANTIDAD_NOTAS

    def get_lista_notas(self) -> list:
        return list(self.__lista_notas)

    def set_nota(self, indice: int, valor: float) -> None:
        self.__lista_notas[indice] = valor

    def calcular_promedio(self) -> float:
        return sum(self.__lista_notas) / len(self.__lista_notas)

    def calcular_desviacion(self) -> float:
        promedio = self.calcular_promedio()
        suma = 0.0
        for nota in self.__lista_notas:
            suma += math.pow(nota - promedio, 2)
        return math.sqrt(suma / len(self.__lista_notas))

    def calcular_menor(self) -> float:
        menor = self.__lista_notas[0]
        for nota in self.__lista_notas:
            if nota < menor:
                menor = nota
        return menor

    def calcular_mayor(self) -> float:
        mayor = self.__lista_notas[0]
        for nota in self.__lista_notas:
            if nota > mayor:
                mayor = nota
        return mayor


class VentanaPrincipal(tk.Tk):


    _PATRON_NUMERO = re.compile(r"[+-]?(\d+([.,]\d*)?|[.,]\d+)")

    def __init__(self):
        super().__init__()
        self.__campos_nota = []
        self.__etiqueta_promedio = None
        self.__etiqueta_desviacion = None
        self.__etiqueta_mayor = None
        self.__etiqueta_menor = None
        self.__inicio()
        self.title("Notas")
        self.resizable(False, False)
        self.__centrar_en_pantalla()

    def __inicio(self) -> None:
        estilo = ttk.Style(self)
        if estilo.theme_use() == "default":
            estilo.theme_use("clam")

        contenedor = ttk.Frame(self, padding=20)
        contenedor.grid()


        for i in range(Notas.CANTIDAD_NOTAS):
            etiqueta = ttk.Label(contenedor, text=f"Nota {i + 1}:")
            etiqueta.grid(row=i, column=0, sticky="w", pady=4)
            campo = ttk.Entry(contenedor, width=18)
            campo.grid(row=i, column=1, padx=(12, 0), pady=4)
            self.__campos_nota.append(campo)


        botones = ttk.Frame(contenedor)
        botones.grid(row=Notas.CANTIDAD_NOTAS, column=0, columnspan=2, pady=(12, 6))
        calcular = ttk.Button(botones, text="Calcular", command=self.__al_calcular)
        calcular.grid(row=0, column=0, padx=(0, 8))
        limpiar = ttk.Button(botones, text="Limpiar", command=self.__al_limpiar)
        limpiar.grid(row=0, column=1)
        self.bind("<Return>", lambda evento: self.__al_calcular())

        ttk.Separator(contenedor).grid(
            row=Notas.CANTIDAD_NOTAS + 1, column=0, columnspan=2, sticky="ew", pady=8)


        fila = Notas.CANTIDAD_NOTAS + 2
        self.__etiqueta_promedio = ttk.Label(contenedor)
        self.__etiqueta_desviacion = ttk.Label(contenedor)
        self.__etiqueta_mayor = ttk.Label(contenedor)
        self.__etiqueta_menor = ttk.Label(contenedor)
        for etiqueta in (self.__etiqueta_promedio, self.__etiqueta_desviacion,
                         self.__etiqueta_mayor, self.__etiqueta_menor):
            etiqueta.grid(row=fila, column=0, columnspan=2, sticky="w", pady=3)
            fila += 1
        self.__borrar_resultados()

    def __centrar_en_pantalla(self) -> None:
        self.update_idletasks()
        ancho = self.winfo_reqwidth()
        alto = self.winfo_reqheight()
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"+{x}+{y}")


    @staticmethod
    def validar_textos(textos: list) -> tuple:
        notas = []
        faltantes = []
        invalidas = []
        for numero, texto in enumerate(textos, start=1):
            texto = texto.strip()
            if texto == "":
                faltantes.append(numero)
            elif VentanaPrincipal._PATRON_NUMERO.fullmatch(texto):
                notas.append(float(texto.replace(",", ".")))
            else:
                invalidas.append(numero)
        return notas, faltantes, invalidas

    def __mostrar_alerta(self, faltantes: list, invalidas: list) -> None:
        mensajes = []
        if faltantes:
            nombres = ", ".join(f"Nota {n}" for n in faltantes)
            mensajes.append(f"Debe ingresar las cinco notas. Falta: {nombres}.")
        if invalidas:
            nombres = ", ".join(f"Nota {n}" for n in invalidas)
            mensajes.append(f"El valor no es numérico en: {nombres}. "
                            "Use solo números (por ejemplo 4.5).")
        primer_error = min(faltantes + invalidas)
        messagebox.showwarning("Datos incorrectos", "\n\n".join(mensajes), parent=self)
        self.__campos_nota[primer_error - 1].focus_set()


    def __al_calcular(self) -> None:
        textos = [campo.get() for campo in self.__campos_nota]
        valores, faltantes, invalidas = self.validar_textos(textos)
        if faltantes or invalidas:
            self.__borrar_resultados()
            self.__mostrar_alerta(faltantes, invalidas)
            return

        notas = Notas()
        for indice, valor in enumerate(valores):
            notas.set_nota(indice, valor)

        self.__etiqueta_promedio.config(
            text=f"Promedio = {notas.calcular_promedio():.2f}")
        self.__etiqueta_desviacion.config(
            text=f"Desviación estándar = {notas.calcular_desviacion():.2f}")
        self.__etiqueta_mayor.config(
            text=f"Nota mayor = {notas.calcular_mayor():.2f}")
        self.__etiqueta_menor.config(
            text=f"Nota menor = {notas.calcular_menor():.2f}")

    def __al_limpiar(self) -> None:
        for campo in self.__campos_nota:
            campo.delete(0, tk.END)
        self.__borrar_resultados()
        self.__campos_nota[0].focus_set()

    def __borrar_resultados(self) -> None:
        self.__etiqueta_promedio.config(text="Promedio = ")
        self.__etiqueta_desviacion.config(text="Desviación estándar = ")
        self.__etiqueta_mayor.config(text="Nota mayor = ")
        self.__etiqueta_menor.config(text="Nota menor = ")


class Principal:

    @staticmethod
    def main() -> None:
        mi_ventana_principal = VentanaPrincipal()
        mi_ventana_principal.mainloop()


if __name__ == "__main__":
    Principal.main()
