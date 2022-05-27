# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def print_recipe(recipe):
    """Pretty print recipe, which is a dictionary whose keys are
    ingredients and whose values are their corresponding amounts.
    """
    for k,v in recipe.items():
        print(f'{k}: {v}')


def read_recipe(recipe_file_name):
    """Read recipe file 'recipe_file_name', and return ingredients as a
    dictionary whose keys are ingredients and whose values are the
    corresponding amounts.
    """
    with open(recipe_file_name, 'r')as file:
        d = {}
        for l in file:
            words = l.split(',')
            f = ['',''] #f:formated
            for i in range(len(words)):
                f[i] = words[i].strip()
                f[i] = f[i].strip('\n')
                f[i] = f[i].strip('\t')
            if f[0] != '':
                d[f[0]] = int(f[1])
        return d
    
def write_recipe(recipe, recipe_file_name):
    """Write recipe to a file named recipe_file_name."""
    with open(recipe_file_name, 'w')as file:
        for k,v in recipe.items():
            file.write(f'{k},{v}\n')
            
def read_fridge(fridge_file_name):
    """Read fridge file 'fridge_file_name', and return the ingredients
    held in the given fridge as an ingredient=amount dictionary.
    """
    with open(fridge_file_name, 'r')as file:
        d = {}
        for l in file:
            words = l.split(',')
            f = ['',''] #f:formated
            for i in range(len(words)):
                f[i] = words[i].strip()
                f[i] = f[i].strip('\n')
                f[i] = f[i].strip('\t')
            if f[0] == '':
                pass
            elif f[0] not in d:
                d[f[0]] = int(f[1])
            else:
                d[f[0]] = d[f[0]] + int(f[1])
        return d

def is_cookable(recipe_file_name, fridge_file_name):
    """Return True if the contents of the fridge named fridge_file_name
    are sufficient to cook the recipe named recipe_file_name.
    """
    rec = read_recipe(recipe_file_name)
    fri = read_fridge(fridge_file_name)
    #i:ingredient, a:amount
    for i,a in rec.items():
        if(i not in fri):
            return False
        elif a > fri[i]:
            return False
    return True

def add_recipes(recipes):
    """Return a dictionary representing the sum of all of
    the recipe dictionaries in recipes.
    """
    d = {}
    for r in recipes:
        for ing,amount in r.items():
            if ing not in d:
                d[ing] = amount
            else:
                d[ing] = d[ing] + amount
    return d

def create_shopping_list(recipe_file_names, fridge_file_name):
    """Return the shopping list (a dictionary of ingredients and
    amounts) needed to cook the recipes named in recipe_file_names,
    after the ingredients already present in the fridge named
    fridge_file_name have been used.
    """
    recipes = []
    buy = {}
    fridge = read_fridge(fridge_file_name)
    for f in recipe_file_names:
        recipes.append(read_recipe(f))
    total_ing = add_recipes(recipes)
    for i,a in total_ing.items():
        if(i not in fridge):
            buy[i] = a
        elif(a > fridge[i]):
            buy[i] = a - fridge[i]
    return buy   


def total_price(shopping_list, market_file_name):
    """Return the total price in millicents of the given shopping_list
    at the market named market_file_name.
    """
    price = 0
    market = read_recipe(market_file_name)
    for i,a in shopping_list.items():
        price += a * market[i]
    return price   


def find_cheapest(shopping_list, market_file_names):
    """Return the name of the market in market_file_names
    offering the lowest total price for the given shopping_list,
    together with the total price.
    """
    pd = {}
    prices = []
    for f in market_file_names:
        pd[total_price(shopping_list, f)] = f
        prices.append(total_price(shopping_list, f))
    minprice = min(prices) 
    return (pd[minprice], minprice)


def update_fridge(fridge_file_name, recipe_file_names, market_file_names, new_fridge_file_name):
    """Compute the shopping list for the given recipes after the
    ingredients in fridge fridge_file_name have been used; find the cheapest
    market; and write the new fridge contents to new_fridge_file_name.
    Print the shopping list, the cheapest market name, and the total
    amount to be spent at that market.
    """
    print('Shopping list:')
    shopping_list = create_shopping_list(recipe_file_names, fridge_file_name)
    print_recipe(shopping_list)
    cheapest = find_cheapest(shopping_list, market_file_names)
    fridge = read_fridge(fridge_file_name)
    print(f'Market: {cheapest[0]}\nTotal cost: {cheapest[1]}')
    #fridge + shopping list
    new_fridge = add_recipes([shopping_list, fridge])
    write_recipe(new_fridge, new_fridge_file_name)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    