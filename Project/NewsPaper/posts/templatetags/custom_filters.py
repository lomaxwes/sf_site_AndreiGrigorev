from django import template

register = template.Library()

censor_list = ['политика', 'мбаппе', 'килиан', 'спорт', 'лыжи']


@register.filter()
def censor(value):
    new_list = list(value.split())
    if isinstance(value, str):
        for i in range(len(new_list)):
            if new_list[i].lower() in censor_list:
                s = new_list[i]
                new_list[i] = s[:2] + '*' * (len(s) - 2)
        return ' '.join(new_list)
    else:
        raise TypeError('Объект не является строкой')