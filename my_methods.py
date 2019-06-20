from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Tag:
    tags = ['fishery', 'animal husbandry', 'piggery', 'horticulture', 'banana farming']


class Bank:
    bank = ['First Bank of Nigeria', 'Stanbic IBTC', 'GTB bank', 'Access Bank', 'Oceanic Bank']


class State:
    states = [
        ' Abia ',
        ' Adamawa ',
        ' AkwaIbom ',
        ' Anambra ',
        ' Bauchi ',
        ' Benue ',
        ' Bornu ',
        ' Bayelsa ',
        ' CrossRiver ',
        ' Delta ',
        ' Edo ',
        ' Enugu ',
        ' Imo ',
        ' Jigawa ',
        ' Lagos ',
        ' Kogi ',
        ' Nassarawa ',
        ' Gombe ',
        ' Kaduna ',
        ' Kano ',
        ' Kastina ',
        ' Kebbi ',
        ' Niger ',
        ' Ogun ',
        ' Ondo ',
        ' Osun ',
        ' Oyo ',
        ' Plateu ',
        ' Rivers ',
        ' Sokoto ',
        ' Taraba ',
        ' Yobe ',
        ' Zamfara ',
        ' Abuja ',
    ]


def get_pagination(page, item):
    paginator = Paginator(item, 1)
    try:
        pages = paginator.page(page)
        return pages
    except PageNotAnInteger:
        pages = paginator.page(1)
        return pages
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
        return pages





