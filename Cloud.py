import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os


def initialize_firestore():
    # Setup Google Cloud Key - The json file is obtained by going to
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firebaseAccess.json"
    # Use the application default credentials. The projectID is obtianed
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
    'projectId': 'cloub-db',
    })

    # Get reference to database
    db = firestore.client()
    return db

def add_new_Character(db):

    characterName = input("Character Name: ")
    race = input("Race: ")
    classX = input("Class: ")
    lvl = int(input("Level: "))
    str = int(input("Strength: "))
    dex = int(input("Dexterity: "))
    con = int(input("Constitution: "))
    inte = int(input("Intelligence: "))
    wis = int(input("Wisdom: "))
    cha = int(input("Charisma: "))
    ac = int(input("Armor Class: "))
    hp = int(input("Health: "))

    # Check for Characters already existing with the same name.

    result = db.collection("Characters").document(characterName).get()
    if result.exists:
        print("Character already exists.")
        return

    # Build a dictionart to hold contents of firestore document

    data = {"Race" : race, "Class" : classX,
     "Str" : str ,"Dex" : dex, "Con" : con,
      "Int" : inte, "Wis" : wis, "Chr" : cha,
      "AC" : ac, "HP" : hp, "Lvl" : lvl}
    db.collection("Characters").document(characterName).set(data)

def health_gain(db):
    CharacterName = input("Character Name: ")
    amountChanged = int(input("Health Gained: "))

    # Check for an already existing Character by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("Characters").document(CharacterName).get()
    if not result.exists:
        print("Invalid Character Name")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new quanity and then save the 
    # updated dictionary to Firestore.
    data["HP"] += amountChanged
    db.collection("Characters").document(CharacterName).set(data)


def health_loss(db):
    CharacterName = input("Character Name: ")
    amountChanged = int(input("Health lost: "))

    # Check for an already existing Character by the same name.

    result = db.collection("Characters").document(CharacterName).get()
    if not result.exists:
        print("Invalid Character Name")
        return

    data = result.to_dict()

    data["HP"] -= amountChanged
    db.collection("Characters").document(CharacterName).set(data)


def stats_gain(db):
    CharacterName = input("Character Name: ")
    statChoice = input("Choices-\nStr, Dex, Con,\nInt, Wis, Chr\n> ")
    amountChanged = int(input(f"{statChoice} Gained: "))

    # Check for an already existing Character by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("Characters").document(CharacterName).get()
    if not result.exists:
        print("Invalid Character Name")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new quanity and then save the 
    # updated dictionary to Firestore.
    data[statChoice] += amountChanged
    db.collection("Characters").document(CharacterName).set(data)


def stats_loss(db):
    CharacterName = input("Character Name: ")
    statChoice = input("Choices-\nStr, Dex, Con,\nInt, Wis, Chr\n> ")
    amountChanged = int(input(f"{statChoice} lost: "))

    # Check for an already existing Character by the same name.

    result = db.collection("Characters").document(CharacterName).get()
    if not result.exists:
        print("Invalid Character Name")
        return

    data = result.to_dict()

    data[statChoice] -= amountChanged
    db.collection("Characters").document(CharacterName).set(data)


def level_gain(db):
    CharacterName = input("Character Name: ")
    amountChanged = int(input("Levels Gained: "))

    # Check for an already existing Character by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("Characters").document(CharacterName).get()
    if not result.exists:
        print("Invalid Character Name")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new quanity and then save the 
    # updated dictionary to Firestore.
    data["Lvl"] += amountChanged
    db.collection("Characters").document(CharacterName).set(data)


def level_loss(db):
    CharacterName = input("Character Name: ")
    amountChanged = int(input("Levels Lost: "))

    # Check for an already existing Character by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("Characters").document(CharacterName).get()
    if not result.exists:
        print("Invalid Character Name")
        return

    # Convert data read from the firestore document to a dictionary
    data = result.to_dict()

    # Update the dictionary with the new quanity and then save the 
    # updated dictionary to Firestore.
    data["Lvl"] -= amountChanged
    db.collection("Characters").document(CharacterName).set(data)



def level_character(db):
    print("1) Increase Level")        
    print("2) Decrease Level")        
    choice = input("> ")
    if choice =="1":
        level_gain(db)
    elif choice == "2":
        level_loss(db)


def search_characters(db):
    print("Select Query")
    print("1) Show All Characters")        
    print("2) Show Dead Characters")
    print("3) Show Low HP Characters")
    choice = input("> ")
    print()


    # Build and execute the query based on the request made
    if choice == "1":
        results = db.collection("Characters").get()
    elif choice == "2":
        results = db.collection("Characters").where("HP","==",0).get()
    elif choice == "3":
        results = db.collection("Characters").where("HP","<=", 20).get()
    else:
        print("Invalid Selection")
        return
    
    # Display all the results from any of the queries
    print("")
    print("Search Results")
    print(f"{'Name':<20}  {'Race':<10}  {'Class':<10}  {'HP':<10}")
    for result in results:
        item = result.to_dict()
        print(f"{result.id:<20}  {str(item['Race']):<10}  {str(item['Class']):<10}  {item['HP']:<10}")
    print()    


def delete_characters(db):
    print("What character do you want to delete: ")
    name = input("> ")
    print("Are you sure you want to delete this character (y/n): ")
    choice = input("> ")
    if choice == 'y':
        db.collection("Characters").document(name).delete()
 
def health_decide(db):
    print("1) Increase Health")
    print("2) Decrease Health")
    choice = input("> ")
    if choice == "1":
        health_gain(db)
    elif choice == "2":
        health_loss(db)

def stat_change(db):
    print("1) Increase Stats")
    print("2) Decrease Stats")
    choice = input("> ")
    if choice == "1":
        stats_gain(db)
    elif choice == "2":
        stats_loss(db)

def main():
    db = initialize_firestore()
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add New Character")
        print("2) Modify Health")
        print("3) Modify Stats")
        print("4) Modify Level")
        print("5) Search Characters")
        print("6) Delete Characters")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_new_Character(db)
        elif choice == "2":
            health_decide(db)
        elif choice == "3":
            stat_change(db)
        elif choice == "4":
            level_character(db)
        elif choice == "5":
            search_characters(db)                        
        elif choice == "6":
            delete_characters(db)                        

if __name__ == "__main__":
    main()
