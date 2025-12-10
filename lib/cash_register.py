#!/usr/bin/env python3

class CashRegister:
    def __init__(self, discount=0):
        # internal storage for discount, don't touch this directly
        self._discount = 0
        
        # setting discount through the property so it gets validated
        self.discount = discount

        # running total of everything added so far
        self.total = 0

        # list of item names, one entry per unit (so qty=3 means 3 copies)
        self.items = []

        # list of past transactions so I can undo the last one
        self.previous_transactions = []

    @property
    def discount(self):
        # just return whatever the current discount actually is
        return self._discount

    @discount.setter
    def discount(self, value):
        # discount HAS to be an int, period
        if not isinstance(value, int):
            print("Not valid discount")
            return

        # and it can't be outside 0–100, anything else gets rejected
        if value < 0 or value > 100:
            print("Not valid discount")
            return

        # if it's valid, cool, set it
        self._discount = value

    def add_item(self, item, price, quantity=1):
        # price * qty = how much this transaction adds to total
        transaction_total = price * quantity
        
        # update the running total
        self.total += transaction_total

        # add this item to the items list qty times
        for _ in range(quantity):
            self.items.append(item)

        # store the whole transaction so we can undo it later if needed
        transaction_record = {
            "item": item,
            "price": price,
            "quantity": quantity,
            "total": transaction_total
        }
        self.previous_transactions.append(transaction_record)

    def apply_discount(self):
        # if there's no discount set, tell the user and dip
        if self.discount == 0:
            print("There is no discount to apply.")
            return 

        # calculate what the new total SHOULD be after discount
        discounted_total = self.total * (100 - self.discount) / 100

        # update total to match the discounted total
        self.total = discounted_total

        # print the exact message the tests expect (int() removes the .0)
        print(f"After the discount, the total comes to ${int(self.total)}.")

    def void_last_transaction(self):
        # if there's nothing to undo, just dip
        if not self.previous_transactions:
            return

        # grab the last transaction and remove it from the log
        last_transaction = self.previous_transactions.pop()

        # subtract what that transaction added to the total
        self.total -= last_transaction["total"]

        # remove the correct number of items from the items list
        for _ in range(last_transaction["quantity"]):
            if self.items:
                self.items.pop()
