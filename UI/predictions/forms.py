from django import forms

class PredictionForm(forms.Form):
    clasificacion_general = forms.IntegerField(label='Clasificación general del inmueble', min_value=1, max_value=10)
    numero_de_recamaras = forms.IntegerField(label='Número de recámaras', min_value=0)
    clasificacion_zona = forms.IntegerField(label='Clasificación de la zona', min_value=1, max_value=5)
    superficie_construida = forms.FloatField(label='Superficie construida (m²)')
    superficie_lote = forms.FloatField(label='Superficie del lote (m²)')
    numero_de_banos = forms.IntegerField(label='Número de baños', min_value=1)
    edad_del_inmueble = forms.IntegerField(label='Edad del inmueble (años)')
    fecha_de_venta = forms.IntegerField(label='Año de la venta', min_value=2000, max_value=2024)

    class Meta:
        fields = ['clasificacion_general', 'numero_de_recamaras', 'clasificacion_zona', 'superficie_construida', 'superficie_lote', 'numero_de_banos', 'edad_del_inmueble', 'fecha_de_venta']
