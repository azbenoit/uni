# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Trobble:
    """Trobbles: simplified digital pets.

    Data Attributes:
    name -- the Trobble's name.
    sex -- 'male' or 'female'.
    age -- a non-negative integer
    health -- an integer between 0 (dead) and 10 (full health) inclusive
    hunger -- a non-negative integer (0 is not hungry)
    """
    def __init__(self, name, sex):
        self.health = 10
        self.age = 0
        self.hunger = 0 
        self.name = name
        self.sex = sex
    
    def check(self):
        if self.hunger <0:
            self.hunger = 0
        if self.health > 10:
            self.health = 10
            
    def __str__(self):
        x = f'{self.name}: {self.sex}, health {self.health}, '
        x += f'hunger {self.hunger}, age {self.age}'
        return x
        
    def next_turn(self):
        if(self.health != 0):
            self.age += 1
            self.hunger += self.age
            self.health -= self.hunger // 20
            if (self.health < 0):
                self.health = 0
            
    def feed(self):
        self.hunger -= 25
        self.check()
        
            
    def cure(self):
        self.health += 5
        self.check()
            
    def have_fun(self):
        self.health += 2
        self.check()
        
    def is_alive(self):
        return self.health > 0
    


def get_name():
    return input('Please give your new Trobble a name: ')

def get_sex():
    sex = None
    while sex is None:
        prompt = 'Is your new Trobble male or female? Type "m" or "f" to choose: '
        choice = input(prompt)
        if choice == 'm':
            sex = 'male'
        elif choice == 'f':
            sex = 'female'
    return sex

def get_action(actions):
    while True:
        prompt = f"Type one of {', '.join(actions.keys())} to perform the action: "
        action_string = input(prompt)
        if action_string not in actions:
            print('Unknown action!')
        else:
            return actions[action_string]
        
def play():
    name = get_name()
    sex = get_sex()
    trobble = Trobble(name, sex)
    actions = {'feed': trobble.feed, 'cure': trobble.cure}
    while trobble.is_alive():
        print('You have one Trobble named ' + str(trobble))
        action = get_action(actions)
        action()
        trobble.next_turn()
    print(f'Unfortunately, your Trobble {trobble.name} has died at the age of {trobble.age}')



def mate(trobble1, trobble2, name_offspring):
    """Check if the given Trobbles can procreate and if so give back a new
    Trobble that has the sex of trobble1 and the name 'name_offspring'.
    Otherwise, return None.
    """
    if(trobble1.age <4 or trobble2.age <4):
        return None
    elif(trobble1.sex == trobble2.sex):
        return None
    elif(not trobble1.is_alive() or not trobble2.is_alive()):
        return None
    else:
        return Trobble(name_offspring, trobble1.sex)
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    






































            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            