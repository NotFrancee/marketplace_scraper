import pyperclip


def gen_excel_formula():
    """Generate excel formula to track current price of position and handle during non-mkt hours"""

    template = '=IF({current_price}="#Undef",{check_price},{current_price})'

    current_price = input("RTD link for current price: ").replace("=", "")
    check_price = input("RTD link for check price: ").replace("=", "")

    result = template.format(current_price=current_price, check_price=check_price)

    print("\n")
    print(result)
    pyperclip.copy(result)


gen_excel_formula()
