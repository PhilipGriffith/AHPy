# AHPy

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
