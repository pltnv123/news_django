from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': 'Р',
    'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
    """
    value: значение, к которому нужно применить фильтр
    code: код валюты
    """
    postfix = CURRENCIES_SYMBOLS[code]

    return f'{value} {postfix}'

@register.filter()
def filter_message(message: str):
    """
    message: значение, которое мы получаем от пользователя
     return  - возвращает отфильтрованное от нецензурной лексики сообщение
    """
    variants = ['сука', 'блять', 'пиздец', 'бля', 'нахуй', 'ебало',
                'ебальник', 'ебать', 'выебываться', 'долбаеб',
                'уебан', 'уебался', 'дрочила', 'пидор', 'пизда',
                'хуета', 'хуй', 'хуйня', 'хуевый', 'хуёвый', 'залупа',
                'дрочить', 'гандон', 'манда', 'блядь',
                ]  # непристойные выражения

    ln = len(variants)
    filtred_message = ''  # default value
    pattern = '*'  # чем заменять непристойные выражения
    if str(message):
        string = ''
        for i in message:
            string += i
            string2 = string.lower()

            flag = 0
            for j in variants:
                if not string2 in j:
                    flag += 1
                if string2 == j:
                    filtred_message += string[0] + pattern*(len(string)-1)
                    flag -= 1
                    string = ''
            if flag == ln:
                filtred_message += string
                string = ''
        if string2 != '' and string2 not in variants:
            filtred_message += string
        elif string2 != '':
            filtred_message += pattern * len(string)

    return filtred_message
