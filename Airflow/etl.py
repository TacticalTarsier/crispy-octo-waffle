# %%
import pandahouse

from datetime import datetime, timedelta
import pandas as pd
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context

connection = {
    'host': 'https://clickhouse.lab.karpov.courses',
    'password': 'dpo_python_2020',
    'user': 'student',
    'database': 'simulator_20220620.feed_actions'}

default_args = {
    'owner': 'o.karnugaev',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2022, 7, 9)
}

schedule_interval = '0 8 * * *'


@dag(default_args=default_args, schedule_interval=schedule_interval, catchup=False)
def dag_sim():
    @task
    def extract_actions():
        actions_query = '''
        SELECT toDate(time) AS date,
               user_id,
               sum(CASE
                       WHEN action='view' THEN 1
                       ELSE 0
                   END) AS views,
               sum(CASE
                       WHEN action='like' THEN 1
                       ELSE 0
                   END) AS likes
        FROM simulator_20220620.feed_actions
        WHERE date = today() - 1
        GROUP BY date, user_id
        '''

        actions_df = pandahouse.read_clickhouse(actions_query, connection=connection)

        return actions_df

    @task
    def extract_messages():
        messages_query = '''
        SELECT date, user_id,
                     messages_sent,
                     messages_received,
                     users_sent,
                     users_received
        FROM
          (SELECT toDate(time) AS date,
                  user_id,
                  count(reciever_id) AS messages_sent,
                  uniqExact(reciever_id) AS users_sent
           FROM simulator_20220620.message_actions
           WHERE toDate(time) = today() - 1
           GROUP BY user_id, date) AS ma
        FULL OUTER JOIN
          (SELECT toDate(time) AS date,
                  reciever_id,
                  count(user_id) AS messages_received,
                  uniqExact(user_id) AS users_received
           FROM simulator_20220620.message_actions
           WHERE toDate(time) = today() - 1
           GROUP BY reciever_id, date) AS sub
           ON ma.user_id = sub.reciever_id AND ma.date = sub.date
            '''

        messages_df = pandahouse.read_clickhouse(messages_query, connection=connection)

        return messages_df

    @task
    def extract_unique_users():
        users_query = '''
        select distinct user_id,
        age,
        gender,
        os
        from simulator_20220620.feed_actions
        where toDate(time) = today() - 1
        union all
        select distinct user_id,
        age,
        gender,
        os
        from simulator_20220620.message_actions
        where toDate(time) = today() - 1
        '''

        users_df = pandahouse.read_clickhouse(users_query, connection=connection)
        return users_df

    @task
    def join_tables(users_df, actions_df, messages_df):
        result_df = pd.merge(users_df, actions_df, how='left', on='user_id')
        result_df = result_df.merge(messages_df, how='left', on=['user_id', 'date']).fillna(0)

        result_df = result_df.astype({'gender': 'int',
                                      'age': 'int',
                                      'views': 'int',
                                      'likes': 'int',
                                      'messages_sent': 'int',
                                      'messages_received': 'int',
                                      'users_sent': 'int',
                                      'users_received': 'int'})

        return result_df

    metrics_list = ['views', 'likes', 'messages_sent', 'messages_received', 'users_sent', 'users_received']

    @task
    def transform_gender_grouped(result_df, metrics_list=metrics_list):
        gender_grouped = result_df.groupby('gender', as_index=False)[metrics_list] \
            .sum()
        gender_grouped['gender'] = gender_grouped.gender.apply(lambda x: 'male' if x == 1 else 'female')
        gender_grouped.insert(0, 'slice', 'gender')
        gender_grouped = gender_grouped.rename(columns={'gender': 'sub_slice'})

        return gender_grouped

    @task
    def transform_os_grouped(result_df, metrics_list=metrics_list):
        os_grouped = result_df.groupby('os', as_index=False)[metrics_list] \
            .sum()
        os_grouped.insert(0, 'slice', 'os')
        os_grouped = os_grouped.rename(columns={'os': 'sub_slice'})

        return os_grouped

    @task
    def transform_age_grouped(result_df, metrics_list=metrics_list):
        result_df['age_group'] = pd.cut(result_df.age, bins=[0, 18, 25, 30, 40, 50, 70, 90],
                                        labels=[' age <18', 'age 18-25', 'age 25-30', 'age 31-40', 'age 41-50',
                                                'age 51-70', 'age 71-90'])
        age_grouped = result_df.groupby('age_group', as_index=False)[metrics_list].sum() \
            .rename(columns={'age_group': 'sub_slice'})
        age_grouped.insert(0, 'slice', 'age')

        return age_grouped

    @task
    def concat_tables(gender_grouped, os_grouped, age_grouped):
        concated_df = pd.concat([gender_grouped, os_grouped, age_grouped])
        concated_df.insert(0, 'date', result_df.date.loc[0])

        concated_df = concated_df.astype({'views': 'int',
                                          'likes': 'int',
                                          'messages_sent': 'int',
                                          'messages_received': 'int',
                                          'users_sent': 'int',
                                          'users_received': 'int'})

        return concated_table

    @task
    def load(concated_df):
        load_connection = {
            'host': 'https://clickhouse.lab.karpov.courses',
            'database': 'test',
            'password': '656e2b0c9c',
            'user': 'student-rw'}

        table_query = '''
                        CREATE TABLE IF NOT EXISTS test.test_karnugaev
                        (
                            date Date,
                            slice String,
                            sub_slice String,
                            views Int32,
                            likes Int32,
                            messages_sent Int32,
                            messages_received Int32,
                            users_sent Int32,
                            users_received Int32
                        )
                            ENGINE = Log()
                        '''

        pandahouse.execute(query=table_query, connection=load_connection)
        pandahouse.to_clickhouse(df=concated_df, table='test_karnugaev', index=False, connection=load_connection)

    actions_df = extract_actions()
    messages_df = extract_messages()
    users_df = extract_unique_users()

    result_df = join_tables(users_df, actions_df, messages_df)

    gender_grouped = transform_gender_grouped(result_df)
    os_grouped = transform_os_grouped(result_df)
    age_grouped = transform_age_grouped(result_df)

    concated_df = concat_tables(gender_grouped, os_grouped, age_grouped)


    load(concated_df)


dag_sim = dag_sim()

# %%
