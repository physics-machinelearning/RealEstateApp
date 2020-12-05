from django.forms import ModelForm

from realestate.models import SearchCondition


class SearchConditionForm(ModelForm):
    class Meta:
        model = SearchCondition
        fields = ('min_rent', 'max_rent', 'floor_plan', 'min_area', 'bath_toilet', 'autolock')
        labels = {
            'min_rent': '家賃下限(万円)',
            'max_rent': '家賃上限(万円）',
            'floor_plan': '間取り',
            'min_area': '占有面積下限',
            'bath_toilet': 'バストイレ',
            'autolock': 'オートロック'
        }