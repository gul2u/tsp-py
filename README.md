# Commuting Engineer Challenge - Traveling Salesman Problem

A Python-based solution submitted to [CodeEval's Commuting Engineer Challenge](https://www.codeeval.com/open_challenges/90/).

Submission notes have been pulled from file and are provided below:

>Solution to Commuting Engineer Challenge(Traveling Salesman Problem) is based on the hill climbing principle for finding the best solution through stochastic optimization based on random initializations and solution sets/move operators(Sources 1 and 2).
>
>Source code was merged to a single file and modified to satisfy the conditions/constraints of the challenge.
>
>Further changes were inspired to be made to the construction of the distance matrix for objective scoring to utilize Google Maps API for actual distance/duration calculations based on street conditions instead of cartesian coordinates. distance_matrix method was optimized to fully take advantage of Google's Distance Matrix API(Source 4).
>
>Simulated Annealing was considered but discarded due to expected small sample size of 10 locations and lack of sufficient improvements from the publication(Source 3).
>
> Note: Final submission was adjusted to utilize default cartesian distance matrix due to urllib2:urlopen errors with code submissions.
>
> Sources:  1. [Tackling the Travelling Salesman Problem Part One](http://www.psychicorigami.com/2007/04/17/tackling-the-travelling-salesman-problem-part-one/)
>		 	2. [Hill Climbing](http://www.psychicorigami.com/2007/05/12/tackling-the-travelling-salesman-problem-hill-climbing/)
>		 	3. [Simulated Annealing](http://www.psychicorigami.com/2007/06/28/tackling-the-travelling-salesman-problem-simmulated-annealing/)
>		 	4. [https://github.com/mabounassif/traveling_salesman](https://github.com/mabounassif/traveling_salesman)

Socring of final submission was 100/100 thus passing all test cases for the challenge.

The Google distance calculations proved to be unnecessary for the challenge but are left intact for those that are curious. Included is a json response from the Google Distance Matrix API containing all 10 locations provided in the challenge description. For more information see [Google Distance Matrix](https://developers.google.com/maps/documentation/distancematrix/).

# Usage

Python 2.7.2 was used to execute the code:

```bash
$ python cec-tsp.py [FILENAME]
```
