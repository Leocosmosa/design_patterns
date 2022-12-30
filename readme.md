# 商品状态+商品审核模块设计：
## 1. 方案设计：
采用状态+职责链模式设计模块。商品状态部分State为父类定义抽象方法，OnSaleState、AbsentState、LoadingState为子类实现具体商品状态，Product为具体商品；商品上架审核部分Request为商品审核单记录补货的商品和数量，Auditor为父类定义审核人员，InventoryAuditor、SaleAuditor、ManagementAuditor为子类实现具体审核人员。
此外，Inventory为现有商品在售情况，包括商品类别和商品数量，当某商品数量=0时将进入商品缺货状态，当商品审核单被驳回时将进入商品上架状态，当初始化和商品审核单被批准时将进入商品在售状态。
## 2.代码实现及截图：
```python
class State(object):
    def __init__(self, p):
        pass
    def sell(self, p, count):
        pass

# 在售状态
class OnSaleState(State):
    def __init__(self, p):
        print("商品", p.name, "在售中")
    def sell(self, p, count):
        if count < p.count:
            p.count -= count
            print("商品", p.name, "卖出数量", count, "剩余数量", p.count)
        elif count == p.count:
            p.count -= count
            print("商品", p.name, "卖出数量", count, "剩余数量", p.count)
            p.set_state(AbsentState(p))
        else:
            print("商品", p.name, "剩余数量不足")
# 缺货状态
class AbsentState(State):
    def __init__(self, p):
        print("商品", p.name, "缺货中，需要补货")
    def sell(self, p, count):
        print("商品", p.name, "缺货中，无法购买")

# 上架状态
class LoadingState(State):
    def __init__(self, p):
        print("商品", p.name, "上架中，等待批准")
    def sell(self, p, count):
        print("商品", p.name, "上架中，无法购买")

# 商品
class Product(object):
    __state = None
    __price = 0
    __count = 0
    __name = None
    def __init__(self, price, count, name):
        self.__price = price
        self.__count = count
        self.__name = name
        self.__state = OnSaleState(self)

    def set_state(self, state):
        self.__state = state
    def sell(self, count):
        self.__state.sell(self, count)

    def get_price(self):
        return self.__price
    def set_price(self, price):
        self.__price = price
    def get_count(self):
        return self.__count
    def set_count(self, count):
        self.__count = count
    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    price = property(get_price, set_price)
    count = property(get_count, set_count)
    name = property(get_name, set_name)

# 商品审核单
class Request(object):
    __price = None
    __count = None
    __name = None
    def get_price(self):
        return self.__price
    def set_price(self, value):
        self.__price = value
    def get_count(self):
        return self.__count
    def set_count(self, value):
        self.__count = value
    def get_name(self):
        return self.__name
    def set_name(self, value):
        self.__name = value
    price = property(get_price,set_price)
    count = property(get_count,set_count)
    name = property(get_name,set_name)

# 审核人员
class Auditor(object):
    superior = None
    def __init__(self,name):
        self.name = name
    def set_superior(self, superior):
        self.superior = superior
    def request_applications(self, request, inventory):
        pass

# 库存审核人
class InventoryAuditor(Auditor):
    def __init__(self, name):
        super().__init__(name)
    def request_applications(self, request, inventory):
        if request.name in inventory:
            p = inventory[request.name]
        else:
            p = Product(0, 0, request.name)
            inventory[request.name] = p
        p.set_state(LoadingState(p))
        if self.superior != None:
            return self.superior.request_applications(request, inventory)
        else:
            p.set_state(OnSaleState(p))
            return True

# 销售审核人
class SaleAuditor(Auditor):
    def __init__(self, name):
        super().__init__(name)
    def request_applications(self, request, inventory):
        p = inventory[request.name]
        if request.price >= 100 and request.count >= 10:
            print('价格为', request.price, '数量为', request.count, '的商品', request.name, '申请被批准')
            p.set_state(OnSaleState(p))
            return True
        else:
            if self.superior != None:
                return self.superior.request_applications(request, inventory)
            else:
                p.set_state(OnSaleState(p))
                return True

# 审核管理人
class ManagementAuditor(Auditor):
    def __init__(self,name):
        super().__init__(name)
    def request_applications(self, request, inventory):
        p = inventory[request.name]
        if request.price >= 50 and request.count >= 5:
            print('价格为', request.price, '数量为', request.count, '的商品', request.name, '申请被批准')
            p.set_state(OnSaleState(p))
            return True
        elif request.price < 50:
            print('价格为', request.price, '数量为', request.count, '的商品', request.name, '申请被驳回，价格太便宜')
            return False
        elif request.count < 5:
            print('价格为', request.price, '数量为', request.count, '的商品', request.name, '申请被驳回，数量太少')
            return False

if __name__ == '__main__':
    initial_products = [(100, 10, 'P1'), (50, 5, 'P2'), (100, 10, 'P3')]
    Inventory = {}
    zhangsan = InventoryAuditor("张三")
    lisi = SaleAuditor("李四")
    wangwu = ManagementAuditor("王五")
    zhangsan.superior = lisi
    lisi.superior = wangwu
    for price, count, name in initial_products:
        if name not in Inventory:
            Inventory[name] = Product(price, count, name)
        else:
            Inventory[name].price = price
            Inventory[name].count += count
    
    print("初始商品状态为：")
    for p in Inventory.values():
        print("商品", p.name, "价格为", p.price, "数量为", p.count)

    order_products = [(10, 'P1'), (8, 'P2'), (6, 'P3'), (4, 'P4')]
    for count, name in order_products:
        print("收到商品", name, "订单 数量为", count)
        if name not in Inventory:
            print("商品", name, "缺货中，无法购买")
        else:
            Inventory[name].sell(count)
    
    loading_products = [(120, 10, 'P1'), (120, 2, 'P3'), (60, 5, 'P4'),
                    (40, 5, 'P5')]
    for price, count, name in loading_products:
        request = Request()
        request.price = price
        request.count = count
        request.name = name
        approved = zhangsan.request_applications(request, Inventory)
        if approved:
            if name not in Inventory:
                Inventory[name] = Product(price, count, name)
                print('价格为', price, '数量为', count, '的商品', name, '已上架')
            else:
                Inventory[name].price = price
                Inventory[name].count += count
                print('价格更新为', price, '数量为', count, '的商品', name, '已上架')

    print("上架后商品状态为：")
    for p in Inventory.values():
        print("商品", p.name, "价格为", p.price, "数量为", p.count)

    order_products = [(1, 'P1'), (1, 'P2'), (1, 'P3'), (1, 'P4'), (1, 'P5')]
    for count, name in order_products:
        print("收到商品", name, "订单 数量为", count)
        if name not in Inventory:
            print("商品", name, "缺货中，无法购买")
        else:
            Inventory[name].sell(count)
```
![](./screenshot.png)
## 3.采用理由：
状态模式用于设计商品在售、缺货、上架三种状态之间的转换，职责链模式用于表示上架状态下的商品的上架流程，即商品审核单在库存审核人、销售审核人、审核管理人三种节点的审核情况。
