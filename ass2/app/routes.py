from flask import render_template,request
from app import app
import sqlite3
import base64

def get_car_data():
    connection = sqlite3.connect("table.sqlite")
    cursor = connection.cursor()

    # Fetch data from the 'VEHICLE' table
    cursor.execute("SELECT category, COUNT(*) as category_count FROM VEHICLE GROUP BY category;")
    category_data = cursor.fetchall()
    total_car_count = 0
    car_list_category_info=[]
    for row in category_data:
        category_value = row[0]
        category_count = row[1]     
        total_car_count= total_car_count + category_count

        category_list_dict = {
            'category_value' : category_value,
            'category_count' : category_count
        }
        car_list_category_info.append(category_list_dict)

    # Close the database connection
    connection.close()
    return car_list_category_info,total_car_count

def get_house_data():
    connection = sqlite3.connect("table.sqlite")
    cursor = connection.cursor()

    # Fetch data from the 'VEHICLE' table
    cursor.execute("SELECT category, COUNT(*) as category_count FROM HOUSE GROUP BY category;")
    category_data = cursor.fetchall()

    house_list_category_info = []
    total_house_count=0
    for row in category_data:
        category_value = row[0]
        category_count = row[1]
        total_house_count = total_house_count + category_count

        house_list_dict = {
            'category_value' : category_value,
            'category_count' : category_count
        }

        house_list_category_info.append(house_list_dict)

    return house_list_category_info,total_house_count

def get_lecturer_data():
    connection = sqlite3.connect("table.sqlite")
    cursor = connection.cursor()

    # Fetch data from the 'VEHICLE' table
    cursor.execute("SELECT category, COUNT(*) as category_count FROM LECTURER GROUP BY category;")
    category_data = cursor.fetchall()

    lecturer_list_category_info = []
    total_lecturer_count=0
    for row in category_data:
        lecture_name = row[0]
        lecturer_count = row[1]
        total_lecturer_count = total_lecturer_count + lecturer_count

        house_list_dict = {
            'lecture_name' : lecture_name,
            'lecturer_count' : lecturer_count
        }

        lecturer_list_category_info.append(house_list_dict)

    return lecturer_list_category_info,total_lecturer_count    

def get_all_data():
    connection = sqlite3.connect("table.sqlite")
    cursor = connection.cursor()

    # Fetch data from the 'VEHICLE' table
    cursor.execute("SELECT description,data FROM VEHICLE;")
    all_data = cursor.fetchall()

    cursor.execute("SELECT description, data FROM HOUSE;")
    house_data = cursor.fetchall()

    cursor.execute("SELECT description, data from LECTURER;")
    lecturer_data = cursor.fetchall()
    all_data = all_data + house_data + lecturer_data

    all_data_info=[]
    for row in all_data:
        description = row[0]
        image =  row[1]

        base64_image = base64.b64encode(image).decode('utf-8')
        # Ensure the correct MIME type based on your image format (e.g., image/jpeg)
        mime_type = 'image/jpeg'
        data_url = f'data:{mime_type};base64,{base64_image}'

        all_data_dict = {
            'description' : description,
            'image' : data_url
        }
        all_data_info.append(all_data_dict)

    # Close the database connection
    connection.close()

    return all_data_info

def get_data_by_attribute(attribute):
    connection = sqlite3.connect("table.sqlite")
    cursor = connection.cursor()

    # Fetch data from the 'VEHICLE' table
    vehicle_query = ('''
                    SELECT description,data
                    FROM VEHICLE
                    WHERE category LIKE ?
                    OR brand LIKE ?
                    OR model LIKE ?
                    OR city LIKE ?;
                   ''')
    cursor.execute(vehicle_query,('%' + attribute + '%', '%' + attribute + '%', '%' + attribute + '%','%' + attribute + '%'))

    vehicle_result = cursor.fetchall()

    house_query = ('''
                   SELECT description,data
                   FROM HOUSE
                   WHERE category LIKE ?
                   OR city LIKE ?;
                   ''')
    
    cursor.execute(house_query,('%' + attribute + '%', '%' + attribute + '%'))

    house_result = cursor.fetchall()

    lecturer_query = ('''
                      SELECT description,data
                      FROM LECTURER
                      WHERE category LIKE ?
                      OR city LIKE ?  
                      ''')
    cursor.execute(lecturer_query,('%' + attribute + '%', '%' + attribute + '%'))

    lecturer_result = cursor.fetchall()

    all_data = vehicle_result + house_result + lecturer_result

    data_given_attributes = []

    for row in all_data:
        description = row[0]
        image =  row[1]

        base64_image = base64.b64encode(image).decode('utf-8')
        # Ensure the correct MIME type based on your image format (e.g., image/jpeg)
        mime_type = 'image/jpeg'
        data_url = f'data:{mime_type};base64,{base64_image}'

        all_data_dict = {
            'description' : description,
            'image' : data_url
        }
        data_given_attributes.append(all_data_dict)

    # Close the database connection
    connection.close()
    return data_given_attributes
# If search_query is empty it means render template with all data
# Else look all tables, render template with all data with include search input
@app.route('/', methods=['GET'])
def homesql():
    search_query = request.args.get('search_query')

    car_list_category_info, total_car_count = get_car_data()
    house_list_category_info, total_house_count = get_house_data()
    lecturer_list_category_info , total_lecturer_count = get_lecturer_data()
    
    if search_query is None or len(search_query)==0:
        all_ads= get_all_data()
        return render_template('index.html', 
                           total_car_count=total_car_count,car_data=car_list_category_info,
                           total_house_count=total_house_count,house_data=house_list_category_info,
                           total_lecturer_count = total_lecturer_count, lecturer_data = lecturer_list_category_info,
                           all_data=all_ads)
    else:
        all_ads = get_data_by_attribute(search_query)
        return render_template('index.html', 
                           total_car_count=total_car_count,car_data=car_list_category_info,
                           total_house_count=total_house_count,house_data=house_list_category_info,
                           total_lecturer_count = total_lecturer_count, lecturer_data = lecturer_list_category_info,
                           all_data=all_ads)
    
@app.route('/detail')
def detail_ads():
    ad_title = request.args.get('title')
    # Since I have three different tables
    # First I should find which table responsible
    connection = sqlite3.connect("table.sqlite")
    cursor = connection.cursor()
    
    # Check VEHICLE table
    vehicle_query = ("SELECT * FROM VEHICLE WHERE description = ?;")
    house_query = ("SELECT * FROM HOUSE WHERE description = ?;")
    lecturer_query = ("SELECT * FROM LECTURER WHERE description = ?;")
    cursor.execute(vehicle_query, (ad_title,))

    vehicle_result = cursor.fetchone()
    # If it is not in VEHICLE table look for other tables
    if vehicle_result is None:
        # Check house table
        cursor.execute(house_query,(ad_title,))
        house_result = cursor.fetchone()
        if house_result is None:
            cursor.execute(lecturer_query,(ad_title,))
            lecturer_result = cursor.fetchone()

            image = lecturer_result[6]
            base64_image = base64.b64encode(image).decode('utf-8')
            # Ensure the correct MIME type based on your image format (image/jpeg)
            mime_type = 'image/jpeg'
            data_url = f'data:{mime_type};base64,{base64_image}'
            data = {
                'Ders' : lecturer_result[1],
                'İlan No' : lecturer_result[2],
                'Şehir' : lecturer_result[3],
                'Fiyat' : lecturer_result[4],
                'Açıklama' : lecturer_result[5],
            }
            return render_template('detail.html',detail_data = data,image=data_url)

        else:
            image = house_result[6]
            base64_image = base64.b64encode(image).decode('utf-8')
            mime_type = 'image/jpeg'
            data_url = f'data:{mime_type};base64,{base64_image}'
            data = {
                'Kategori' : house_result[1],
                'İlan No' : house_result[2],
                'Şehir' : house_result[3],
                'Fiyat' : house_result[4],
                'Açıklama' : house_result[5]
            }

            return render_template('detail.html',detail_data = data, image = data_url)

    else:
        image = vehicle_result[8]
        base64_image = base64.b64encode(image).decode('utf-8')
        mime_type = 'image/jpeg'
        data_url = f'data:{mime_type};base64,{base64_image}'
        data = {
            'Kategori' : vehicle_result[1],
            'İlan No' : vehicle_result[2],
            'Marka' : vehicle_result[3],
            'Model' : vehicle_result[4],
            'Şehir' : vehicle_result[5],
            'Fiyat' : vehicle_result[6],
            'Açıklama' : vehicle_result[7]
        }

    return render_template('detail.html', detail_data = data, image = data_url)
