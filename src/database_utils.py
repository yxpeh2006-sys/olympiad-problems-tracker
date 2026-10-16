from sqlalchemy import create_engine, text
import pandas as pd

connection_url = "sqlite:///olympiad.db"
engine = create_engine(connection_url)

def log_training_session(problems_list, demographic, training_type, session_date):
    session_query = text(
        """
        SELECT * FROM sessions
        WHERE demographic = :dm
          AND training_type = :tt
          AND session_date = :sd
        """
    )
    session_named_parameters = {
        'dm': str(demographic),
        'tt': str(training_type),
        'sd': str(session_date)
    }

    pd_session_match = pd.read_sql(session_query, con=engine, params=session_named_parameters)

    if pd_session_match.empty:
        new_session = pd.DataFrame([{
            'demographic': demographic,
            'training_type': training_type,
            'session_date': session_date
        }])
        new_session.to_sql('sessions', con=engine, if_exists='append', index=False)

        with engine.connect() as conn:
            session_id = conn.execute(text('SELECT last_insert_rowid()')).scalar()

    else:
        session_id = pd_session_match.iloc[0]['session_id']


    for problem in problems_list:
        if int(problem['year']) < 1900 or int(problem['year']) > 2100:
            print('Invalid Syntax')
            continue
        
        problem_query = text(
            """
            SELECT * FROM problems 
            WHERE country_code = :cc
              AND contest = :ct
              AND year = :yr
              AND problem_number = :pn
            """
        )
        problem_named_parameters = {
            'cc': str(problem['country_code']),
            'ct': str(problem['contest']),
            'yr': int(problem['year']),
            'pn': str(problem['problem_number'])
        }
        
        pd_problem_match = pd.read_sql(problem_query, con=engine, params=problem_named_parameters)

        if pd_problem_match.empty:
            new_problem = pd.DataFrame([problem])
            new_problem.to_sql('problems', con=engine, if_exists='append', index=False)

            with engine.connect() as conn:
                problem_id = conn.execute(text('SELECT last_insert_rowid()')).scalar()

        else:
            problem_id = pd_problem_match.iloc[0]['problem_id']

        problem_session_query = text(
            '''
            SELECT * FROM problem_session
            WHERE problem_id = :problem_id
              AND session_id = :session_id
            '''
        )

        problem_session_parameters = {
            'problem_id': int(problem_id),
            'session_id': int(session_id)
        }

        pd_problem_session_match = pd.read_sql(problem_session_query, con=engine, params=problem_session_parameters)

        if pd_problem_session_match.empty:
            new_problem_session = pd.DataFrame([problem_session_parameters])
            new_problem_session.to_sql('problem_session', con=engine, if_exists='append', index=False)


def get_problems(demographic, training_type, session_date):
    session_query = text(
        """
        SELECT * FROM sessions
        WHERE demographic = :dm
          AND training_type = :tt
          AND session_date = :sd
        """
    )
    session_named_parameters = {
        'dm': str(demographic),
        'tt': str(training_type),
        'sd': str(session_date)
    }

    pd_session_match = pd.read_sql(session_query, con=engine, params=session_named_parameters)

    if pd_session_match.empty:
        print('No such session')
        return None

    search_parameters = {'s_id': int(pd_session_match.iloc[0]['session_id'])}

    query = text(
        """
        SELECT * FROM problems
        WHERE problem_id IN (
            SELECT problem_id FROM problem_session
            WHERE session_id = :s_id
        )
        """
    )

    df_session_problems = pd.read_sql(query, con=engine, params=search_parameters)

    print(df_session_problems)
    return df_session_problems


def get_sessions(problem):
    problem_query = text(
        '''
        SELECT * FROM problems
        WHERE country_code = :cc
          AND contest = :ct
          AND year = :yr
          AND problem_number = :pn
        '''
    )
    problem_search_parameters = {
        'cc': str(problem['country_code']),
        'ct': str(problem['contest']),
        'yr': int(problem['year']),
        'pn': str(problem['problem_number'])
    }
    pd_problem_match = pd.read_sql(problem_query, con=engine, params=problem_search_parameters)

    if pd_problem_match.empty:
        print('No such problem')
        return None

    problem_id = pd_problem_match.iloc[0]['problem_id']

    session_query = text(
        '''
        SELECT * FROM sessions
        WHERE session_id IN (
            SELECT session_id FROM problem_session
            WHERE problem_id = :id
        )
        '''
    )
    session_search_parameters = {
        'id': int(problem_id)
    }
    pd_sessions_match = pd.read_sql(session_query, con=engine, params=session_search_parameters)
    
    print(pd_sessions_match)
    return pd_sessions_match


def get_all_problems():
    query = text('SELECT * FROM problems')
    df_problems = pd.read_sql(query, con=engine)
    print(df_problems)
    return df_problems


def get_all_sessions():
    query = text('SELECT * FROM sessions')
    df_sessions = pd.read_sql(query, con=engine)
    print(df_sessions)
    return df_sessions


def get_all_problem_session():
    query = text('SELECT * FROM problem_session')
    df_problem_session = pd.read_sql(query, con=engine)
    print(df_problem_session)
    return df_problem_session
