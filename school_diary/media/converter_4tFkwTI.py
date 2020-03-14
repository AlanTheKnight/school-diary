ALPHABET = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def convert_to_decimal(num : str, base : int) -> int:
    """Return number num with base base converted to the decimal number"""
    return int(num, base)


def convert_to_y(base : int, decimal : int) -> str:
    """Return decimal converted to the number with base base."""
    output = []
    num = decimal
    while True:
        if num < base:
            output.append(num)
            break
        else:
            output.append(num % base)
            num = num // base
    output.reverse()
    checklist(output)
    output = "".join(output)
    return output


def checklist(catalog : list) -> list:
    """Checks if there are any numbers > 9 in catalog and changes them to their alphabetical equivalents.
    Also this function str() every element in the list."""
    for count in range(0, len(catalog)):
        sym = catalog[count]
        if sym > 9:
            sym = ALPHABET[sym]
        catalog[count] = str(sym)
    return catalog


def check_for_base(num, base):
    catalog = ALPHABET
    for a in num:
        if a not in catalog[0:base]:
            return False
    return True


def convert(number, base, base2):
    try:
        if check_for_base(number, base):
            decimal = int(convert_to_decimal(number, base))
            return convert_to_y(base2, decimal)
        else:
            return "Error"
    except:
        return "Error"


number = input("Введите число: ").upper()
base = int(input("Введите его систему счисления: "))
base2 = int(input("Введите систему счисления числа, которое вы хотите получить: "))
if 2 <= base <= 36 and 2 <= base2 <= 36:
    print(convert(number, base, base2))
else:
    print("Error")
