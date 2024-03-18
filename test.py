c={}

class Character():
    def __init__(self, name) -> None:
        self.species_choices = ["Human", "Alien", "Namekian", "Angel", "Saiyan", "Zenos"]
        self.name = name.lower()
        self.power_lvl= None
        self.title = None
        self.species = None

    def save(self):
        if c.has_key(self.name) :
            return f"{self.name} already exists!!!"
        c[self.name.lower()] = self
        print("Saved!!!!!!")
    
    ########### Update/Create Character #################
    def update(self):
        name = input("Confirm Character name -->  ")
        my_power_lvl = input("Input Character's Power Level--> ")
        species_is_valid=False

        while not species_is_valid:
            species = input("Choose a species(Human, Alien, Namekian, Angel, Saiyan, Zenos):  ")
            species_is_valid = self.verify_species(species) #looping until function returns True

        title= input("Tell us your characters title:   ")
        self.name = name.lower()
        self.power_lvl= my_power_lvl
        self.title = title
        self.species = species
        self.save()
        print("------------------------------------------------------------------------")        
        print("Character successfully Updated!!!!")

    ###### Verify inputed species #######
    def verify_species(self, species) ->bool:
        species_is_valid = False
        if species in self.species_choices:
            species_is_valid = True
        else:
            print("------------------------------------------------------------------------")
            print("This Species is Unheard of, until then please provide a valid species ")
            print("------------------------------------------------------------------------")
        return species_is_valid
        
    ######## Show Character Details ############
    def details(self):
        print(
f"""Character:  {self.name},  {self.title}
Species: {self.species}
Power Level:  {self.power_lvl}
""")

    def populate(self):
        if not self.species and not self.title:
            self.power_lvl = 1000000
            self.species = "Saiyan"
            self.title = "Protector of the Earth"
            self.save()
        else:
            print("______Character is updated already______")
            print("------Population not required-----------")
        
        self.details()

def show_c():
    c_list =list(c.keys())
    print (c_list)

def get_c(person :str)->object:
    if selected_person := c[person.lower()]:
        return selected_person
    else:
        return f"The Character ( {person} ) does not exist"
    


