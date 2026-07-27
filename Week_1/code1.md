
**Class, Object, Attribute, Method**

A class is a blueprint.  
It is not the finished thing. It is only the plan from which many finished things can be made.

An object is one concrete entity created from that blueprint.  
It holds data (attributes) and can perform actions (methods). A variable simply points to an object; the variable is not the object itself.

An attribute is a named piece of data that lives inside an object.  
It can hold any kind of value — a number, a text, a list, or even another object.

A method is a function defined inside the class.  
When we call it, it works on the particular object that owns it.

---

**Why this matters**

Imagine we are building a video game and need many enemies: goblins, orcs, trolls.  
Each enemy needs a name, health points, and attack power.

Without a class we would write:

```python
goblin_name = "Goblin"
goblin_health = 50
goblin_attack = 10

orc_name = "Orc"
orc_health = 80
orc_attack = 15
```

This works for two enemies.  
For one hundred or ten thousand it becomes a swamp of scattered variables. Changing one rule means hunting through dozens of places.

A class lets us write the plan once. Then we create as many enemy objects as we need from that single plan. Everything stays together and stays manageable.

---

**The Simplest Class**

A class begins as an empty plan:

```python
class Enemy:
    pass
```

We may now create an object from it:

```python
goblin = Enemy()
```

The object exists, yet it holds nothing.  

**Attributes**

We may attach data after creation:

```python
goblin.name = "Goblin"
goblin.health = 50
goblin.attack_power = 10
```

Each name stores a value that belongs to that particular object.

**A Method**

A method is a function that lives inside the class and works on the object that calls it.  
Notice that the attribute and the method must carry different names, otherwise one will hide the other.

```python
class Enemy:
    def strike(self):
        print(f"{self.name} attacks with {self.attack_power} damage!")
```

We create the object, give it data, then call the method:

```python
goblin = Enemy()
goblin.name = "Goblin"
goblin.attack_power = 10
goblin.strike()
```

**The __init__ Method**

Instead of attaching attributes after creation, we may set them at the moment the object is born. That is the work of `__init__`.

```python
class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def strike(self):
        print(f"{self.name} attacks with {self.attack_power} damage!")
```

Creation now becomes simple and safe:

```python
goblin = Enemy("Goblin", 50, 10)
orc = Enemy("Orc", 80, 15)

goblin.strike()
orc.strike()
```

**Practice Task**

Write a class called Hero that contains:

- an `__init__` method taking name, health, and attack_power  
- a method called fight that prints: “[name] fights with [attack_power] damage!”  

Then create one hero named “Aragon” with health 100 and attack_power 25, and call its fight method.

---

**A Clear Hero Class**

Here is a complete, working example. Every line is explained in plain language.

```python
# We create a new blueprint called Hero.
# By custom, the name of a class begins with a capital letter.
class Hero:

    # __init__ is the constructor.
    # It runs automatically the moment a new Hero object is born.
    # self always refers to the object that is being created.
    # name, health and attack are the values we supply when we create the object.
    def __init__(self, name, health, attack):
        # We store the given name inside this particular object.
        self.name = name

        # We store the given health inside this particular object.
        self.health = health

        # We store the given attack power inside this particular object.
        self.attack = attack

    # fight is a method that belongs to every Hero.
    # self lets the method read the data of the object that called it.
    def fight(self):
        # We print a short message using this object's own name and attack values.
        print(f"{self.name} fights with {self.attack} damage!")


# We create one Hero object and keep a reference to it in the variable jones.
jones = Hero("Jones", 90, 35)

# We ask the jones object to perform its fight method.
# The output will be: Jones fights with 35 damage!
jones.fight()
```

**What We Keep in Mind**

1. self is always the first parameter of every method inside a class.  
2. __init__ runs by itself when a new object is created.  
3. Attributes are attached with the form self.attribute = value.  
4. Methods are called on an object: object.method(). Python passes self automatically.  
5. Each object carries its own separate copy of the attributes.

**Small Practice**

Create a second hero named “Smith” with health 80 and attack 20.  
Then call the fight method on both jones and smith.

---

**Methods That Work With Other Objects**

When we write `person1.fight()`, Python quietly turns it into:

```python
Hero.fight(person1)
```

That is the whole reason `self` exists.  
`self` is simply the object that is being asked to act. It is the object’s way of saying “me”.

**A Method That Affects Another Object**

We can give a method an extra parameter so that one object can act on another:

```python
def attack_enemy(self, other_hero):
    print(f"\n{self.name} attacks {other_hero.name}!")
    other_hero.health -= self.attack
    print(f"{other_hero.name} now has {other_hero.health} health.")
```

- `self` is the attacker.  
- `other_hero` is the target — it is an object, not a class.  
- We change the target’s health by writing directly to `other_hero.health`.

**Complete Working Example**

```python
class Hero:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def fight(self):
        print(f"{self.name} fights with {self.attack} damage!")

    def attack_enemy(self, other_hero):
        print(f"\n{self.name} attacks {other_hero.name}!")
        other_hero.health -= self.attack
        print(f"{other_hero.name} now has {other_hero.health} health.")


person1 = Hero("Jones", 90, 35)
person2 = Hero("John", 80, 20)
person3 = Hero("Jack", 75, 28)

person1.fight()
person2.fight()
person1.attack_enemy(person3)
```

Expected output:

```
Jones fights with 35 damage!
John fights with 20 damage!

Jones attacks Jack!
Jack now has 40 health.
```

**What We Keep in Mind**

- Inside the method, `other_hero` is an ordinary object that was passed in.  
- We may read or change any of its attributes.  
- Each object still keeps its own separate data.

**Small Practice**

Add a second call so that person3 attacks person1.  
Observe that both objects keep their own health values independently.

---

**Why self Always Points to the Caller**

When we write `person1.attack_enemy(person3)`, the object that sits before the dot becomes `self`.  
That is why `self.name` is “Jones” and `self.attack` is 35.  

If we later write `person2.attack_enemy(person3)`, then `self` becomes person2.  
Its name is “John” and its attack power is 20.  

`self` is never fixed. It is simply the object that is performing the action.

**The Correct Way to Apply Damage**

We must never hard-code a number such as 35.  
We use the attacker’s own attribute:

```python
other_hero.health -= self.attack
```

Each hero then deals damage equal to its own strength.

**Complete Working Example**

```python
class Hero:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def fight(self):
        print(f"{self.name} fights with {self.attack} damage!")

    def attack_enemy(self, other_hero):
        print(f"\n{self.name} attacks {other_hero.name}!")
        other_hero.health -= self.attack
        print(f"{other_hero.name} now has {other_hero.health} health.")


person1 = Hero("Jones", 90, 35)
person2 = Hero("John", 80, 20)
person3 = Hero("Jack", 75, 28)

person1.attack_enemy(person3)   # 75 - 35 = 40
person2.attack_enemy(person3)   # 40 - 20 = 20

print(f"\nFinal health of {person3.name}: {person3.health}")
```

Expected output:

```
Jones attacks Jack!
Jack now has 40 health.

John attacks Jack!
Jack now has 20 health.

Final health of Jack: 20
```

**What We Keep in Mind**

- `self` is always the object that called the method.  
- Using `self.attack` lets every object bring its own power.  
- The target’s health is updated and stays updated for the next attack.

**Small Practice**

Make person3 attack person1 once.  
Then print the final health of both person1 and person3.

---

**A Complete Text-Based Battle System**

We now bring together everything we have learned into a small, working combat system.

A Hero can:

- strike another Hero and permanently reduce the target’s health  
- fall when health reaches zero or below  
- attempt to restore its own health, but only while still alive  

```python
class Hero:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def fight(self):
        print(f"{self.name} fights with {self.attack} damage!")

    def attack_enemy(self, other_hero):
        print(f"\n{self.name} attacks {other_hero.name}!")
        other_hero.health -= self.attack

        if other_hero.health <= 0:
            other_hero.health = 0
            print(f"{other_hero.name} now has {other_hero.health} health.")
            print(f"{other_hero.name} is defeated.")
            return

        print(f"{other_hero.name} now has {other_hero.health} health.")

    def heal(self, amount):
        if self.health <= 0:
            print(f"{self.name} tries to heal, yet nothing happens — the hero has already fallen.")
            return

        self.health += amount
        print(f"\n{self.name} recovers {amount} health and now stands at {self.health}.")


# Three distinct combatants
person1 = Hero("Jones", 90, 35)
person2 = Hero("John", 80, 60)
person3 = Hero("Jack", 75, 28)

# Two sequential attacks on the third combatant
person1.attack_enemy(person3)
person2.attack_enemy(person3)

# The fallen combatant attempts recovery
person3.heal(35)
```

**What the Code Demonstrates**

- One blueprint produces many independent objects.  
- `self` is always the object that was asked to act.  
- One object may change the state of another.  
- A simple check prevents a fallen hero from restoring itself.  
- Early return stops further work once defeat is certain.

**Small Practice**

Change the attack values so that the third hero survives the first blow yet falls to the second.  
Then let a living hero heal and observe the difference.

---

**Reviewing the Battle System**

We now pause to examine the exact behaviour of the code we have written.

```python
person1.attack_enemy(person3)   # 75 - 35 → 40
person2.attack_enemy(person3)   # 40 - 60 → 0
person3.heal(35)                # refused because health is already 0
```

The console shows:

```
Jones attacks Jack!
Jack now has 40 health.

John attacks Jack!
Jack now has 0 health.
Jack is defeated.

Jack tries to heal, yet nothing happens — the hero has already fallen.
```

**What the Sequence Demonstrates**

- Damage is applied using the attacker’s own `self.attack`.  
- Health is clamped at zero once it falls to or below that line.  
- An early `return` stops any further work inside the method.  
- The heal method contains a guard that refuses action when the hero is already fallen.  

These small checks turn a simple class into reliable behaviour.

**What We Have Solidly Grasped**

- A class is a single blueprint.  
- Each object carries its own independent state.  
- `self` is always the object that was asked to act.  
- Methods may read or change the state of other objects.  
- Guard clauses and early returns keep the logic safe.

**Small Practice**

Adjust the attack values so that the third hero survives the first strike, falls to the second, and then attempts to heal.  
Observe that the final heal is correctly refused.