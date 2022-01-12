Dm exo 3 option A :

1) import turtle

2) x = immeuble[0] / y = immeuble[1] / z = immeuble[2] / turtle.color(rgb)

3) def trace_ville(list) :
	for i in range(len(list)) :
		Trace_immeuble(list[i],(255,255,255))

4) 10 / skyline[-1][1] /
def trace_skyline ( skyline ) :
 	turtle . colormode (255)
 	turtle . color ((0 ,0 ,0) )
 	abs = skyline[0][0]
 	ord = skyline[0][1]
 	turtle . setx ( abs )
 	turtle . sety ( ord )
 	for i in range (1 , len ( skyline ) ) :
 		if skyline[i-1][0] != abs :
                                  	abs = skyline[i][0]
 			turtle . setx ( abs *10)
 		else :
                             	ord = skyline[i][1]
 			turtle . sety ( ord *10)

b) 1) def hauteur_max_immeubles(skyline) :
	If len(skyline) == 0 :
		Return None
	else :
		max = 0
		For i in range(len(skyline)-1) :
			If skyline[i][2] > skyline[i+1][2] :
				max = skyline[i][2]
			else :
				max = skyline[i+1][2]
	Return max

b) 2)
max = 0
def hauteur max immeubles rec(skyline,n) :
	If n == -1 :
		Return max
	elif len(skyline) == 0 :
		Return none
	else :
		If skyline[n][2] > skyline[n-1][2] :
			max = skyline[n][2]
			Return hauteur max immeubles rec(skyline,n-1)
		Else :
			max = skyline[n-1][2]
hauteur max immeubles rec(skyline,n-1)

c) 1) On divise en 2 une liste pour trier indépendamment les sous listes pour ensuite recombiner ces 2 listes afin d’avoir une liste de départ trier
c) 2) tri fusion / tri rapide
c) 3) On divise bien la ville en 2 villes : ville1, ville2 pour ensuite les envoyer dans une fonction de fusion
c) 4) Je n'arrrive pas à comprendre
