class Category:

    def __init__(self, name) -> None:
        self.name = name
        self.ledger = list()

    def __str__(self) -> str:
        title = f"{self.name:*^30}\n"
        items = ""
        total = 0

        for i in range(len(self.ledger)):
            items += f"{self.ledger[i]['description'][0:23]:23}" + \
                f"{self.ledger[i]['amount']:>7.2f}" + '\n'
            total += self.ledger[i]['amount']

        output = title + items + "Total: " + str(total)

        return output

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": abs(amount) * -1,
                               "description": description})
            return True
        return False

    def get_balance(self):
        total = 0
        i = 0
        for l in self.ledger:
            total += l["amount"]
        return total

    def transfer(self, amount, category):
        if self.check_funds(amount):
            if self.withdraw(amount, f'Transfer to {category.name}'):
                category.deposit(amount, f'Transfer from {self.name}')
                return True
        return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True


def create_spend_chart(categories):
    amounts = list()

    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(amounts), 2)
    spent_percentage = list(map(lambda amount: int(
        (((amount / total) * 10) // 1) * 10), amounts))

    # Create the table substrings
    header = "Percentage spent by category\n"
    table = ""

    for value in reversed(range(0, 101, 10)):
        table += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                table += " o "
            else:
                table += "   "
        table += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"

    descriptions = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(
        map(lambda description: description.ljust(max_length), descriptions))

    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + table + footer).rstrip("\n")
