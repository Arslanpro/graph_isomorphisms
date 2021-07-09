# Graph Isomorphisms - Team 47
This is the final code for the Graph Isomorphism Project.

## Team

| S-Number | Name               |
|----------|--------------------|
| s2325993 | Fabian van Zetten  |
| s2362023 | Serge Johanns      |
| s2198312 | Wenjie Zhao        |
| s2267810 | Tom Meulenkamp     |

## Instructions
### Delivery Files
In order to run the final instances (`*Aut*`, `*GI*` and `*GIAut*`). One need to make sure that the directory `/graphs/delivery`
contains the necessary graph files. The main program is called `delivery.py`.

The program is able to recognize the files and will automatically decide what to calculate (equivalence classes
and/or automorphisms). Once the program has started it will prompt you to give in a filename. This filename should
correspond to one of the filenames in the `/graphs/delivery` directory.

### Example Graphs
In order to run the example graph files, such as `colorref_largeexample_4_1026.grl` one needs to choose a corresponding
week. Weeks are related to the treated subjects, in order of the project instruction lectures. 

| File Name                 | Subject                                   |
|---------------------------|-------------------------------------------|
| color_refinement.py       | Color Refinement                          |
| branching.py              | Branching                                 |
| fast_color_refinement.py  | Fast Color Refinement (DFA Minimization)  |
| auto_morphisms.py         | Auto Morphisms (Generating Sets)          |

To be more specific, the programs `color_refinement.py` and `fast_color_refinement.py` make use of the example graphs 
located in the `graphs/color refinement` directory. For the programs `branching.py` and `auto_morphisms.py` the graphs 
are located in the `graphs/branching` directory.

## Tests
All tests make use of the unittest library from Python.
For most programs there is also a testing class present, each testing file ends with `_test`. Some tests are more extensive
than others. The color refinement tests runs each instance in the `graphs/color refinement` directory, but doesn't check
for accurateness. The branching test is fully automated and checks the produced answers, due to time limitations, it only
checks all graphs with less then 2000 isomorphisms. Finally the automorphisms test contains two tests: one for membership
testing and one for order computations. 