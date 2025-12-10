from django import forms
from .models import Jugador, Torneo, Resultado, Contacto, Inscripcion, Partido

class FormJugador(forms.ModelForm):
    class Meta:
        model = Jugador
        # Excluir licencia antigua de la UI; requerir rut
        fields = ['nombre','apellido','categoria','rut']
        widgets = {
            'rut': forms.TextInput(attrs={'placeholder': '12.345.678-5'})
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            raise forms.ValidationError('El RUT es obligatorio.')
        return rut


class FormTorneo(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre','direccion','fecha','categoria','cupos_max','estado','numero_grupos']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }
        help_texts = {
            'numero_grupos': 'Cantidad de grupos para fase inicial (0 = sin grupos, directo a eliminación).'
        }


class FormResultado(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = ['torneo', 'jugador1', 'jugador2', 'marcador_j1', 'marcador_j2']
        widgets = {
            'marcador_j1': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'marcador_j2': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class FormContacto(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'


class FormInscripcion(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['torneo','jugador']


class FormPartido(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ['torneo','etapa','grupo','ronda','jugador_a','jugador_b','best_of','detalle_sets','sets_a','sets_b','marcador_a','marcador_b']
        widgets = {
            'detalle_sets': forms.TextInput(attrs={'placeholder': '11-7,8-11,11-9'}),
            'grupo': forms.TextInput(attrs={'placeholder': 'A'}),
            'sets_a': forms.NumberInput(attrs={'min': 0}),
            'sets_b': forms.NumberInput(attrs={'min': 0}),
            'marcador_a': forms.NumberInput(attrs={'min': 0}),
            'marcador_b': forms.NumberInput(attrs={'min': 0}),
        }
        help_texts = {
            'best_of': 'Usar 3 para grupos/eliminación y 5 para final.',
            'detalle_sets': 'Lista separada por comas de cada set: puntosA-puntosB.'
        }

    def clean(self):
        cleaned_data = super().clean()
        sets_a = cleaned_data.get('sets_a')
        sets_b = cleaned_data.get('sets_b')
        marcador_a = cleaned_data.get('marcador_a')
        marcador_b = cleaned_data.get('marcador_b')
        best_of = cleaned_data.get('best_of')
        
        if sets_a is not None and sets_a < 0:
            self.add_error('sets_a', 'Sets A no puede ser negativo.')
        if sets_b is not None and sets_b < 0:
            self.add_error('sets_b', 'Sets B no puede ser negativo.')
        if marcador_a is not None and marcador_a < 0:
            self.add_error('marcador_a', 'Marcador A no puede ser negativo.')
        if marcador_b is not None and marcador_b < 0:
            self.add_error('marcador_b', 'Marcador B no puede ser negativo.')
        
        # Validar lógica de sets según best_of
        if best_of and best_of > 1:
            max_sets = (best_of + 1) // 2  # Best of 3 = max 2 sets, Best of 5 = max 3 sets
            if sets_a is not None and sets_a > max_sets:
                self.add_error('sets_a', f'Para Best of {best_of}, el máximo de sets es {max_sets}.')
            if sets_b is not None and sets_b > max_sets:
                self.add_error('sets_b', f'Para Best of {best_of}, el máximo de sets es {max_sets}.')
        
        return cleaned_data


class BulkJugadorImportForm(forms.Form):
    archivo = forms.FileField(help_text="Archivo Excel .xlsx con columnas: nombre, apellido, categoria, rut")
