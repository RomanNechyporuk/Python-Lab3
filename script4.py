## --- Модель товару ---
class Product:
    def __init__(self, product_id: int, name: str, price: float, quantity: int):
        self.id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        # Форматування ціни за допомогою лямбда-функції
        format_price = lambda p: f"{p:.2f}грн"
        return f"[{self.id}] {self.name} - {format_price(self.price)} (В наявності: {self.quantity} шт.)"


# --- Консольний магазин ---
class ConsoleShop:
    def __init__(self):
        # Початковий каталог товарів
        self.catalog = [
            Product(1, "Ноутбук", 25000.0, 5),
            Product(2, "Мишка", 450.5, 15),
            Product(3, "Клавіатура", 1200.0, 8),
            Product(4, "Навушники", 850.75, 10),
        ]
        self.cart = {}  # {Product: quantity}
        self.admin_password = "admin"

        # Лямбда-функція для форматування ціни: xxx.xxгрн
        self.format_price = lambda p: f"{p:.2f}грн"

    def display_catalog(self):
        print("\n=== Каталог товарів ===")
        if not self.catalog:
            print("Каталог порожній.")
            return

        # Використання map та lambda для виводу
        list(map(lambda p: print(p), self.catalog))

    def add_to_cart(self):
        self.display_catalog()
        try:
            prod_id = int(input("\nВведіть ID товару для додавання в кошик: "))
            # Використання filter + lambda для пошуку товару за ID
            product = next(filter(lambda p: p.id == prod_id, self.catalog), None)

            if not product:
                print("Товар з таким ID не знайдено.")
                return

            qty = int(input(f"Введіть кількість для '{product.name}': "))
            if qty <= 0:
                print("Кількість має бути більшою за 0.")
                return

            current_in_cart = self.cart.get(product, 0)
            if qty + current_in_cart > product.quantity:
                print(f"Недостатньо товару на складі! Доступно: {product.quantity - current_in_cart}")
                return

            self.cart[product] = current_in_cart + qty
            print(f"У кошик додано: {product.name} x{qty}")

        except ValueError:
            print("Помилка: Введіть числове значення.")

    def view_cart(self):
        print("\n=== Ваш кошик ===")
        if not self.cart:
            print("Кошик порожній.")
            return

        # Вивід товарів у кошику з підрахунком проміжної суми лямбдою
        calculate_item_total = lambda item, qty: item.price * qty
        for item, qty in self.cart.items():
            total_item_price = calculate_item_total(item, qty)
            print(f"[{item.id}] {item.name} x{qty} = {self.format_price(total_item_price)}")

        # Підрахунок загальної суми кошика через reduce + lambda
        from functools import reduce
        total_sum = reduce(lambda acc, pair: acc + (pair[0].price * pair[1]), self.cart.items(), 0.0)
        print(f"\nЗагальна сума: {self.format_price(total_sum)}")

    def remove_from_cart(self):
        if not self.cart:
            print("\nКошик порожній.")
            return

        self.view_cart()
        try:
            prod_id = int(input("\nВведіть ID товару для видалення з кошика: "))
            # Пошук товару в кошику за ID
            product_to_remove = next(filter(lambda p: p.id == prod_id, self.cart.keys()), None)

            if not product_to_remove:
                print("Цього товару немає у вашому кошику.")
                return

            del self.cart[product_to_remove]
            print(f"Товар '{product_to_remove.name}' видалено з кошика.")

        except ValueError:
            print("Помилка: Введіть числове значення.")

    def checkout(self):
        if not self.cart:
            print("\nКошик порожній. Немає чого купувати.")
            return

        self.view_cart()
        confirm = input("\nПідтвердити покупку? (так/ні): ").strip().lower()

        if confirm in ['так', 'yes', 'y']:
            # Списання товарів зі складу
            for product, qty in self.cart.items():
                product.quantity -= qty

            self.cart.clear()
            print("\n Дякуємо за покупку! Замовлення успішно оформлено.")
        else:
            print("\nПокупку скасовано.")

    def admin_login(self):
        password = input("\nВведіть пароль адміністратора: ")
        if password == self.admin_password:
            print("\n=== Панель адміністратора (Залишки на складі) ===")
            # Форматування залишків через map та lambda
            print_stock = lambda p: f"ID: {p.id} | Назва: {p.name:<15} | Ціна: {self.format_price(p.price):<12} | Залишок: {p.quantity} шт."
            stock_info = list(map(print_stock, self.catalog))
            for item in stock_info:
                print(item)
        else:
            print("Невірний пароль!")

    def run(self):
        while True:
            print("\n" + "="*30)
            print("      ГОЛОВНЕ МЕНЮ")
            print("="*30)
            print("1. Переглянути каталог")
            print("2. Додати товар у кошик")
            print("3. Переглянути кошик")
            print("4. Видалити товар з кошика")
            print("5. Купити товари з кошика")
            print("6. Вхід для адміністратора")
            print("0. Вихід")

            choice = input("Оберіть дію: ").strip()

            if choice == "1":
                self.display_catalog()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.view_cart()
            elif choice == "4":
                self.remove_from_cart()
            elif choice == "5":
                self.checkout()
            elif choice == "6":
                self.admin_login()
            elif choice == "0":
                print("\nДякуємо, що завітали! До побачення.")
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    shop = ConsoleShop()
    shop.run()
