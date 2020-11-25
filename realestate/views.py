from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import render

from realestate.models import Rentproperty


CITY_LIST = [
    '中央区', '千代田区', '文京区', '港区', '新宿区', '品川区', '目黒区', '大田区', '世田谷区', 
    '渋谷区', '中野区', '杉並区', '練馬区', '板橋区', '豊島区', '北区',
    '台東区', '墨田区', '江東区', '荒川区', '足立区', '葛飾区', '江戸川区'
]


class EachCityView(ListView):
    model = Rentproperty
    template_name = "city.html"

    # def get_queryset(self):
    #     return Rentproperty.objects.order_by('rent_diff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = context['address']
        context['rentproperty'] = context['rentproperty']\
            .objects.filter(location__contains=city)
        return context


def eachcityview(request, address):
    context = {}
    context['object_list'] = Rentproperty.objects\
        .filter(location__contains=address).order_by('rent_diff')
    return render(request, 'city.html', context)


def cityview(request):
    context = {'city_list': CITY_LIST}
    return render(request, 'index.html', context)
