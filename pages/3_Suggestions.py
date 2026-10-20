import sqlite3
import pandas as pd
import streamlit as st

st.title('BOOK SUGGESTIONS')
conn = sqlite3.connect('library.db')

students = pd.read_sql('select student_id, name from students order by name', conn)
students['label'] = students['student_id'] + ' - ' + students['name']
dicts = dict(zip(students['label'], students['student_id']))

choice = st.selectbox('Student', list(dicts))
sid = dicts[choice]

cur = conn.cursor()
cur.execute('select count(*) from checkouts where student_id=?', (sid,))
n = cur.fetchone()[0]

if n == 0:
    st.info('New reader: showing books from the most popular genre')

query = """
SELECT book_id, title, author, genre
FROM books
WHERE genre = COALESCE(
        (SELECT books.genre
         FROM checkouts
         JOIN books ON books.book_id = checkouts.book_id
         WHERE checkouts.student_id = ?
         GROUP BY books.genre
         ORDER BY COUNT(*) DESC
         LIMIT 1),
        (SELECT books.genre
         FROM checkouts
         JOIN books ON books.book_id = checkouts.book_id
         GROUP BY books.genre
         ORDER BY COUNT(*) DESC
         LIMIT 1)
      )
  AND book_id NOT IN (SELECT book_id FROM checkouts WHERE student_id = ?)
  AND book_id NOT IN (SELECT book_id FROM checkouts WHERE return_date IS NULL)
ORDER BY title
LIMIT 5
"""

result = pd.read_sql(query, conn, params=(sid, sid))

st.subheader('Suggested books')
if result.empty:
    st.warning('No suggestions available')
else:
    st.dataframe(result, hide_index=True)
