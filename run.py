#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Modified by Alchan Kim at SNU Software Platform Lab for
# SWPP fall 2020 lecture

import sys
import os

from babyname_parser import BabynameParser


class BabyRecord:
    def __init__(self, year, rank, name, gender, rank_change=None):
        self.year = year
        self.rank = rank
        self.name = name
        self.gender = gender
        self.rank_change = rank_change
    
    def to_csv_record(self):
        res=""
        res=repr(self.year)+','+repr(self.rank)+','+self.name+','+self.gender
        if self.rank_change !=None : 
            res+=','
            res+=repr(self.rank_change)
        return res
        # TODO: Implment this function


    def __repr__(self):
        """
        NOTE: This method is provided for debugging. You don't need to modify this.
        """
        return "<BabyRecord year={} rank={} name={} gender={} rank_change={}>".format(
            self.year,
            self.rank,
            self.name,
            self.gender,
            self.rank_change,
        )

def save(filename, records):
    """
    NOTE: DO NOT change this function.
    This function saves the parsed records in csv format.

    Args:
        filename: The name of the output file.
        records: The list of records.
    """
    with open(filename, "w") as f:
        f.write("year,rank,name,gender,rank_change\n")
        for record in records:
            f.write(record.to_csv_record())
            f.write("\n")


def main():
    """
    (5 points)
    """
    
    args = sys.argv[1:]
    
    if len(args) < 2:
        print('usage: python run.py `starting year` `ending year`')
        sys.exit(1)
    
    year1, year2 = int(args[0]), int(args[1])
    records = [] # list of BabyRecord objects
    prev_male_ranking = {} # use this to calculate the rank if you need
    prev_female_ranking = {}
    for year in range(year1, year2 + 1):
        parser = BabynameParser("babydata", year)
        # TODO: In the following two lines, change `None` to your lambda function to parse baby name records.
        # By using the lambda function, `parse` method should return a list of `BabyRecord` objects
        # that contain year, rank, name, and gender data.
        male_records = parser.parse(lambda baby_tuple: baby_tuple[1]) # Parse the male ranks and store them as a list of `BabyRecord` objects.
        for i in range(len(male_records)):
            
            if male_records[i] in prev_male_ranking :
             bb=BabyRecord(parser.year,i,male_records[i],'M',i-prev_male_ranking[male_records[i]])
            else :
             bb=BabyRecord(parser.year,i,male_records[i],'M')    
            records.append(bb)        
        prev_male_ranking={}
        for i in range(len(male_records)):
            prev_male_ranking[male_records[i]]=i
        
        female_records = parser.parse(lambda baby_tuple: baby_tuple[2]) # Parse the female ranks and store it as a list of `BabyRecord` objects.
        for i in range(len(female_records)):
            if female_records[i] in prev_female_ranking :
             bb=BabyRecord(parser.year,i,female_records[i],'F',i-prev_female_ranking[female_records[i]])
            else :
             bb=BabyRecord(parser.year,i,female_records[i],'F')    
            records.append(bb)        
        prev_female_ranking={}
        for i in range(len(female_records)):
            prev_female_ranking[female_records[i]]=i

        # TODO: Calculate the rank change for each of `male_records` and `female_records`.
        # For example, if the rank of the previous year is 8 and the rank of the current year is 5,
        # -3 is the rank change. (Beware the sign of the value. Rank-up is respresented with a negative value!)
        # If the rank of previous year is not available, set `rank_change` to `None`.

    # TODO: Save the result as a csv file named `babyname.report.csv` under `babydata/` directory.
    # To verify correctness, try running this function using the html files we provided in the swppfall2020 repository
    # and compare the content of the babyname.report.csv.
    # Due to the inconsistency of the ranking information provided by ssa.gov, your output and the provided example output may differ
    # See issue #12 for more info
    save(os.path.join("babydata", "babyname.report.csv"), records)

if __name__ == '__main__':
    main()
