class Customer:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def display_info(self):
        print(f"Customer ID: {self.ID}, Name: {self.name}")


class Member:
    discount_rate = 0.10  # Default discount rate

    def __init__(self, ID, name):
        self.ID = ID
        self.name = name

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    @classmethod
    def set_discount_rate(cls, rate):
        cls.discount_rate = rate

    def get_discount(self, rental_cost):
        return rental_cost * self.discount_rate

    def display_info(self):
        print(f"Member ID: {self.ID}, Name: {self.name}, Discount Rate: {self.discount_rate * 100}%")


class GoldMember:
    discount_rate = 0.12  # Default discount rate for all Gold members

    def __init__(self, ID, name, reward_rate=1.0):
        self.ID = ID
        self.name = name
        self.reward_rate = reward_rate
        self.reward = 0

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_reward_rate(self):
        return self.reward_rate

    def get_reward(self):
        return self.reward

    def get_discount(self, rental_cost):
        return rental_cost * self.discount_rate

    def calculate_reward(self, rental_cost_after_discount):
        return round(rental_cost_after_discount * self.reward_rate)

    def update_reward(self, value):
        self.reward += value

    def display_info(self):
        print(f"Gold Member ID: {self.ID}, Name: {self.name}, Discount Rate: {self.discount_rate * 100}%, Reward Rate: {self.reward_rate * 100}%, Reward: {self.reward}")

    @classmethod
    def set_discount_rate(cls, rate):
        cls.discount_rate = rate

    def set_reward_rate(self, rate):
        self.reward_rate = rate


class Book:
    def __init__(self, ID, name, category):
        self.ID = ID
        self.name = name
        # Resolve the category name to a BookCategory object
        category_obj = next((cat for cat in Records().book_categories if cat.name == category), None)
        self.category = category_obj  # Update the category to the resolved object
        
    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def daily_price(self, borrowing_days):
        return self.category.get_price(borrowing_days)

    def display_info(self):
        print(f"Book ID: {self.ID}, Name: {self.name}, Category: {self.category.name}")


class BookCategory:
    def __init__(self, ID, name, price_1, price_2):
        self.ID = ID
        self.name = name
        self.price_1 = price_1
        self.price_2 = price_2
        self.books = []  # List to store Book objects

    def display_info(self):
        print(f"Category ID: {self.ID}, Name: {self.name}, Price Tier 1: ${self.price_1:.2f}, Price Tier 2: ${self.price_2:.2f}")
        print("Books in this category:")
        for book in self.books:
            print(f"  - {book.get_name()} (ID: {book.get_ID()})")

    def add_book(self, book):
        if isinstance(book, Book):
            self.books.append(book)
        else:
            print("Error: Only Book objects can be added to the category.")

    def get_price(self, borrowing_days):
        if borrowing_days <= 7:  # First-tier price for up to 7 days
            return self.price_1 
        else:  # Second-tier price for more than 7 days
            return self.price_2 


class Rental:
    def __init__(self, customer, book, borrowing_days):
        self.customer = customer  # Customer object (Customer, Member, or GoldMember)
        self.book = book  # Book object
        self.borrowing_days = borrowing_days

    def compute_cost(self):
        original_cost = self.book.daily_price(self.borrowing_days) * self.borrowing_days
        discount = 0
        total_cost = original_cost
        reward = 0

        if isinstance(self.customer, Member):
            discount = self.customer.get_discount(original_cost)
            total_cost -= discount

        if isinstance(self.customer, GoldMember):
            discount = self.customer.get_discount(original_cost)
            total_cost -= discount
            reward = self.customer.calculate_reward(total_cost)
            self.customer.update_reward(reward)

        return original_cost, discount, total_cost, reward

    def display_info(self):
        print(f"Rental Info:")
        print(f"  Customer: {self.customer.get_name()} (ID: {self.customer.get_ID()})")
        print(f"  Book: {self.book.get_name()} (ID: {self.book.get_ID()})")
        print(f"  Borrowing Days: {self.borrowing_days}")
        original_cost, discount, total_cost, reward = self.compute_cost()
        print(f"  Original Cost: ${original_cost:.2f}")
        print(f"  Discount: ${discount:.2f}")
        print(f"  Total Cost: ${total_cost:.2f}")
        if isinstance(self.customer, GoldMember):
            print(f"  Reward Earned: {reward}")


class Records:
    def __init__(self):
        self.customers = []  # List to store Customer, Member, or GoldMember objects
        self.book_categories = []  # List to store BookCategory objects
        self.books = []  # List to store Book objects

    def read_customers(self, file_name):
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    customer_type = data[0]
                    customer_id = data[1]
                    customer_name = data[2]
                    discount_rate = data[3]
                    reward_rate = data[4]
                    reward_points = data[5]

                    if customer_type == "C":
                        customer = Customer(customer_id, customer_name)
                    elif customer_type == "M":
                        customer = Member(customer_id, customer_name)
                        if discount_rate != "na":
                            customer.set_discount_rate(float(discount_rate))
                    elif customer_type == "G":
                        customer = GoldMember(customer_id, customer_name)
                        if discount_rate != "na":
                            customer.set_discount_rate(float(discount_rate))
                        if reward_rate != "na":
                            customer.set_reward_rate(float(reward_rate))
                        if reward_points != "na":
                            customer.update_reward(int(reward_points))
                    else:
                        continue  # Skip invalid customer types

                    self.customers.append(customer)
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def read_books_and_book_categories(self, book_file, book_category_file):
        try:
            # Read books from the book file
            with open(book_file, 'r') as file:
                for line in file:
                    book_id, book_name = line.strip().split(', ')
                    book = Book(book_id, book_name, None)  # Category  will be set later
                    self.books.append(book)

            # Read book categories from the book category file
            with open(book_category_file, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    category_id = data[0]
                    category_name = data[1]
                    price_1 = float(data[2])
                    price_2 = float(data[3])
                    books = data[4:]

                    category = BookCategory(category_id, category_name, price_1, price_2)

                    # Add books to the category
                    for book_name in books:
                        book = next((b for b in self.books if b.get_name() == book_name), None)
                        if book:
                            book.category = category  # Set the category object for the book
                            category.add_book(book)

                    self.book_categories.append(category)

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def find_customer(self, search_value):
        for customer in self.customers:
            if customer.get_ID() == search_value or customer.get_name() == search_value:
                return customer
        return None

    def find_book_category(self, search_value):
        for category in self.book_categories:
            if category.ID == search_value or category.name == search_value:
                return category
        return None

    def find_book(self, search_value):
        for book in self.books:
            if book.get_ID() == search_value or book.get_name() == search_value:
                return book
        return None

    def list_customers(self):
        print("Customers:")
        for customer in self.customers:
            if isinstance(customer, GoldMember):
                print(f"ID: {customer.get_ID()}, Name: {customer.get_name()}, Discount Rate: {customer.discount_rate * 100}%, Reward Rate: {customer.get_reward_rate() * 100}%, Reward: {customer.get_reward()}")
            elif isinstance(customer, Member):
                print(f"ID: {customer.get_ID()}, Name: {customer.get_name()}, Discount Rate: {customer.discount_rate * 100}%")
            else:
                print(f"ID: {customer.get_ID()}, Name: {customer.get_name()}")

    def list_books(self):
        print("Books:")
        for book in self.books:
            category_name = book.get_category().name if book.get_category() else "Uncategorized"
            print(f"ID: {book.get_ID()}, Name: {book.get_name()}, Category: {category_name}")

    def list_book_categories(self):
        print("Book Categories:")
        for category in self.book_categories:
            print(f"ID: {category.ID}, Name: {category.name}, Price Tier 1: ${category.price_1:.2f}, Price Tier 2: ${category.price_2:.2f}")
            print("Books:")
            for book in category.books:
                print(f"  - {book.get_name()} (ID: {book.get_ID()})")

class Operations:
    def __init__(self):
        self.records = None  # Initialize the records attribute as None
        self.load_data()  # Load data when the Operations object is created
        self.display_menu()  # Display the menu after loading data

    def load_data(self):
        try:
            self.records = Records()  # Create a Records object and store it in the instance attribute
            self.records.read_customers("customers.txt")
            # self.records.list_customers()
            self.records.read_books_and_book_categories("books.txt", "book_categories.txt")
            # self.records.list_book_categories()
            # self.records.list_books()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit()

    def display_menu(self):
        if not self.records:  # Check if records have been loaded
            print("Error: Records have not been loaded. Please load data first.")
            return

        while True:
            print("\nMenu:")
            print("1. Rent a book")
            print("2. Display existing customers")
            print("3. Display existing book categories")
            print("4. Display existing books")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.rent_book()
            elif choice == "2":
                self.records.list_customers()
            elif choice == "3":
                self.records.list_book_categories()
            elif choice == "4":
                self.records.list_books()
            elif choice == "5":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def rent_book(self):
        customer_name = input("Enter customer name: ")
        customer = self.records.find_customer(customer_name)

        if not customer:
            print("Customer not found. Adding as a new customer.")
            customer_type = input("Is the customer a Member (M) or just a Customer (C)? ").strip().upper()
            customer_id = input("Enter new customer ID: ")
            if customer_type == "M":
                customer = Member(customer_id, customer_name)
            else:
                customer = Customer(customer_id, customer_name)
            self.records.customers.append(customer)

        book_name = input("Enter book name: ")
        book = self.records.find_book(book_name)

        if not book:
            print("Book not found. Please try again.")
            return

        borrowing_days = int(input("Enter number of borrowing days: "))
        rental = Rental(customer, book, borrowing_days)
        original_cost, discount, total_cost, reward = rental.compute_cost()

        print("\n------------------------------------------------------------------------------------------")
        print(f"Receipt for {customer.get_name()}")
        print("------------------------------------------------------------------------------------------")
        print(f"Books rented:")
        print(f" - {book.get_name()} for {borrowing_days} days (${book.daily_price(borrowing_days):.2f} AUD/day)")
        print("------------------------------------------------------------------------------------------")
        print(f"Original cost: ${original_cost:.2f} (AUD)")
        print(f"Discount: ${discount:.2f} (AUD)")
        print(f"Total cost: ${total_cost:.2f} (AUD)")
        if isinstance(customer, GoldMember):
            print(f"Reward: {reward}")
        print("------------------------------------------------------------------------------------------")


# Call the main function
if __name__ == "__main__":
    operations = Operations()
