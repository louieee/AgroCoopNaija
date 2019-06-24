from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# This contains the list of specializations
class Tag:
    tags = ['fishery', 'animal husbandry', 'piggery', 'horticulture', 'banana farming']


# This contains the list of banks
class Bank:
    bank = ['First Bank of Nigeria', 'Stanbic IBTC', 'GTB bank', 'Access Bank', 'Oceanic Bank']


# This contains the list of states in Nigeria
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


# This function paginates a list item
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
