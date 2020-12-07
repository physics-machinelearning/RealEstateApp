from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from datetime import datetime, timedelta

from realestate.models import Rentproperty
from realestate.forms import SearchConditionForm


CITY_LIST = [
    '中央区', '千代田区', '文京区', '港区', '新宿区', '品川区', '目黒区', '大田区', '世田谷区', 
    '渋谷区']  #, '中野区', '杉並区', '練馬区', '板橋区', '豊島区', '北区',
    #'台東区', '墨田区', '江東区', '荒川区', '足立区', '葛飾区', '江戸川区'
#]


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
    last_record = Rentproperty.objects.order_by("-date").first()
    year = last_record.date.year
    month = last_record.date.month
    day = last_record.date.day
    start = datetime(year, month, day)
    end = start + timedelta(days=1)
    
    num = 10

    if request.method == 'POST':
        form = SearchConditionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            min_rent = float(post.min_rent)
            max_rent = float(post.max_rent)
            floor_plan = post.floor_plan
            min_area = post.min_area
            min_area = float(min_area)

            if post.bath_toilet == None:
                bath_toilet = None
            else:
                if post.bath_toilet == '別':
                    bath_toilet = True
                else:
                    bath_toilet = False

            if post.autolock == None:
                autolock = None
            else:
                if post.autolock == 'オートロック有り':
                    autolock = True
                else:
                    autolock = False

            queryset = Rentproperty.objects.filter(location__contains=address)
            # queryset = queryset.filter(date__range=(start, end))
            if min_rent:
                queryset = queryset.filter(rent__gte=min_rent)
            if max_rent:
                queryset = queryset.filter(rent__lte=max_rent)
            if floor_plan:
                queryset = queryset.filter(floor_plan=floor_plan)
            if min_area:
                queryset = queryset.filter(area__gte=min_area)
            queryset = queryset.order_by('rent_diff')
            paginator = Paginator(queryset, num)
            request.session['queryset'] = queryset
            try:
                page_int = 1
                inquiries_page = paginator.get_page(page_int)
                context = {}
                context['form'] = form
                context['object_list'] = inquiries_page
                return render(request, 'city.html', context)
            except Exception as err:
                print('page not found')
                print(err)

    else:
        form = SearchConditionForm()
        page_int = request.GET.get('page', 1)

        if 'queryset' in request.session:
            print(request.session['queryset'])
            queryset = request.session['queryset']
        else:
            queryset = Rentproperty.objects.filter(location__contains=address)
            # queryset = queryset.filter(date__range=(start, end))
            queryset = queryset.order_by('rent_diff')

        paginator = Paginator(queryset, num)
        try:
            inquiries_page = paginator.get_page(page_int)
        except EmptyPage:
            print('page not found')

        context = {}
        context['object_list'] = inquiries_page
        context['form'] = form
        return render(request, 'city.html', context)


def cityview(request):
    context = {'city_list': CITY_LIST}
    return render(request, 'index.html', context)


def mapview(request):
    pass
