from database_utils import log_training_session, get_problems
import csv

with open('logs/problems.csv', mode='r') as file:
    reader = csv.DictReader(file)
    problems_list = list(reader)

with open('logs/session.csv', mode='r') as file:
    reader = csv.DictReader(file)
    session = list(reader)[0]

log_training_session(problems_list, **session)
get_problems(**session)
