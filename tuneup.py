#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "perrymw...with assistance from Peter"

import cProfile
import pstats
from functools import wraps
import timeit
import collections


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    # You need to understand how decorators are constructed and used.
    # Be sure to review the lesson material on decorators, they are used
    # extensively in Django and Flask.
    @wraps(func)
    def decorator(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        ps = pstats.Stats(profiler).strip_dirs().sort_stats('cumulative')
        ps.print_stats()
        return result
    return decorator

    # raise NotImplementedError("Complete this decorator function")


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """returns True if title is within movies list"""
    return title in movies

@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates


@profile
def find_dup_moov(src):
    movies = [movie.lower() for movie in read_movies(src)]
    return [item for item, count in collections.Counter(movies).items() if count > 1]
    # dupes = [movie for movie in movies if is_duplicate(movie.lower(), movies)]
    # return dupes

def timeit_helper():
    """Part A:  Obtain some profiling measurements using timeit"""
    t = timeit.Timer(
        stmt="find_duplicate_movies('movies.txt')",
        setup='from __main__ import find_duplicate_movies'
        )
    number_of_repeats = 7
    number_of_times = 5
    result = t.repeat(
        repeat=number_of_repeats,
        number=number_of_times
        )
    le_final = (min(result) / float(number_of_times))
    print("Best time across {} repeats of {} runs per repeat: {} sec".format(number_of_repeats, number_of_times,  le_final))


def main():
    """Computes a list of duplicate movie entries"""
    result = find_dup_moov('movies.txt')
    # result = find_duplicate_movies("movies.txt")
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result).title())
    # timeit_helper()


if __name__ == '__main__':
    main()
