import pandas as pd
import sqlite3
import streamlit as st
st.title('Library Reports')
periods={'Last 7 days':7,'Last 30 days':30,'Last 90 days':90}
parameters = {'Title': 'books.title', 'Author': 'books.author', 'Genre': 'books.genre'}
c1=st.selectbox('choose a period',list(periods))
c2=st.selectbox('choose the parameter',list(parameters))
p=parameters[c2]
days=periods[c1]
conn=sqlite3.connect('library.db')
cur=conn.cursor()
query = f"""
SELECT * FROM (
    SELECT {p} as name,
           COUNT(*) AS times_borrowed,
           DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS position
    FROM checkouts
    JOIN books ON books.book_id = checkouts.book_id
    WHERE checkouts.issue_date >= date('now',?)
    GROUP BY {p}
)
WHERE position <= 3
ORDER BY position, name
"""
v = "-" + str(days) + " days"
#cur.execute(query,(value,))
result = pd.read_sql(query, conn , params=(v,))
st.subheader(f"Top {c2}s")
st.dataframe(result, hide_index=True)
st.subheader(f"Top {c2}s")
st.dataframe(result, hide_index=True)
st.bar_chart(result.set_index('name')['times_borrowed'], color='#1B2A41')

