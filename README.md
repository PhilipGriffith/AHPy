# AHPy
*AHPy* is an implementation of the Analytical Hierarchy Process (AHP)
how to link in a hierarchy
names
order
complete()

how comparisons work
permutations
(a, b): 2 implies a over (?) b by 2
normalizing by values
missing values
link to paper
Optimally completes an incomplete pairwise comparison matrix according to the cyclic coordinates algorithm described in
        Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,'
        Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333. (https://doi.org/10.1016/j.mcm.2010.02.047)
        

precision
target differs from node's local/global

Random indices
Sets the 'consistency_ratio' property of the Compare object, using random index estimates from
        Donegan and Dodd's 'A note on Saaty's Random Indexes' in Mathematical and Computer Modelling,
        15:10, 1991, pp. 135-137 (doi: 10.1016/0895-7177(91)90098-R) by default (random_index='dd').
        If the random index of the object equals 'saaty', uses the estimates from
        Saaty's Theory And Applications Of The Analytic Network Process, Pittsburgh: RWS Publications, 2005, p. 31.
        
link to paper
when to use saaty

iterations

tolerance

cr override
saaty <= 15
dd <= 100

add_children()

report()
structure
json
name
weight
weights: local, global, target
cr
ri
elements: count, names
children: count, names
comparisons: input, computed

checks for values over 0 and that all values are numeric

After sitting on the back burner for too long, I'm picking up this code again.
I was pleasantly surprised when I was asked to include a license with the repository;
I was genuinely shocked to see that it has been forked multiple times!

- [x] My immediate goal is to update everything to Python 3.7.
- [ ] Next, I intend to create some test classes, as I remember that it was becoming more and more difficult to
make changes and also be sure that I hadn't broken the code elsewhere.
- [ ] Third, I'd like to do some refactoring of the code, especially separating out the checks for the matrices
into separate sections.
- [ ] Fourth, I'd like to revisit how the various objects interrelate and see if it can be done any better.
In particular, I'm wondering whether building the hierarchy using a context manager (in the style of PyMC3)
would be more user-friendly. Regardless, I still believe the flexibility of the current approach works well when integrating
the code into a larger decision-support system, which is my main use case.
