import urllib.request as request
from bs4 import BeautifulSoup
from constants import armor_table
from titlecase import titlecase
import re



def get_price(name):
    name = name.lower()
    name = name.strip()
    print(name)
    if (name[0] == '+' and ord(name[1]) >= 49 and ord(name[1]) <= 53):
        item_name = name[2:]
        item_name = item_name.strip()
        item_name = item_name.lower().capitalize()

        keyword = ' of '
        index = item_name.find(keyword)



        pluses = ord(name[1]) - 49
        if index != -1:


            buffs = item_name[index + 4:].split(',')
            item_name = item_name[:index]
        else:
            buffs = []
        price = get_armor(item_name)
        if price != -1:
            enchant = 0
            for buff in buffs:
                cost = get_armor_enchant(buff)
                if cost[1] == 1:
                    pluses += cost[0]
                elif cost[1] == 2:
                    enchant += cost[0]
                else:
                    return -1
            enchant += armor_table[pluses]
            total_price = convert_gold(price) + enchant + 150
            return f"This {name} is worth {total_price} gp with {price} from the base armor, +150 from Masterwork, and {enchant} from enchantments"
        price, special = get_weapon(item_name, True)
        if price != -1:
            enchant = 0
            for buff in buffs:
                cost = get_weapon_enchant(buff)
                if cost[1] == 1:
                    pluses += cost[0]
                elif cost[1] == 2:
                    enchant += cost[0]
                else:
                    return -1
            enchant += 2 * armor_table[pluses]
            total_price = convert_gold(price) + enchant
            if special and 'double' in special:
                total_price += 600
                return f"This {name} is worth {total_price} gp with {price} from the base weapon, +600 from Masterwork, and {enchant} from enchantments"
            else:
                total_price += 300
                return f"This {name} is worth {total_price} gp with {price} from the base weapon, +300 from Masterwork, and {enchant} from enchantments"
        return - 1
    else:
        item_list = [get_wonderous_item, get_weapon, get_armor]
        iterate(name, item_list)

def get_wonderous_item(name):
    name = titlecase(name)
    name = request.quote(name)
    path = f"http://aonprd.com/MagicWondrousDisplay.aspx?FinalName={name}"
    page = request.urlopen(path)
    soup = BeautifulSoup(page, features='html.parser')
    cost_obj = soup.find('b', text="Price")
    if cost_obj:
        price = cost_obj.next_sibling
        return (price.strip())
    else:
        print("not a wonderous item")
        return -1

def get_armor(name):
    name = name.lower().capitalize()
    path = request.quote(name)
    path = f"http://aonprd.com/EquipmentArmorDisplay.aspx?ItemName={path}"
    page = request.urlopen(path)
    soup = BeautifulSoup(page, features='html.parser')
    cost_obj = soup.find('b', text="Cost")
    if cost_obj:
        price = cost_obj.next_sibling
        return (price.strip())
    else:
        print("not armor")
        return -1
def get_weapon(name, special = False):
    name = name.lower().capitalize()
    path = request.quote(name)
    path = f"http://aonprd.com/EquipmentWeaponsDisplay.aspx?ItemName={path}"
    page = request.urlopen(path)
    soup = BeautifulSoup(page, features='html.parser')
    cost_obj = soup.find('b', text="Cost")
    if cost_obj:
        price = cost_obj.next_sibling
        if special:
            special_field = soup.find('b', text="Special")
            if special_field:
                return (price.strip(), special_field.next_sibling)
            else:
                return(price.strip(), None)
    else:
        print("not weapon")
        if special:
            return -1, None
        else:
            return -1

#returns
# 1 = enchant bonus
# 2 = flat cost
def get_weapon_enchant(name):
    name = name.strip()
    name = titlecase(name)
    name = request.quote(name)
    path = f"http://aonprd.com/MagicWeaponsDisplay.aspx?ItemName={name}"
    page = request.urlopen(path)
    soup = BeautifulSoup(page, features='html.parser')
    cost_obj = soup.find('b', text="Price")
    if cost_obj:
        price = cost_obj.next_sibling
        price = price.strip()
        price = price.strip(';')
        if price[-5:] == 'bonus':
            return int(price[1]), 1
        else:
            price = price.strip(';')
            return convert_gold(price), 2
    else:
        print("not a weapon enchant")
        return -1, -1

#returns
# 1 = enchant bonus
# 2 = flat cost
def get_armor_enchant(name):
    name = name.strip()
    name = titlecase(name)
    name = request.quote(name)
    path = f"http://aonprd.com/MagicArmorDisplay.aspx?ItemName={name}"
    page = request.urlopen(path)
    soup = BeautifulSoup(page, features='html.parser')
    cost_obj = soup.find('b', text="Price")
    if cost_obj:
        price = cost_obj.next_sibling
        price = price.strip()
        price = price.strip(';')
        if price[-5:] == 'bonus':
            return int(price[1]), 1
        else:
            price = price.strip(';')
            return convert_gold(price), 2
    else:
        print("not a armor enchant")
        return -1, -1

def iterate(name, item_list):
    price = -1
    for func in item_list:
        price = func(name)
        if price != -1:
            return price
    return price
def convert_gold(input):
    if input[-2:] == 'gp':
        return int(re.sub("[^0-9]", "", input))
    if input[-2] == 'sp':
        return int(re.sub("[^0-9]", "", input)) / 10
    if input[-2] == 'cp':
        return int(re.sub("[^0-9]", "", input)) / 100
    else:
        raise ValueError("input must end with \'gp\', \'sp\', or \'cp\'")

if __name__ == '__main__':
    print (get_price("+1 Harpoon of keen"))
