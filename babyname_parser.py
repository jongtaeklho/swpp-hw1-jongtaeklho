#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Modified by Alchan Kim at SNU Software Platform Lab for
# SWPP fall 2020 lecture.

import sys
import re
import os

from functools import wraps

"""Baby Names exercise

Implement the babyname parser class that parses the popular names and their ranks from a html file.

1) At first, you need to implement a decorator that checks whether the html file exists or not.
2) Also, the parser should extract tuples of (rank, male-name, female-name) from the file by using regex. 
   For writing regex, it's nice to include a copy of the target text for inspiration.
3) Finally, you need to implement `parse` method in `BabynameParser` class that parses the extracted tuples
   with the given lambda and return a list of processed results.
"""


class BabynameFileNotFoundException(Exception):
    """
    A custom exception for the cases that the babyname file does not exist.
    """
    pass



def check_filename_existence(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except FileNotFoundError as pathname :
            raise BabynameFileNotFoundException("No such file: {}".format(pathname.filename))
    return wrapper

    """
    (1 point)
    A decorator that catches the non-exiting filename argument and raises a custom `BabynameFileNotFoundException`.

    Args:
        func: The function to decorate.
    Raises:
    BabynameFileNotFoundException: if there is no such file while func tries to open a file.
                                        We assume func receives directory path and year to generate a filename to open.
    """
    # TODO: Implement this decorator


class BabynameParser:

    @check_filename_existence
    def __init__(self, dirname, year):
        """
        (3 points)
        Given directory path and year, extracts the name of a file to open the corresponding file
        and a list of the (rank, male-name, female-name) tuples from the file read by using regex.
        [('1', 'Michael', 'Jessica'), ('2', 'Christopher', 'Ashley'), ....]

        Args:
            dirname: The name of the directory where baby name html files are stored
            year: The year number. int.
        """
        pathname = os.path.join(dirname, "{}.html".format(year))
        f=open(pathname,'r')
        text=f.read()
        self.year=year
        regex=re.compile("<td>\w{1,60}</td>")
        res=regex.findall(text)
        
        mylist=[(res[0][4:-5],res[1][4:-5],res[2][4:-5])]
        i=3
        while i <= (len(res)-3):
            firs=res[i][4:-5]
            secon=res[i+1][4:-5]
            thir=res[i+2][4:-5]
            mylist.append((firs,secon,thir))
            i+=3
        self.rank_to_names_tuples = mylist

    def parse(self, parsing_lambda):
        answer=[]
        for i in self.rank_to_names_tuples :
            answer.append(parsing_lambda(i))
        return answer
        """
        (2 points)
        Collects a list of babynames parsed from the (rank, male-name, female-name) tuples.
        The list must contains all results processed with the given lambda.

        Args:
            parsing_lambda: The parsing lambda.
                            It must process an single (string, string, string) tuple and return something.
        Returns:
            A list of lambda function's output
        """
        # TODO: Implement this method

