"""
This module contains some basic permutation group algorithms, for:

-computing orbits and transversals, 
-computing generators for a stabilizer, and
-reducing a generating set to an equivalent one of at most quadratic size.

Most important functions:

 Orbit		(computes orbit and transversal)
 Stabilizer	(computes generators for a stabilizer subgroup)

Use this with permutation objects generated by the module permv2.py
(Or your own permutation objects that support equivalent methods).
"""

# basicpermutationgroup.py: based on fir/perm/basicpermutationgroup
#	uses permv2, reversed composition.
# 18-03-2015, Paul Bonsma


from permv2 import permutation


def Orbit(generators, el, returntransversal=False):
    """
	<generators> should be a Python list of permutations (from permv2.py), which
	represent a generating set of a permutation group H.
	<el> is an element of the ground set (which should be from 0...n-1).
	
	This function returns the orbit <O> of <el> in group H, as a python list.
	
	If <returntransversal> = True, it also returns a transversal <U>, which is
	an equal length python list:
	For every index i, U[i] is a permutation from H that maps <el> to O[i].
	
	(The lists O and U are returned as a 2-tuple.)
	
	See the lecture slides for this algorithm in pseudocode, and an example.
	"""
    O = [el]
    if len(generators) == 0:
        return O, None
    n = generators[0].n
    memberVec = [0] * n
    memberVec[el] = 1
    if returntransversal:
        U = [permutation(n)]
    ind = 0
    while ind < len(O):
        el = O[ind]
        for P in generators:
            mapel = P[el]
            if not memberVec[mapel]:
                memberVec[mapel] = 1
                O.append(mapel)
                if returntransversal:
                    U.append(P * U[ind])
        ind += 1
    for el in O:
        memberVec[el] = 0
    if returntransversal:
        return O, U
    else:
        return O


def SchreierGenerators(generators, el):
    """
	(Mostly for internal use.)
	Given a generating set <generators> (a Python list containing permutations) that
	generate a group H, and an element <el> (from the ground set 0...n-1), 
	this function returns a number of permutations that are in the <el>-stabilizer subgroup
	of H, which is in fact a generating set for this stabilizer subgroup.
	This may be a long list, which may even contain duplicates.
	"""
    O, U = Orbit(generators, el, True)
    SchrGen = []
    for ind in range(len(O)):
        el = O[ind]
        for P in generators:
            mapel = O.index(P[el])
            newgen = -U[mapel] * P * U[ind]
            if not newgen.istrivial():
                SchrGen.append(newgen)
    return SchrGen


def FindNonTrivialOrbit(generators):
    """
	Given a generating set <generators> (a Python list containing permutations),
	this function returns an element <el> with a nontrivial orbit in the group
	generated by <generators>, or <None> if no such element exists.
	(Useful for order computation / membership testing.)
	"""
    if generators == []:
        return None
    n = generators[0].n
    for P in generators:
        for el in range(n):
            if P[el] != el:
                return el


def Reduce(generators, wordy=0):
    """
	Given a generating set <generators> (a Python list containing permutations) that 
	generates a group H, this function returns a possibly smaller generating set for the
	same group H (but certainly not larger). 
	The resulting generating set will contain less than n^2
	permutations, when the permutations are on n elements.
	(Set <wordy> =1 or 2 to see what is going on exactly.)
	"""
    if wordy >= 1:
        print("  Reducing. Input length:", len(generators))
    if generators == []:
        return generators
    n = generators[0].n
    outputgenerators = []
    todo = generators
    while todo != []:
        el = FindNonTrivialOrbit(todo)
        if el == None:  # can happen if the input (erroneously) contains trivial permutations
            break
        if wordy >= 2:
            print("    Next iteration: still to reduce:\n     ", todo)
            print("    Reducing for element", el)
        images = [None] * n
        todonext = []
        for P in todo:
            if P[el] == el:
                todonext.append(P)
            elif images[P[el]] == None:
                if wordy >= 2:
                    print("      Keeping", P, "which maps", el, "to", P[el])
                outputgenerators.append(P)
                images[P[el]] = P
            else:
                Q = -images[P[el]] * P
                if wordy >= 2:
                    print("      Changing", P, "to", Q)
                if not Q.istrivial():
                    todonext.append(Q)
        todo = todonext
    if wordy >= 1:
        print("  Output length:", len(outputgenerators))
    return outputgenerators


def Stabilizer(generators, el):
    """
	<generators> should be a python list containing permutations (from permv2.py),
	which is viewed as a generating set for a group H.
	<el> should be an element from 0...n-1 (the ground set for the permutations).
	
	This function returns a generating set for H_{el}, the stabilizer subgroup of H
	for element <el>. The generating set has size less than n^2.
	"""
    return Reduce(SchreierGenerators(generators, el), 0)
