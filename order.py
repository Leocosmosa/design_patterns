from collections import defaultdict

class CashSuper():
    def __init__(self):
        pass
    def acceptCash(self, money):
        pass

class CashNormal(CashSuper):
    def __init__(self):
        pass
    def acceptCash(self, money):
        return money

class CashRebate(CashSuper):
    def __init__(self, rebate):
        self.rebate = rebate
    def acceptCash(self, money):
        return money * self.rebate

class CashReturn(CashSuper):
    def __init__(self, con, ret):
        self.con = con
        self.ret = ret
    def acceptCash(self, money):
        return money - money // self.con * self.ret

class CashContext():
    def __init__(self, type):
        self.cs = CashSuper()
        if type == 'Normal':
            self.cs = CashNormal()
        elif type == 'Rebate':
            self.cs = CashRebate(0.8)
        elif type == 'Return':
            self.cs = CashReturn(300, 100)
    def getResult(self, money):
        return self.cs.acceptCash(money)

if __name__ == '__main__':
    orders = [(100, 10, 'Normal'), (50, 5, 'Normal'), 
              (100, 10, 'Rebate'), (50, 5, 'Rebate'), 
              (100, 10, 'Return'), (50, 5, 'Return')]
    prices = defaultdict(int)
    for price, count, type in orders:
        cc = CashContext(type)
        prices[type] += cc.getResult(price * count)
    for k, v in prices.items():
        print("The price of type %s" % k + " is %d" % v)
    print("The total price of order is %d" % sum(prices.values()))