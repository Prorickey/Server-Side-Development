class Bob:

    def __init__(self):
        self.__name = 'Bob'

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, newName):
        self.__name = newName
    

b = Bob()
b.name = 'Lemming'
print(b.name)