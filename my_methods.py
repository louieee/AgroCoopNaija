from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# This contains the list of specializations
class Tag:
    tags = ['Agricultural Business',
            'Agricultural Economics',
            'Agricultural Equipment',
            'Agricultural Management',
            'Agronomy',
            'Animal Husbandry', 'Crop Production', 'Fishery',
            'Food Science', 'Forestry', 'Horticulture', 'Soil Science', 'Tropical Agriculture',
            'Veterinary Science', 'Water Science']


# This contains the list of banks
class Bank:
    bank = ['First Bank of Nigeria Limited', 'Fidelity Bank Plc',
            'First City Monument Bank Plc', 'Access Bank Plc',
            'Guaranty Trust Bank Plc', 'Union Bank of Nigeria Plc', 'United Bank for Africa Plc',
            'Zenith Bank Plc', 'Citibank Nigeria Limited', 'Ecobank Nigeria Plc',
            'Heritage Banking Company Limited', 'Keystone Bank Limited',
            'Polaris Bank Limited.', 'Stanbic IBTC Bank Plc', 'Standard Chartered', 'Sterling Bank Plc',
            'Unity Bank Plc', 'Wema Bank Plc'
            ]


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
    paginator = Paginator(item, 10)
    try:
        pages = paginator.page(page)
        return pages
    except PageNotAnInteger:
        pages = paginator.page(1)
        return pages
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
        return pages


degrees = ['No Degree', 'First School leaving certificate', 'WASSCE', 'NCE', 'ND', 'HND', 'BA', 'BSc', 'BEngr', 'MSc',
           'PGD',
           'PHD', 'Doctorate Degree']


def degree_to_title(argument):
    switcher = {
        'Doctorate Degree': 'Dr. ',
        'PHD': 'Prof. ',
        'BEngr': 'Engr. '
    }
    return switcher.get(argument, 'None')
