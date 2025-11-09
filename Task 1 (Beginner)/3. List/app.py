"""1. You have a list of superheroes representing the Justice League.
justice_league = ["Superman","Batman","WonderWoman","Flash","Aquaman","Green Lantern"]"""
#Perform the following tasks:
#1. Calculate the number of members in the Justice League.
justice_league = ["Superman","Batman","WonderWoman","Flash","Aquaman","Green Lantern"]

print(f"Number of members in Justice League: {len(justice_league)}")
   
#2. Batman recruited Batgirl and Nightwing as new members. Add them to your list.

justice_league.append("Batgirl")
justice_league.append("Nightwing")
print(f"After adding new members: {justice_league}")

"""4. Aquaman and Flash are having conflicts, and you need to separate them. 
Choose either "Green Lantern" or "Superman" and move them in between Aquaman and Flash.""" 

aquaman_index = justice_league.index("Aquaman")
flash_index = justice_league.index("Flash")
justice_league.remove("Green Lantern")
justice_league.insert(flash_index, "Green Lantern")
print(f"After separating Aquaman and Flash: {justice_league}")


"""5. The Justice League faced a crisis, and Superman decided toassemble a new team. 
Replace the existing list with the following new members: 
     "Cyborg","Shazam","Hawkgirl","Martian Manhunter","Green Arrow"."""

justice_league = ["Cyborg","Shazam","Hawkgirl","Martian Manhunter","Green Arrow"]
print(f"New Justice League team: {justice_league}")

#6. Sort the Justice League alphabetically. The hero at the 0th index will become the new leader

justice_league.sort()
print(f"Sorted Justice League: {justice_league}")
print(f"New leader: {justice_league[0]}")

#(BONUS: Can you predict who the new leader will be?)
print("\nBonus Answer:")
print("Prediction: Cyborg will be the new leader")
print("Reason: When sorted alphabetically, 'Cyborg' comes first among the team members")
print("Order: Cyborg < Green Arrow < Hawkgirl < Martian Manhunter < Shazam")
