from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner


class GallinasApp(App):

    def build(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 🔹 FORMULARIO
        grid = GridLayout(cols=2, spacing=12, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        def fila(texto, widget):
            label = Label(text=texto, size_hint_x=0.6, halign="left")
            label.bind(size=label.setter('text_size'))

            widget.size_hint_x = 0.4
            widget.size_hint_y = None
            widget.height = 42

            grid.add_widget(label)
            grid.add_widget(widget)

        # Entradas
        self.gallinas = TextInput(input_filter="int")
        fila("Número de gallinas", self.gallinas)

        self.edad = TextInput(input_filter="int")
        fila("Edad (días)", self.edad)

        self.alimento = TextInput(input_filter="float")
        fila("Alimento (g/día)", self.alimento)

        self.precio_alimento = TextInput(input_filter="float")
        fila("Precio concentrado ($/kg)", self.precio_alimento)

        self.agua = TextInput(input_filter="float")
        fila("Agua (ml/día)", self.agua)

        self.precio_huevo = TextInput(input_filter="float")
        fila("Precio por huevo ($)", self.precio_huevo)

        self.tipo = Spinner(
            text="Media",
            values=("Alta producción", "Media", "Baja"),
            size_hint_y=None,
            height=42
        )
        fila("Tipo de gallina", self.tipo)

        self.dias = TextInput(input_filter="int")
        fila("Días (máx 365)", self.dias)

        root.add_widget(grid)

        # 🔘 BOTÓN
        self.btn = Button(text="Calcular", size_hint_y=None, height=60)
        self.btn.bind(on_press=self.calcular)
        root.add_widget(self.btn)

        # 📊 RESULTADO
        self.resultado = Label(
            text="",
            size_hint_y=1,
            halign="left",
            valign="top"
        )
        self.resultado.bind(size=self.resultado.setter('text_size'))

        root.add_widget(self.resultado)

        return root

    def calcular(self, instance):
        try:
            gallinas = int(self.gallinas.text)
            edad_dias = int(self.edad.text)
            alimento = float(self.alimento.text)
            precio_alimento = float(self.precio_alimento.text)
            agua = float(self.agua.text)
            precio_huevo = float(self.precio_huevo.text)
            dias = int(self.dias.text)
            tipo = self.tipo.text

            if gallinas <= 0 or alimento <= 0 or dias <= 0:
                self.resultado.text = "Valores inválidos"
                return

            if dias > 365:
                self.resultado.text = "Máx 365 días"
                return

            edad_semanas = edad_dias / 7

            if edad_semanas < 18:
                total_huevos = 0
                huevos_dia = 0
            else:
                if tipo == "Alta producción":
                    postura = 0.9
                elif tipo == "Media":
                    postura = 0.75
                else:
                    postura = 0.6

                total_huevos = 0

                for dia in range(dias):
                    factor = max(0.7, 1 - (0.001 * dia))
                    huevos = round(gallinas * postura * factor)
                    total_huevos += huevos

                huevos_dia = round(total_huevos / dias)

            # 🔹 Consumos
            alimento_total = round((alimento * gallinas * dias) / 1000, 2)
            agua_total = round((agua * gallinas * dias) / 1000, 2)

            # 🔹 Economía (sin decimales)
            costo_alimento = int(alimento_total * precio_alimento)
            ingreso_total_huevos = int(total_huevos * precio_huevo)

            # Resultado limpio
            self.resultado.text = (
                f"Huevos por día: {huevos_dia}\n"
                f"Huevos totales: {total_huevos}\n"
                f"Valor total huevos: ${ingreso_total_huevos}\n\n"
                f"Alimento total: {alimento_total} kg\n"
                f"Costo alimento: ${costo_alimento}\n"
                f"Agua total: {agua_total} L"
            )

        except:
            self.resultado.text = "Error en datos"


if __name__ == "__main__":
    GallinasApp().run()