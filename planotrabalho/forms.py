from django.forms import ModelForm

from .models import CriacaoSistema, OrgaoGestor, ConselhoCultural
from .models import FundoCultura, PlanoCultura


class CriarSistemaForm(ModelForm):
    class Meta:
        model = CriacaoSistema
        fields = '__all__'


class OrgaoGestorForm(ModelForm):
    class Meta:
        model = OrgaoGestor
        fields = '__all__'


class ConselhoCulturalForm(ModelForm):
    class Meta:
        model = ConselhoCultural
        fields = '__all__'


class FundoCulturaForm(ModelForm):
    class Meta:
        model = FundoCultura
        fields = '__all__'


class PlanoCulturaForm(ModelForm):
    class Meta:
        model = PlanoCultura
        fields = '__all__'
