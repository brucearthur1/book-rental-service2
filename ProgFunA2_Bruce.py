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
    def __init__(self, ID, name, category_type, price_1, price_2):
        self.ID = ID
        self.name = name
        self.category_type = category_type  # New attribute for category type
        self.price_1 = price_1
        self.price_2 = price_2
        self.books = []  # List to store Book objects

    def display_info(self):
        print(f"Category ID: {self.ID}, Name: {self.name}, Type: {self.category_type}, Price Tier 1: ${self.price_1:.2f}, Price Tier 2: ${self.price_2:.2f}")
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


class BookSeries:
    def __init__(self, ID, name, category, component_books):
        self.ID = ID
        self.name = name
        self.category = category  # BookCategory object
        self.component_books = component_books  # List of Book objects

    def get_ID(self):
        return self.ID

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_component_books(self):
        return self.component_books

    def display_info(self):
        print(f"Book Series ID: {self.ID}, Name: {self.name}, Category: {self.category.name}")
        print("Component Books:")
        for book in self.component_books:
            print(f"  - {book.get_name()} (ID: {book.get_ID()})")


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
        self.book_series = []  # List to store BookSeries objects

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
            unresolved_book_series = []  # Temporary storage for unresolved book series

            # Read books from the book file
            with open(book_file, 'r') as file:
                for line in file:
                    if line.startswith("S"):  # Skip book series for now
                        data = line.strip().split(', ')
                        series_id = data[0]
                        series_name = data[1]
                        component_book_names = data[2:]
                        unresolved_book_series.append((series_id, series_name, component_book_names))
                    else:
                        book_id, book_name = line.strip().split(', ')
                        category = next((cat for cat in self.book_categories if cat.name == category_name), None)
                        book = Book(book_id, book_name, category)
                        self.books.append(book)

            # Read book categories from the book category file
            with open(book_category_file, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    category_id = data[0]
                    category_name = data[1]
                    category_type = data[2]
                    price_1 = float(data[3])
                    price_2 = float(data[4])
                    books = data[5:]

                    category = BookCategory(category_id, category_name, category_type, price_1, price_2)

                    # Add books to the category
                    for book_name in books:
                        book = next((b for b in self.books if b.get_name() == book_name), None)
                        if book:
                            book.category = category
                            category.add_book(book)

                    self.book_categories.append(category)

            # Resolve book series categories
            for series_id, series_name, component_book_names in unresolved_book_series:
                component_books = [b for b in self.books if b.get_name() in component_book_names]
                if component_books:
                    category = component_books[0].get_category()  # Resolve category from the first component book
                    book_series = BookSeries(series_id, series_name, category, component_books)
                    self.book_series.append(book_series)

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def find_customer(self, search_value):
        for customer in self.customers:
            if customer.get_ID() == search_value or customer.get_name() == search_value:
                return customer
        return None

    def find_customer_by_id_or_name(self, input_value):
        return next((c for c in self.customers if c.get_ID() == input_value or c.get_name() == input_value), None)

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

    def find_book_by_id_or_name(self, input_value):
        return next((b for b in self.books if b.get_ID() == input_value or b.get_name() == input_value), None)

    def find_book_series_by_id_or_name(self, input_value):
        return next((s for s in self.book_series if s.get_ID() == input_value or s.get_name() == input_value), None)

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

        print("\nBook Series:")
        for series in self.book_series:
            category_name = series.get_category().name if series.get_category() else "Uncategorized"
            print(f"ID: {series.get_ID()}, Name: {series.get_name()}, Category: {category_name}")
            print("Component Books:")
            for book in series.get_component_books():
                print(f"  - {book.get_name()} (ID: {book.get_ID()})")

    def list_book_categories(self):
        print("Book Categories:")
        for category in self.book_categories:
            print(f"ID: {category.ID}, Name: {category.name}, Type: {category.category_type}, Price Tier 1: ${category.price_1:.2f}, Price Tier 2: ${category.price_2:.2f}")
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
            print("5. Update information of a book category")
            print("6. Update books of a book category")
            print("7. Adjust the discount rate of all members")
            print("8. Adjust the reward rate of a Gold member")  # New option
            print("9. Exit")
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
                self.update_book_category()
            elif choice == "6":
                self.update_books_of_book_category()
            elif choice == "7":
                self.adjust_discount_rate()
            elif choice == "8":
                self.adjust_reward_rate()  # Call the new method
            elif choice == "9":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def rent_book(self):
        is_new_customer = False  # Track if the customer is newly added

        while True:
            customer_input = input("Enter customer ID or name: ")
            customer = self.records.find_customer_by_id_or_name(customer_input)

            if not customer:
                print("Customer not found. Adding a new customer.")
                while True:
                    customer_id = input("Enter new customer ID: ")
                    if self.records.find_customer(customer_id):
                        print(f"Error: A customer with ID '{customer_id}' already exists. Please enter a unique ID.")
                        continue
                    else:
                        break
                while True:
                    customer_name = input("Enter new customer name: ")
                    if self.records.find_customer(customer_name):
                        print(f"Error: A customer with name '{customer_name}' already exists. Please enter a unique name.")
                        continue
                    else:
                        break

                customer = Customer(customer_id, customer_name)
                self.records.customers.append(customer)
                print(f"Customer '{customer_name}' with ID '{customer_id}' has been added.")
                is_new_customer = True  # Mark the customer as newly added
                
            break
        # Confirm the customer name and ID
        print(f"Customer confirmed: {customer.get_name()} (ID: {customer.get_ID()})")
        rental_items = []  # List to store rental items (book/book series and borrowing days)

        while True:
            book_input = input("Enter book or book series ID or name (or type 'done' to finish): ")
            if book_input.lower() == "done":
                if not rental_items:
                    print("Error: You must rent at least one book or book series.")
                    continue
                else:
                    break

            book = self.records.find_book_by_id_or_name(book_input)
            book_series = self.records.find_book_series_by_id_or_name(book_input)

            if not book and not book_series:
                print("Error: Book or book series not found. Please try again.")
                continue
            
            # Confirm the selected book or book series
            if book:
                print(f"Selected Book: {book.get_name()} (ID: {book.get_ID()})")
            elif book_series:
                print(f"Selected Book Series: {book_series.get_name()} (ID: {book_series.get_ID()})")
            while True:
                try:
                    borrowing_days = int(input(f"Enter number of borrowing days for '{book_input}': "))
                    if borrowing_days <= 0:
                        print("Error: Number of borrowing days must be a positive integer. Please try again.")
                    elif book and book.get_category().category_type == "Reference" and borrowing_days > 14:
                        print("Error: This book can't be borrowed for more than 14 days. Please enter a valid number of borrowing days.")
                    else:
                        rental_items.append((book or book_series, borrowing_days))
                        break
                except ValueError:
                    print("Error: Invalid input. Please enter a positive integer.")

        # Calculate and display the receipt
        total_cost = 0
        total_discount = 0
        total_reward_points = 0  # Track total reward points for GoldMember customers
        print("\n------------------------------------------------------------------------------------------")
        print(f"Receipt for {customer.get_name()}")
        print("------------------------------------------------------------------------------------------")

        for item, borrowing_days in rental_items:
            if isinstance(item, Book):
                daily_price = item.daily_price(borrowing_days)
                cost = daily_price * borrowing_days
                discount = 0
                reward = 0

                # Apply discounts for members and gold members
                if isinstance(customer, Member):
                    discount = customer.get_discount(cost)
                elif isinstance(customer, GoldMember):
                    discount = customer.get_discount(cost)
                    reward = customer.calculate_reward(cost - discount)
                    total_reward_points += reward

                total_cost += cost - discount
                total_discount += discount
                print(f"Book rented: {item.get_name()} (ID: {item.get_ID()})")
                print(f"  - Daily price: ${daily_price:.2f} (AUD)")
                print(f"  - Total cost for {borrowing_days} days: ${cost:.2f} (AUD)")
                print(f"  - Discount applied: ${discount:.2f} (AUD)")
                if isinstance(customer, GoldMember):
                    print(f"  - Reward points earned: {reward}")
            elif isinstance(item, BookSeries):
                total_daily_price = sum(book.daily_price(borrowing_days) for book in item.get_component_books())
                series_daily_price = total_daily_price * 0.5
                cost = series_daily_price * borrowing_days
                discount = 0
                reward = 0

                # Apply discounts for members and gold members
                if isinstance(customer, Member):
                    discount = customer.get_discount(cost)
                elif isinstance(customer, GoldMember):
                    discount = customer.get_discount(cost)
                    reward = customer.calculate_reward(cost - discount)
                    total_reward_points += reward

                total_cost += cost - discount
                total_discount += discount
                print(f"Book Series rented: {item.get_name()} (ID: {item.get_ID()})")
                print("Component Books:")
                for book in item.get_component_books():
                    print(f"  - {book.get_name()} (ID: {book.get_ID()})")
                print(f"  - Daily price for the series: ${series_daily_price:.2f} (AUD)")
                print(f"  - Total cost for {borrowing_days} days: ${cost:.2f} (AUD)")
                print(f"  - Discount applied: ${discount:.2f} (AUD)")
                if isinstance(customer, GoldMember):
                    print(f"  - Reward points earned: {reward}")

        # Deduct reward points for GoldMember customers
        if isinstance(customer, GoldMember):
            print(f"Current reward points: {customer.get_reward()}")
            if customer.get_reward() >= 20:
                reward_deduction = (customer.get_reward() // 20) * 1  # $1 for every 20 points
                max_deduction = min(reward_deduction, total_cost)  # Ensure deduction does not exceed total cost
                points_used = int(max_deduction * 20)  # Convert deduction back to points
                customer.update_reward(-points_used)  # Deduct used points
                total_cost -= max_deduction
                print(f"Reward points used: {points_used} (equivalent to ${max_deduction:.2f} AUD)")
                print(f"Remaining reward points: {customer.get_reward()}")

        print("------------------------------------------------------------------------------------------")
        print(f"Total discount applied: ${total_discount:.2f} (AUD)")
        print(f"Total cost for all rentals after discount and reward deduction: ${total_cost:.2f} (AUD)")
        if isinstance(customer, GoldMember):
            print(f"Total reward points earned from this rental: {total_reward_points}")
            customer.update_reward(total_reward_points)  # Add earned reward points after deduction
            print(f"Updated reward points: {customer.get_reward()}")
        print("------------------------------------------------------------------------------------------")

        # Prompt if the customer would like to become a member (only for new customers)
        if is_new_customer:
            while True:
                upgrade = input("Would you like to become a Member? (yes/no): ").strip().lower()
                if upgrade == "yes":
                    customer = Member(customer.ID, customer.name)
                    self.records.customers[-1] = customer  # Update the customer in the records
                    print(f"Customer '{customer.get_name()}' has been upgraded to a Member.")
                    break
                elif upgrade == "no":
                    print("No membership upgrade selected.")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

    def update_book_category(self):
        category_input = input("Enter the ID or name of the book category to update: ")
        category = self.records.find_book_category(category_input)

        if not category:
            print(f"Error: Book category '{category_input}' not found.")
            return

        print(f"Updating information for book category '{category.name}' (ID: {category.ID})")
        print(f"Current Type: {category.category_type}")
        print(f"Current Price Tier 1: ${category.price_1:.2f}")
        print(f"Current Price Tier 2: ${category.price_2:.2f}")

        # Update the category type
        while True:
            new_type = input("Enter new type (Rental/Reference): ").strip().capitalize()
            if new_type in ["Rental", "Reference"]:
                category.category_type = new_type
                break
            else:
                print("Error: Invalid type. Please enter 'Rental' or 'Reference'.")

        # Update the first-tier price
        while True:
            try:
                new_price_1 = float(input("Enter new price for Tier 1 (up to 7 days): "))
                if new_price_1 >= 0:
                    category.price_1 = new_price_1
                    break
                else:
                    print("Error: Price must be a non-negative number.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")

        # Update the second-tier price
        while True:
            try:
                new_price_2 = float(input("Enter new price for Tier 2 (more than 7 days): "))
                if new_price_2 >= 0:
                    category.price_2 = new_price_2
                    break
                else:
                    print("Error: Price must be a non-negative number.")
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")

        print(f"Book category '{category.name}' (ID: {category.ID}) has been updated.")
        print(f"New Type: {category.category_type}")
        print(f"New Price Tier 1: ${category.price_1:.2f}")
        print(f"New Price Tier 2: ${category.price_2:.2f}")

    def update_books_of_book_category(self):
        category_input = input("Enter the ID or name of the book category to update: ")
        category = self.records.find_book_category(category_input)

        if not category:
            print(f"Error: Book category '{category_input}' not found.")
            return

        print(f"Updating books for book category '{category.name}' (ID: {category.ID})")
        print("Current books in this category:")
        for book in category.books:
            print(f"  - {book.get_name()} (ID: {book.get_ID()})")

        # Prompt for books to add or remove
        while True:
            action = input("Would you like to add or remove books? (add/remove/done): ").strip().lower()
            if action == "done":
                break
            elif action not in ["add", "remove"]:
                print("Error: Invalid action. Please enter 'add', 'remove', or 'done'.")
                continue

            books_input = input("Enter books in the format 'book_1:book_1_ID, book_2:book_2_ID, ...': ").strip()
            books_data = [book.strip() for book in books_input.split(",")]

            for book_entry in books_data:
                try:
                    book_name, book_id = book_entry.split(":")
                    book_name = book_name.strip()
                    book_id = book_id.strip()

                    # Find the book or book series by ID or name
                    book = self.records.find_book_by_id_or_name(book_id) or self.records.find_book_by_id_or_name(book_name)
                    book_series = self.records.find_book_series_by_id_or_name(book_id) or self.records.find_book_series_by_id_or_name(book_name)

                    if not book and not book_series:
                        print(f"Error: Book or book series '{book_name}' (ID: {book_id}) not found.")
                        continue

                    if action == "add":
                        if book:
                            if book not in category.books:
                                category.add_book(book)
                                print(f"Book '{book.get_name()}' (ID: {book.get_ID()}) has been added to the category.")
                            else:
                                print(f"Book '{book.get_name()}' (ID: {book.get_ID()}) is already in the category.")
                        elif book_series:
                            for component_book in book_series.get_component_books():
                                if component_book not in category.books:
                                    category.add_book(component_book)
                                    print(f"Book '{component_book.get_name()}' (ID: {component_book.get_ID()}) from series '{book_series.get_name()}' has been added to the category.")
                                else:
                                    print(f"Book '{component_book.get_name()}' (ID: {component_book.get_ID()}) is already in the category.")

                    elif action == "remove":
                        if book:
                            if book in category.books:
                                category.books.remove(book)
                                print(f"Book '{book.get_name()}' (ID: {book.get_ID()}) has been removed from the category.")
                            else:
                                print(f"Book '{book.get_name()}' (ID: {book.get_ID()}) is not in the category.")
                        elif book_series:
                            for component_book in book_series.get_component_books():
                                if component_book in category.books:
                                    category.books.remove(component_book)
                                    print(f"Book '{component_book.get_name()}' (ID: {component_book.get_ID()}) from series '{book_series.get_name()}' has been removed from the category.")
                                else:
                                    print(f"Book '{component_book.get_name()}' (ID: {component_book.get_ID()}) is not in the category.")

                except ValueError:
                    print(f"Error: Invalid format for book entry '{book_entry}'. Please use the format 'book_name:book_ID'.")
                    continue

        print(f"Updated books for book category '{category.name}' (ID: {category.ID}):")
        for book in category.books:
            print(f"  - {book.get_name()} (ID: {book.get_ID()})")

    def adjust_discount_rate(self):
        while True:
            try:
                new_rate = float(input("Enter the new discount rate for all members (e.g., 0.2 for 20%): "))
                if new_rate <= 0:
                    raise ValueError("The discount rate must be a positive number.")
                
                # Update the discount rate for all members
                Member.set_discount_rate(new_rate)
                GoldMember.set_discount_rate(new_rate)
                print(f"The discount rate for all members has been updated to {new_rate * 100:.2f}%.")
                break
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid positive number.")

    def adjust_reward_rate(self):
        while True:
            customer_input = input("Enter the ID or name of the Gold member: ")
            customer = self.records.find_customer_by_id_or_name(customer_input)

            if not customer:
                print(f"Error: Customer '{customer_input}' not found. Please try again.")
                continue

            if not isinstance(customer, GoldMember):
                print(f"Error: Customer '{customer.get_name()}' (ID: {customer.get_ID()}) is not a Gold member. Please try again.")
                continue

            print(f"Updating reward rate for Gold member '{customer.get_name()}' (ID: {customer.get_ID()})")
            print(f"Current Reward Rate: {customer.get_reward_rate() * 100:.2f}%")

            while True:
                try:
                    new_rate = float(input("Enter the new reward rate (e.g., 1 for 100%): "))
                    if new_rate <= 0:
                        raise ValueError("The reward rate must be a positive number.")
                    
                    customer.set_reward_rate(new_rate)
                    print(f"The reward rate for Gold member '{customer.get_name()}' (ID: {customer.get_ID()}) has been updated to {new_rate * 100:.2f}%.")
                    return
                except ValueError as e:
                    print(f"Error: {e}. Please enter a valid positive number.")



# Call the main function
if __name__ == "__main__":
    operations = Operations()
