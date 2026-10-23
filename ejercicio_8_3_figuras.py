import math
import re
import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox, ttk


class FiguraGeometrica(ABC):

    def __init__(self):
        self.__volumen = 0.0
        self.__superficie = 0.0

    def set_volumen(self, volumen: float) -> None:
        self.__volumen = volumen

    def set_superficie(self, superficie: float) -> None:
        self.__superficie = superficie

    def get_volumen(self) -> float:
        return self.__volumen

    def get_superficie(self) -> float:
        return self.__superficie

    @abstractmethod
    def calcular_volumen(self) -> float:
        pass

    @abstractmethod
    def calcular_superficie(self) -> float:
        pass

    @staticmethod
    def _validar_positivo(nombre: str, valor: float) -> None:
        if valor <= 0:
            raise ValueError(f"{nombre} debe ser mayor que cero.")


class Cilindro(FiguraGeometrica):
    def __init__(self, radio: float, altura: float):
        super().__init__()
        self._validar_positivo("El radio", radio)
        self._validar_positivo("La altura", altura)
        self.__radio = radio
        self.__altura = altura
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return math.pi * self.__altura * math.pow(self.__radio, 2)

    def calcular_superficie(self) -> float:
        area_lado_a = 2 * math.pi * self.__radio * self.__altura
        area_lado_b = 2 * math.pi * math.pow(self.__radio, 2)
        return area_lado_a + area_lado_b


class Esfera(FiguraGeometrica):
    def __init__(self, radio: float):
        super().__init__()
        self._validar_positivo("El radio", radio)
        self.__radio = radio
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return (4 / 3) * math.pi * math.pow(self.__radio, 3)

    def calcular_superficie(self) -> float:
        return 4 * math.pi * math.pow(self.__radio, 2)


class Piramide(FiguraGeometrica):

    def __init__(self, base: float, altura: float, apotema: float):
        super().__init__()
        self._validar_positivo("La base", base)
        self._validar_positivo("La altura", altura)
        self._validar_positivo("El apotema", apotema)
        self.__base = base
        self.__altura = altura
        self.__apotema = apotema
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return (math.pow(self.__base, 2) * self.__altura) / 3

    def calcular_superficie(self) -> float:
        area_base = math.pow(self.__base, 2)
        area_lados = 2 * self.__base * self.__apotema
        return area_base + area_lados


class Cubo(FiguraGeometrica):

    def __init__(self, arista: float):
        super().__init__()
        self._validar_positivo("La arista", arista)
        self.__arista = arista
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return math.pow(self.__arista, 3)

    def calcular_superficie(self) -> float:
        return 6 * math.pow(self.__arista, 2)


class Prisma(FiguraGeometrica):

    def __init__(self, largo: float, ancho: float, alto: float):
        super().__init__()
        self._validar_positivo("El largo", largo)
        self._validar_positivo("El ancho", ancho)
        self._validar_positivo("El alto", alto)
        self.__largo = largo
        self.__ancho = ancho
        self.__alto = alto
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self) -> float:
        return self.__largo * self.__ancho * self.__alto

    def calcular_superficie(self) -> float:
        return 2 * (self.__largo * self.__ancho
                    + self.__largo * self.__alto
                    + self.__ancho * self.__alto)


COLOR_LADO = "#9ec5e8"
COLOR_TAPA = "#cfe3f5"
COLOR_SOMBRA = "#6fa3d4"
COLOR_LINEA = "#1f4e79"
COLOR_OCULTA = "#4a6785"
COLOR_MEDIDA = "#c0392b"


def aplicar_estilo(ventana: tk.Misc) -> None:
    estilo = ttk.Style(ventana)
    if estilo.theme_use() == "default":
        estilo.theme_use("clam")


class VentanaFigura(tk.Toplevel, ABC):

    TITULO = ""
    CAMPOS = []
    _PATRON_NUMERO = re.compile(r"[+-]?(\d+([.,]\d*)?|[.,]\d+)")

    def __init__(self, padre: tk.Misc):
        super().__init__(padre)
        self.__campos_texto = []
        self.__etiqueta_volumen = None
        self.__etiqueta_superficie = None
        self.__inicio()
        self.title(self.TITULO)
        self.resizable(False, False)
        self.__ubicar_respecto_a(padre)

    @abstractmethod
    def crear_figura(self, valores: list) -> FiguraGeometrica:
        pass

    @abstractmethod
    def dibujar(self, lienzo: tk.Canvas) -> None:
        pass

    def __inicio(self) -> None:
        aplicar_estilo(self)
        contenedor = ttk.Frame(self, padding=16)
        contenedor.grid()

        formulario = ttk.Frame(contenedor)
        formulario.grid(row=0, column=0, sticky="n")
        for i, nombre in enumerate(self.CAMPOS):
            ttk.Label(formulario, text=f"{nombre} (cm):").grid(
                row=i, column=0, sticky="w", pady=4)
            campo = ttk.Entry(formulario, width=12)
            campo.grid(row=i, column=1, padx=(10, 0), pady=4)
            self.__campos_texto.append(campo)

        fila = len(self.CAMPOS)
        calcular = ttk.Button(formulario, text="Calcular", command=self.__al_calcular)
        calcular.grid(row=fila, column=0, columnspan=2, sticky="ew", pady=(8, 10))
        self.bind("<Return>", lambda evento: self.__al_calcular())

        self.__etiqueta_volumen = ttk.Label(formulario)
        self.__etiqueta_volumen.grid(row=fila + 1, column=0, columnspan=2, sticky="w", pady=3)
        self.__etiqueta_superficie = ttk.Label(formulario)
        self.__etiqueta_superficie.grid(row=fila + 2, column=0, columnspan=2, sticky="w", pady=3)
        self.__borrar_resultados()


        lienzo = tk.Canvas(contenedor, width=180, height=170, bg="white",
                           highlightthickness=1, highlightbackground="#b0b0b0")
        lienzo.grid(row=0, column=1, padx=(18, 0), sticky="n")
        self.dibujar(lienzo)

        self.__campos_texto[0].focus_set()

    def __ubicar_respecto_a(self, padre: tk.Misc) -> None:
        self.update_idletasks()
        x = padre.winfo_x() + 30
        y = padre.winfo_y() + 60
        self.geometry(f"+{x}+{y}")

    def __leer_valor(self, nombre: str, texto: str) -> float:
        texto = texto.strip()
        if texto == "":
            raise ValueError(f"Campo nulo: ingrese el valor de «{nombre}».")
        if not self._PATRON_NUMERO.fullmatch(texto):
            raise ValueError(f"Error en formato de número en «{nombre}»: "
                             f"'{texto}' no es un número válido.")
        return float(texto.replace(",", "."))

    def __al_calcular(self) -> None:
        try:
            valores = [self.__leer_valor(nombre, campo.get())
                       for nombre, campo in zip(self.CAMPOS, self.__campos_texto)]
            figura = self.crear_figura(valores)
        except ValueError as error:
            self.__borrar_resultados()
            messagebox.showerror("Error", str(error), parent=self)
            return
        self.__etiqueta_volumen.config(text=f"Volumen (cm³): {figura.get_volumen():.2f}")
        self.__etiqueta_superficie.config(
            text=f"Superficie (cm²): {figura.get_superficie():.2f}")

    def __borrar_resultados(self) -> None:
        self.__etiqueta_volumen.config(text="Volumen (cm³):")
        self.__etiqueta_superficie.config(text="Superficie (cm²):")


    @staticmethod
    def _etiqueta_medida(lienzo: tk.Canvas, x: int, y: int, texto: str) -> None:
        lienzo.create_text(x, y, text=texto, fill=COLOR_MEDIDA,
                           font=("TkDefaultFont", 9, "bold"))

    @staticmethod
    def _dibujar_caja(lienzo: tk.Canvas, x0: int, y0: int, x1: int, y1: int,
                      dx: int, dy: int) -> None:

        lienzo.create_rectangle(x0, y0, x1, y1, fill=COLOR_LADO, outline=COLOR_LINEA)
        lienzo.create_polygon(x0, y0, x1, y0, x1 + dx, y0 + dy, x0 + dx, y0 + dy,
                              fill=COLOR_TAPA, outline=COLOR_LINEA)
        lienzo.create_polygon(x1, y0, x1 + dx, y0 + dy, x1 + dx, y1 + dy, x1, y1,
                              fill=COLOR_SOMBRA, outline=COLOR_LINEA)

        oculta = dict(fill=COLOR_OCULTA, dash=(3, 3))
        lienzo.create_line(x0, y1, x0 + dx, y1 + dy, **oculta)
        lienzo.create_line(x0 + dx, y1 + dy, x1 + dx, y1 + dy, **oculta)
        lienzo.create_line(x0 + dx, y1 + dy, x0 + dx, y0 + dy, **oculta)


class VentanaCilindro(VentanaFigura):
    TITULO = "Cilindro"
    CAMPOS = ["Radio", "Altura"]

    def crear_figura(self, valores: list) -> FiguraGeometrica:
        return Cilindro(valores[0], valores[1])

    def dibujar(self, lienzo: tk.Canvas) -> None:
        lienzo.create_oval(30, 115, 140, 145, fill=COLOR_LADO, outline=COLOR_LINEA)
        lienzo.create_rectangle(30, 40, 140, 130, fill=COLOR_LADO, outline=COLOR_LADO)
        lienzo.create_line(30, 40, 30, 130, fill=COLOR_LINEA)
        lienzo.create_line(140, 40, 140, 130, fill=COLOR_LINEA)
        lienzo.create_oval(30, 25, 140, 55, fill=COLOR_TAPA, outline=COLOR_LINEA)

        lienzo.create_line(85, 40, 140, 40, fill=COLOR_MEDIDA, dash=(3, 2))
        self._etiqueta_medida(lienzo, 112, 50, "r")
        lienzo.create_line(160, 40, 160, 130, fill=COLOR_MEDIDA, arrow=tk.BOTH)
        self._etiqueta_medida(lienzo, 170, 85, "h")


class VentanaEsfera(VentanaFigura):
    TITULO = "Esfera"
    CAMPOS = ["Radio"]

    def crear_figura(self, valores: list) -> FiguraGeometrica:
        return Esfera(valores[0])

    def dibujar(self, lienzo: tk.Canvas) -> None:
        lienzo.create_oval(35, 30, 145, 140, fill=COLOR_LADO, outline=COLOR_LINEA)
        lienzo.create_oval(55, 45, 85, 70, fill=COLOR_TAPA, outline="")
        lienzo.create_oval(35, 70, 145, 100, outline=COLOR_OCULTA, dash=(3, 3))
        lienzo.create_line(90, 85, 145, 85, fill=COLOR_MEDIDA)
        lienzo.create_oval(87, 82, 93, 88, fill=COLOR_MEDIDA, outline=COLOR_MEDIDA)
        self._etiqueta_medida(lienzo, 118, 77, "r")


class VentanaPiramide(VentanaFigura):
    TITULO = "Pirámide"
    CAMPOS = ["Base", "Altura", "Apotema"]

    def crear_figura(self, valores: list) -> FiguraGeometrica:
        return Piramide(valores[0], valores[1], valores[2])

    def dibujar(self, lienzo: tk.Canvas) -> None:
        cima = (88, 22)
        frente_izq, frente_der = (26, 130), (115, 130)
        fondo_der, fondo_izq = (150, 108), (61, 108)
        lienzo.create_polygon(*frente_izq, *frente_der, *cima,
                              fill=COLOR_LADO, outline=COLOR_LINEA)
        lienzo.create_polygon(*frente_der, *fondo_der, *cima,
                              fill=COLOR_SOMBRA, outline=COLOR_LINEA)
        oculta = dict(fill=COLOR_OCULTA, dash=(3, 3))
        lienzo.create_line(*frente_izq, *fondo_izq, **oculta)
        lienzo.create_line(*fondo_izq, *fondo_der, **oculta)
        lienzo.create_line(*fondo_izq, *cima, **oculta)

        lienzo.create_line(*cima, 88, 119, fill=COLOR_MEDIDA, dash=(3, 2))
        self._etiqueta_medida(lienzo, 95, 75, "h")
        lienzo.create_line(*cima, 70, 130, fill=COLOR_MEDIDA)
        self._etiqueta_medida(lienzo, 62, 85, "ap")
        self._etiqueta_medida(lienzo, 70, 142, "b")


class VentanaCubo(VentanaFigura):
    TITULO = "Cubo"
    CAMPOS = ["Arista"]

    def crear_figura(self, valores: list) -> FiguraGeometrica:
        return Cubo(valores[0])

    def dibujar(self, lienzo: tk.Canvas) -> None:
        self._dibujar_caja(lienzo, 25, 65, 105, 145, 40, -40)
        self._etiqueta_medida(lienzo, 65, 158, "a")


class VentanaPrisma(VentanaFigura):
    TITULO = "Prisma rectangular"
    CAMPOS = ["Largo", "Ancho", "Alto"]

    def crear_figura(self, valores: list) -> FiguraGeometrica:
        return Prisma(valores[0], valores[1], valores[2])

    def dibujar(self, lienzo: tk.Canvas) -> None:
        self._dibujar_caja(lienzo, 32, 80, 112, 145, 28, -28)
        self._etiqueta_medida(lienzo, 72, 158, "largo")
        self._etiqueta_medida(lienzo, 16, 112, "alto")
        self._etiqueta_medida(lienzo, 158, 62, "ancho")


class VentanaPrincipal(tk.Tk):

    FIGURAS = [("Cilindro", VentanaCilindro),
               ("Esfera", VentanaEsfera),
               ("Pirámide", VentanaPiramide),
               ("Cubo", VentanaCubo),
               ("Prisma", VentanaPrisma)]

    def __init__(self):
        super().__init__()
        self.__ventanas_abiertas = {}
        self.__inicio()
        self.title("Figuras")
        self.resizable(False, False)
        self.__centrar_en_pantalla()

    def __inicio(self) -> None:
        aplicar_estilo(self)
        contenedor = ttk.Frame(self, padding=20)
        contenedor.grid()
        ttk.Label(contenedor, text="Seleccione una figura geométrica:").grid(
            row=0, column=0, columnspan=len(self.FIGURAS), pady=(0, 14))
        for columna, (texto, clase_ventana) in enumerate(self.FIGURAS):
            boton = ttk.Button(contenedor, text=texto, width=10,
                               command=lambda c=clase_ventana: self.__al_pulsar_figura(c))
            boton.grid(row=1, column=columna, padx=4)

    def __centrar_en_pantalla(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 3
        self.geometry(f"+{x}+{y}")

    def __al_pulsar_figura(self, clase_ventana: type) -> None:
        ventana = self.__ventanas_abiertas.get(clase_ventana)
        if ventana is not None and ventana.winfo_exists():
            ventana.deiconify()
            ventana.lift()
            ventana.focus_force()
        else:
            self.__ventanas_abiertas[clase_ventana] = clase_ventana(self)


class Principal:

    @staticmethod
    def main() -> None:
        mi_ventana_principal = VentanaPrincipal()
        mi_ventana_principal.mainloop()


if __name__ == "__main__":
    Principal.main()
