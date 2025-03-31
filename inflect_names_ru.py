from enum import Enum


class Gender(Enum):
    M = 1
    W = 2


SPECIAL_SURNAMES_ON_0 = ("Дюма", "Золя", "Гавальда", "Деррида", "Диарра", "Дрогба", "Пеккала")
SPECIAL_SURNAMES_ON_2 = ("Дарвин", "Даруин", "Грин", "Брин", "Перих", "Рерих", "Дитрих")

SPECIAL_FIRSTNAMES = {
    "Любовь": {
        "Р": "Любови",
        "Д": "Любови",
        "В": "Любовь",
        "Т": "Любовью",
        "П": "Любови"
    },
    "Павел": {
        "Р": "Павла",
        "Д": "Павлу",
        "В": "Павла",
        "Т": "Павлом",
        "П": "Павле"
    },
    "Лев": {
        "Р": "Льва",
        "Д": "Льву",
        "В": "Льва",
        "Т": "Львом",
        "П": "Льве"
    }
}

CHAR_VOWELS = ('а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я')
# Гласные кроме а я
CHAR_VOWELS_OTHER = CHAR_VOWELS[1:-1]

CHAR_CONSONANTS = ('б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ')
CHAR_CONSONANTS_WITH_SOFT_SIGN = CHAR_CONSONANTS + ('ь',)

def _inflect_wrapper(f):
    def wrapper(gender: Gender, name, *args):
        if len(name) <=1 :
            return _inflect_0(name)
        if "-" in name:
            name1, name2 = name.split("-", 1)
            res1 = wrapper(gender, name1, *args)
            res2 = wrapper(gender, name2, *args)

            return {
                "Р": "%s-%s" % (res1['Р'], res2['Р']),
                "Д": "%s-%s" % (res1['Д'], res2['Д']),
                "В": "%s-%s" % (res1['В'], res2['В']),
                "Т": "%s-%s" % (res1['Т'], res2['Т']),
                "П": "%s-%s" % (res1['П'], res2['П']),
            }
        return f(gender, name, *args)
    return wrapper


def _inflect_0(_name):
    return {
        "Р": _name,
        "Д": _name,
        "В": _name,
        "Т": _name,
        "П": _name
    }

# Стандартные фамилии на -ов(а) -ев(а) -ёв(а) -ин(а) -ын(а)
def _inflect_surname_as_standart(_gender: Gender, _surname: str):
    if _gender == Gender.M:
        return {
            "Р": _surname + "а",
            "Д": _surname + "у",
            "В": _surname + "а",
            "Т": _surname + "ым",
            "П": _surname + "е"
        }

    if _gender == Gender.W:
        return {
            "Р": _surname[:-1] + "ой",
            "Д": _surname[:-1] + "ой",
            "В": _surname[:-1] + "у",
            "Т": _surname[:-1] + "ой",
            "П": _surname[:-1] + "ой"
        }


# Фамилии в форме прилагательного
def _inflect_surname_as_noun(_gender: Gender, _surname: str):
    if _gender == Gender.M:
        if _surname[-3:] in ("жий", "чий", "ший", "щий"):
            return {
                "Р": _surname[:-2] + "его",
                "Д": _surname[:-2] + "ему",
                "В": _surname[:-2] + "его",
                "Т": _surname[:-2] + "им",
                "П": _surname[:-2] + "ем"
            }
        else:
            return {
                "Р": _surname[:-2] + "ого",
                "Д": _surname[:-2] + "ому",
                "В": _surname[:-2] + "ого",
                "Т": _surname[:-2] + ("и" if _surname[-3] in ('г', 'ж', 'к', 'х', 'ч', 'ш', 'щ') else "ы") + "м",
                "П": _surname[:-2] + "ом"
            }

    if _gender == Gender.W:
        if _surname[-3:] in ("жая", "чая", "шая", "щая"):
            return {
                "Р": _surname[:-2] + "ей",
                "Д": _surname[:-2] + "ей",
                "В": _surname[:-2] + "ую",
                "Т": _surname[:-2] + "ей",
                "П": _surname[:-2] + "ей"
            }
        else:
            return {
                "Р": _surname[:-2] + "ой",
                "Д": _surname[:-2] + "ой",
                "В": _surname[:-2] + "ую",
                "Т": _surname[:-2] + "ой",
                "П": _surname[:-2] + "ой"
            }

# склонение фамилий и имён, оканчивающихся на согласную
def _inflect_on_consonant(_gender, _name):
    if _gender == Gender.W:
        return _inflect_0(_name)

    if _name[-1] in ("ь", "й"):
        return {
            "Р": _name[:-1] + "я",
            "Д": _name[:-1] + "ю",
            "В": _name[:-1] + "я",
            "Т": _name[:-1] + "ем",
            "П": _name[:-1] + ("и" if _name[-2] == "и" else "е")
        }

    # выпадающая гласная для фамилий, оканчивающихся на -ок -ек
    if len(_name) >=4 and _name[-2:] in ("ок", "ёк", "ек"):
        __name = _name[:-2]+_name[-1]
    else:
        __name = _name

    return {
        "Р": __name + "а",
        "Д": __name + "у",
        "В": __name + "а",
        "Т": __name + ("ем" if (_name[-3:-2] !='ь' and ((_name[-1] == "ц") or (_name[-1] == "ш") or (_name[-1] == 'ч' and _name[-2] in CHAR_VOWELS_OTHER))) else "ом"),
        "П": __name + "е"
    }

# Склонение имён и фамилий на -а -я
def _inflect_on_a_ya(_name):
    if _name[-2] in CHAR_VOWELS and _name[-1] == "a":
        return _inflect_0(_name)

    if len(_name) > 2 and _name[-2:] == "ия":
        return {
            "Р": _name[:-1] + "и",
            "Д": _name[:-1] + "и",
            "В": _name[:-1] + "ю",
            "Т": _name[:-1] + "ей",
            "П": _name[:-1] + "и"
        }

    if _name[-1] == "а":
        return {
                "Р": _name[:-1] + ("и" if _name[-2] in ('г', 'ж', 'к', 'х', 'ч', 'ш', 'щ') else "ы"),
                "Д": _name[:-1] + "е",
                "В": _name[:-1] + "у",
                "Т": _name[:-1] + ("ей" if _name[-2] in ('ж', 'ч', 'ц', 'ш', 'щ') else "ой"),
                "П": _name[:-1] + "е"
        }
    if _name[-1] == "я":
        return {
            "Р": _name[:-1] + "и",
            "Д": _name[:-1] + "е",
            "В": _name[:-1] + "ю",
            "Т": _name[:-1] + "ей",
            "П": _name[:-1] + "е"
        }

@_inflect_wrapper
def inflect_surname(gender: Gender, surname: str, male_surname: str | None = None) -> dict:
    if surname in SPECIAL_SURNAMES_ON_0:
        return _inflect_0(surname)

    if surname in SPECIAL_SURNAMES_ON_2:
        return _inflect_on_consonant(gender, surname)

    if surname[-2:] in ('их', 'ых'):
        return _inflect_0(surname)

    if len(surname) > 4 and (male_surname is None or surname != male_surname):
        if (gender == Gender.W and surname[-3:] in ("ова", "ёва", "ева", "ина", "ына") or
                gender == Gender.M and surname[-2:] in ("ов", "ёв", "ев", "ин", "ын")):
            return _inflect_surname_as_standart(gender, surname)
        # с набором surname[-3] не уверен !!!
        if surname[-3] in ('б', 'в', 'г', 'д', 'ж', 'з', 'к', 'л', 'м', 'н', 'п', 'с', 'т', 'ч', 'ш', 'щ'):
            if gender == Gender.W and surname[-2:] == "ая":
                return _inflect_surname_as_noun(gender, surname)

            if gender == Gender.M and surname[-2:] in ('ой', "ый"):
                return _inflect_surname_as_noun(gender, surname)
            # с набором surname[-3] не уверен !!!
            if gender == Gender.M and surname[-2:] == "ий" and surname[-3] in ('ж', 'з', 'к', 'н', 'ч', 'ш', 'щ'):
                return _inflect_surname_as_noun(gender, surname)

    if surname[-1] in CHAR_CONSONANTS_WITH_SOFT_SIGN:
        return _inflect_on_consonant(gender, surname)

    if surname[-1] in ('а', 'я'):
        return _inflect_on_a_ya(surname)

    return _inflect_0(surname)

@_inflect_wrapper
def inflect_firstname(gender: Gender, firstname: str):
    if firstname in SPECIAL_FIRSTNAMES:
        return SPECIAL_FIRSTNAMES[firstname]

    if firstname[-1] in CHAR_CONSONANTS_WITH_SOFT_SIGN:
        return _inflect_on_consonant(gender, firstname)

    if firstname[-1] in ('а', 'я'):
        return _inflect_on_a_ya(firstname)

    return _inflect_0(firstname)

def inflect_patronymic(gender, patronymic):

    if gender == Gender.M and patronymic[-2:] == "ич":
        return _inflect_on_consonant(gender, patronymic)

    if gender == Gender.W and patronymic[-2:] == "на":
        return _inflect_on_a_ya(patronymic)

    return _inflect_0(patronymic)


def inflect_full_name(gender: Gender, surname: str, firstname: str, patronymic: str | None = None, male_surname: str | None = None):
    result = inflect_surname(gender, surname, male_surname)

    for p, n in inflect_firstname(gender, firstname).items():
        result[p] += " "+ n

    if patronymic:
        for p, n in inflect_patronymic(gender, patronymic).items():
            result[p] += " " + n

    return result
