import sqlite3
import streamlit as st
import pandas as pd
from style import apply_style
apply_style('School Library')
conn = sqlite3.connect('library.db')
cur = conn.cursor()
cur.execute('select count(*) from books')
total_books = cur.fetchone()[0]
cur.execute('select count(*) from students')
total_students = cur.fetchone()[0]
cur.execute('select count(*) from checkouts where return_date is null')
books_out = cur.fetchone()[0]
cur.execute("select count(*) from checkouts where issue_date >= date('now', '-7 days')")
this_week = cur.fetchone()[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric('Books', total_books)
c2.metric('Students', total_students)
c3.metric('Books out now', books_out)
c4.metric('Issued this week', this_week)
st.write('Choose a page from the menu on the left.')
st.subheader('Books issued per day (last 30 days)')
daily = pd.read_sql('''SELECT issue_date, COUNT(*) AS issued
                       FROM checkouts
                       WHERE issue_date >= date('now', '-30 days')
                       GROUP BY issue_date
                       ORDER BY issue_date''', conn)

st.line_chart(daily.set_index('issue_date')['issued'], color='#1B2A41')
st.subheader('Borrowing by genre (all time)')
genres = pd.read_sql('''SELECT books.genre, COUNT(*) AS borrowed
                        FROM checkouts
                        JOIN books ON books.book_id = checkouts.book_id
                        GROUP BY books.genre
                        ORDER BY borrowed DESC''', conn)
st.bar_chart(genres.set_index('genre')['borrowed'], color='#1B2A41')
