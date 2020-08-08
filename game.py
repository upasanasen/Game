
import random
Dbin = {1:"plastic", 2:"biodegradable", 3:"recyclable", 4:"paper", 5:"glass"}
Dwaste = {"polybags": 1, "plastic wraps": 1,"plastic bottles": 1, "banana peels": 2, "egg shels": 2, "molded breads": 2, "tetrapacked milk boxes": 3, "paper boxes": 3, "egg trays": 3, "notebooks": 4, "tissues": 4, "papertowels": 4, "glass bottles": 5, "glass jars": 5, "broken glass windows": 5}
waste = Dwaste.keys()
Score = 0
for  step in range(10):
    N = random.randint(0, len(waste)-1)
    print(waste[N]) 
    bintype = input("choose the dustbin: (hint: (1)plastic, (2)biodegradable, (3)recyclable, (4)paper, (5)glass):" )
    # checking the answer(if correct get one point)
    if (bintype == Dwaste[waste[N]]):
        Score = Score+1
        print("That's right") 
    else:
        print("tumse na ho payega! \n the correct answer is: (%s)%s"%(str(Dwaste[waste[N]]),Dbin[Dwaste[waste[N]]] ) )

print("Final Score: ", Score)





