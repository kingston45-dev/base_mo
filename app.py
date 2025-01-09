from flask import Flask, render_template, request, redirect, url_for, flash, Response
import psycopg2
import psycopg2.extras
import io
import xlwt

import base64
 
app = Flask(__name__)
app.secret_key = "NMIC"
 
DB_HOST = "localhost"
DB_NAME = "YOUR_DB_NAME"
DB_USER = "YOUR_USERNAME"
DB_PASS = "YOUR_PASSWORD"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM public.mo"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)

@app.route('/download/report/excel')
def download_report():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM public.mo"
    cur.execute(s)
    result = cur.fetchall()
    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sh = workbook.add_sheet('МО')
 
    sh.write(0, 0, 'ID субъекта')
    sh.write(0, 1, 'Медицинская организация')
    sh.write(0, 2, 'Якорность МО')
    sh.write(0, 3, 'Год')
 
    idx = 0
    for row in result:
        sh.write(idx+1, 0, str(row['id_subject']))
        sh.write(idx+1, 1, row['mo_name'])
        sh.write(idx+1, 2, row['anchoring'])
        sh.write(idx+1, 3, row['year'])
        idx += 1
 
    workbook.save(output)
    output.seek(0)
 
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=MO.xls"})
 
@app.route('/add_MO', methods=['POST'])
def add_MO():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        id_subject = request.form['id_subject']
        mo_name = request.form['mo_name']
        anchoring = request.form['anchoring']
        year = request.form['year']
        cur.execute("INSERT INTO mo (id_subject, mo_name, anchoring, year) VALUES (%s,%s,%s,%s)", (id_subject, mo_name, anchoring, year))
        conn.commit()
        flash('MO успешно добавлена')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id_subject>', methods = ['POST', 'GET'])
def get_MO(id_subject):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM mo WHERE id_subject = %s', (id_subject,))
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', mo = data[0])
 
@app.route('/update/<id_subject>', methods=['POST'])
def update_MO(id_subject):
    if request.method == 'POST':
        mo_name = request.form['mo_name']
        anchoring = request.form['anchoring']
        year = request.form['year']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE mo
            SET mo_name = %s,
                anchoring = %s,
                year = %s
            WHERE id_subject = %s
        """, (mo_name, anchoring, year, id_subject))
        flash('Данные по МО успешно обновлены')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id_subject>', methods = ['POST','GET'])
def delete_MO(id_subject):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM mo WHERE ID_subject = {0}'.format(id_subject))
    conn.commit()
    flash('MO успешно удалена')
    return redirect(url_for('Index'))

@app.route('/statInfo/')
def statInfo():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM public.stat_info')
    stat_inf = cur.fetchall()
    return render_template('stat.html', stat_inf = stat_inf)

@app.route('/statinfo/<int:id_subject>', methods=['GET'])
def statinfo(id_subject):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM public.stat_info WHERE id_subject = %s', (id_subject,))
    st = cur.fetchall()
    return render_template('stat.html', st = st)

@app.route('/mapstat/<int:id_subject>', methods=['GET'])
def mapstat(id_subject):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT id_subject, map_stat FROM public.maps_stat WHERE id_subject = %s', (id_subject,))
    maps_stat_data = cur.fetchall()
    for row in maps_stat_data:
        if row['map_stat']:
            row['map_stat'] = base64.b64encode(row['map_stat']).decode('utf-8')
    return render_template('mapstat.html', maps_stat_data = maps_stat_data)

@app.route('/download/report_stat/excel')
def download_report_stat():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM public.stat_info"
    cur.execute(s)
    result = cur.fetchall()
    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sh = workbook.add_sheet('Статистическая информация')
 
    sh.write(0, 0, 'Код региона')
    sh.write(0, 1, 'Субъект РФ')
    sh.write(0, 2, 'Год')
    sh.write(0, 3, 'Население')
    sh.write(0, 4, 'Взрослое население')
    sh.write(0, 5, 'Городское население')
    sh.write(0, 6, 'Сельское население')
    sh.write(0, 7, 'Макс. удаленность до ближайшей МО')

    idx = 0
    for row in result:
        sh.write(idx+1, 0, str(row['id_subject']))
        sh.write(idx+1, 1, row['subject_rf'])
        sh.write(idx+1, 2, row['year'])
        sh.write(idx+1, 3, row['population_all'])
        sh.write(idx+1, 4, row['population_adult'])
        sh.write(idx+1, 5, row['population_city'])
        sh.write(idx+1, 6, row['population_country'])
        sh.write(idx+1, 7, row['max_distance'])
        
        idx += 1
 
    workbook.save(output)
    output.seek(0)
 
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=statinf.xls"})

@app.route('/edit_stat/<id_subject>', methods = ['POST', 'GET'])
def get_stat(id_subject):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM stat_info WHERE id_subject = %s', (id_subject,))
    data_stat = cur.fetchall()
    cur.close()
    return render_template('edit_stat.html', stats = data_stat)

@app.route('/update_stat/<id_subject>/<year>', methods=['POST'])
def update_stat(id_subject, year):
    if request.method == 'POST':
        population_all = request.form['population_all']
        population_adult = request.form['population_adult']
        population_city = request.form['population_city']
        population_country = request.form['population_country']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE stat_info
            SET population_all = %s,
                population_adult = %s,
                population_city = %s,
                population_country = %s
            WHERE id_subject = %s AND year = %s
        """, (population_all, population_adult, population_city, population_country, id_subject, year))
        flash('Данные по статистической информации успешно обновлены')
        conn.commit()
        return redirect(url_for('statInfo'))

@app.route('/delete_stat/<string:id_subject>', methods = ['POST','GET'])
def delete_stat(id_subject):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM stat_info WHERE ID_subject = {0}'.format(id_subject))
    conn.commit()
    flash('Пункт успешно удален')
    return redirect(url_for('statInfo'))

@app.route('/list_mo')
def list_mo():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT id_fo, subject_RF, mo FROM public.list_mo"
    cur.execute(s)
    result = cur.fetchall()
    return render_template('list_mo.html', result = result)

@app.route('/listmo/<int:id_fo>', methods=['GET'])
def listmo(id_fo):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM public.list_mo WHERE id_fo = %s', (id_fo,))
    result_fo = cur.fetchall()
    return render_template('list_mo_fo.html', result_fo = result_fo)

if __name__ == "__main__":
    app.run(debug=True)
