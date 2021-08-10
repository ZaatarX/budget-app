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
    total_spent = 0
    percentage = []

    for cat in categories:
        for l in cat.ledger:
            total_spent += l["amount"]

    for cat in categories:
        for l in cat.ledger:
            percentage.append(round((l["amount"] / total_spent) * 100))

    i = 100
    j = 0
    table = ''

    while i >= 0:
        side = f'{i: >3}| '
        mid = ''
        for p in percentage:
            if p >= i:
                mid += 'o '
            else:
                mid += '  '
        table += side + mid + '\n'
        i -= 10

    table += ' ' * 3 + len(mid) * '-' + '\n'

    print(table)

    return table
