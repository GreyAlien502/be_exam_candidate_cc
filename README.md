# SCOIR Technical Interview for Back-End Engineers
This repo contains an exercise intended for Back-End Engineers.

## Instructions
1. Fork this repo.
1. Using technology of your choice, complete [the assignment](./Assignment.md).
1. Update this README with
    * a `How-To` section containing any instructions needed to execute your program.
    * an `Assumptions` section containing documentation on any assumptions made while interpreting the requirements.
1. Before the deadline, submit a pull request with your solution.

## Expectations
1. Please take no more than 8 hours to work on this exercise. Complete as much as possible and then submit your solution.
1. This exercise is meant to showcase how you work. With consideration to the time limit, do your best to treat it like a production system.

## How-To
1. Install watchdog with `pip install watchdog`.
1. Go to the `recordProcessor` directory and run `python fileWatcher.py <input directory> <output directory> <error directory>`.

## Assumptions
1. `MIDDLE_NAME` column can be omitted from csv file, in which case all records will lack a `MIDDLE_NAME`.
1. Extra columns can be included in the csv file, in which case they will be ignored.
1. If any column is missing, one error will be reported for the whole file.
1. Empty files will not be written.
