import sqlite3
import pandas as pd
import streamlit as st
from datetime import date
st.title('ISSUE A BOOK')
conn=sqlite3.connect('library.db')
students=pd.read_sql('select student_id,name,class from students order by name',conn)
books=pd.read_sql('''SELECT book_id, title FROM books WHERE book_id NOT IN (SELECT book_id FROM checkouts
                    WHERE return_date IS NULL)ORDER BY title;''',conn)
students['lables']=students['name']+'-'+students['student_id']
dicts=dict(zip(students['lables'],students['student_id']))
dictb=dict(zip(books['title'],books['book_id']))
with st.form('issue form'):
    sl=st.selectbox('student',list(dicts))
    bt=st.selectbox('book',list(dictb))
    issue_date=st.date_input('Issue date',date.today())
    sumitted=st.form_submit_button('Issue book')
if sumitted:
    sid=dicts[sl]
    bid=int(dictb[bt])
    cur=conn.cursor()
    cur.execute('insert into checkouts(book_id,student_id,issue_date)values(?,?,?)',(bid,sid,issue_date.isoformat()))
    conn.commit()
    st.success(f"Issued '{bt}' to {sl} on {issue_date.isoformat()}")
st.header('RETURN A BOOK')

out = pd.read_sql('''SELECT checkouts.rowid AS id, books.title, checkouts.student_id, students.name
                     FROM checkouts
                     JOIN books ON books.book_id = checkouts.book_id
                     JOIN students ON students.student_id = checkouts.student_id
                     WHERE checkouts.return_date IS NULL
                     ORDER BY books.title''', conn)

if out.empty:
    st.info('No books are currently issued')
else:
    out['label'] = out['title'] + ' - ' + out['student_id'] + ' ' + out['name']
    dictr = dict(zip(out['label'], out['id']))

    with st.form('return_form'):
        rl = st.selectbox('Book being returned', list(dictr))
        return_date = st.date_input('Return date', date.today())
        returned = st.form_submit_button('Return book')

    if returned:
        rid = int(dictr[rl])
        cur = conn.cursor()
        cur.execute('update checkouts set return_date=? where rowid=?', (return_date.isoformat(), rid))
        conn.commit()
        st.success(f"Returned: {rl}")
