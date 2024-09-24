import json

FILE_NAME = "costco.json"


def recursive_print(data, level=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print("\t" * level, key)
            recursive_print(value, level + 1)


def main():
    with open(FILE_NAME, "r") as file:
        data = json.load(file)

    products = data.get("products")

    for product in products:
        print(product.get("name"))
        recursive_print(product)
        break


if __name__ == "__main__":
    main()
