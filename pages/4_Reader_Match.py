import sqlite3
import pandas as pd
import streamlit as st

st.title('READER MATCH')
conn = sqlite3.connect('library.db')

students = pd.read_sql('select student_id, name from students order by name', conn)
students['label'] = students['student_id'] + ' - ' + students['name']
dicts = dict(zip(students['label'], students['student_id']))

choice = st.selectbox('Student', list(dicts))
sid = dicts[choice]

query = """
WITH counts AS (
    SELECT student_id, COUNT(DISTINCT book_id) AS n
    FROM checkouts
    GROUP BY student_id
),
shared AS (
    SELECT c2.student_id AS other, COUNT(DISTINCT c2.book_id) AS common
    FROM checkouts AS c1
    JOIN checkouts AS c2
      ON c1.book_id = c2.book_id AND c2.student_id != c1.student_id
    WHERE c1.student_id = ?
    GROUP BY c2.student_id
)
SELECT students.name, students.class,
       shared.common,
       ROUND(1.0 * shared.common /
             ((SELECT n FROM counts WHERE student_id = ?) + counts.n - shared.common), 2) AS similarity
FROM shared
JOIN counts ON counts.student_id = shared.other
JOIN students ON students.student_id = shared.other
ORDER BY similarity DESC
LIMIT 3
"""

result = pd.read_sql(query, conn, params=(sid, sid))

st.subheader('Closest readers')
if result.empty:
    st.info('No matches yet. This student needs more checkouts.')
else:
    result['reader'] = result['name'] + ' (Class ' + result['class'].astype(str) + ')'
    result['match'] = (result['similarity'] * 100).round(0).astype(int).astype(str) + '%'
    st.dataframe(result[['reader', 'common', 'match']].rename(columns={'common': 'books in common'}), hide_index=True)
