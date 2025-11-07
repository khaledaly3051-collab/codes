class Animal:    
    def sound(self):        
      pass
class Dog(Animal):    
    def sound(self):        
          return "Bark"
class Cat(Animal):    
     def sound(self):        
       return "Meow"
 # Polymorphism in action
for Animal in (Dog(), Cat()):    
   print(Animal.sound())