from . import CostcoDBSingleton
from .lib import CostcoProduct, get_data


def main():
    costco_data = get_data()
    costco_db = CostcoDBSingleton.get_instance()

    products = costco_data.get("products")

    for product in products:
        product = CostcoProduct.fromJson(product)
        if costco_db.is_exists(product):
            costco_db.modify_product(product)
        else:
            costco_db.insert_product(product)

    products = costco_db.get_products()
    serialized_products = []
    for product in products:
        product = list(product)
        try:
            serialized_product = CostcoProduct(*product)
        except Exception as e:
            print(product)
            print(e)
            continue
        serialized_products.append(serialized_product)

    with open("db_products.txt", "w") as file:
        for product in serialized_products:
            file.write(str(product) + "\n\n")


if __name__ == "__main__":
    main()
