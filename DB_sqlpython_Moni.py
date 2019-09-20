#######################################
#######################################
####### Python <3 Mysql
#######################################
#######################################
# Comandos utiles y basicos en python para conectarse con Mysql


#######################################
import mysql.connector
#######################################
# conda install -c anaconda mysql-connector-python
# pip install mysql-connector-python

#######################################
# Establecer la concexion
#######################################
mydb = mysql.connector.connect(
  host="localhost",
  user="mpadilla",
  passwd="genoma123",
  port = '3306'
  #database = "TraitsQTLs_Genetica"
)

mycursor = mydb.cursor()

#######################################
# metodo execute para ejecutar acciones dentro de mysql
#######################################
mycursor.execute("CREATE DATABASE TraitsQTLs_Genetica")

mydb = mysql.connector.connect(
  host="localhost",
  user="mpadilla",
  passwd="genoma123",
  port = '3306',
  database = "TraitsQTLs_Genetica"
)

mycursor = mydb.cursor()
#######################################
#Mostrar bases de datos
#######################################
mycursor.execute("SHOW DATABASES")
#Imprimi
for x in mycursor:
  print(x)

mycursor.execute("USE TraitsQTLs_Genetica")
#######################################
# Crear una tabla
#######################################
mycursor.execute("CREATE TABLE DatosGenerales (persona_id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), sexo CHAR(1), edad INT(2), estado VARCHAR(255))")
mycursor.execute("CREATE TABLE Mediciones (medicion_id INT AUTO_INCREMENT PRIMARY KEY, tipo varchar(255), medida FLOAT, persona_id INT, CONSTRAINT persona_fk FOREIGN KEY (persona_id) REFERENCES DatosGenerales(persona_id))")
#######################################
#Mostrar las tablas
#######################################
mycursor.execute("SHOW TABLES")

#Imprimir
for x in mycursor:
  print(x)

#######################################
# Popular la tabla
#######################################
# formato sql
sql = "INSERT INTO DatosGenerales (nombre, sexo, edad, estado) VALUES (%s, %s, %s, %s)"
# variable para incresar en mysql
val = ("Mario Santana", "M", "35", "CDMX")
val
mycursor.execute(sql, val)

#######################################
# Super importante hacer COMMIT!!!!!!!!
#######################################
#Importate hacer commit
mydb.commit()

#######################################
# Contar cuantos commit se hicieron con rowcount
#######################################
print(mycursor.rowcount, "record inserted.")

#######################################
# Popular la tabla con más de un valor
#######################################
# formato sql
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# variables
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]

mycursor.executemany(sql, val)

#Hacer commit
mydb.commit()

#######################################
# Popular la tabla desde archivos .csv
#######################################
import pandas as pd
# leer el archivo
data = pd.read_csv('MedicionesQTLs_Geneticacsv') # header, names

fields= []
# para cada linea insertar en Mysql
sql = "INSERT INTO DatosGenerales (nombre, sexo, edad, estado) VALUES (%s, %s, %s, %s)"
for row in data.iterrows():
    fields = list(row[1])
    print(row[0])
    val = fields[0:4]
    #mycursor.execute(sql, val)

mydb.commit()

vals, i = [], 1;
for row in data.iterrows():
    sql = "INSERT INTO Mediciones (tipo, medida, persona_id) VALUES (%s, %s, %s)"
    campos = list(row[1])
    vals = [("altura", campos[5], i), ("pigm_fr_avg", campos[11], i), ("pigm_br_avg", campos[17], i),
        ("calzado", campos[18], i), ("ps_sis", campos[19], i), ("ps_dia", campos[20], i)]
    pigm_fr = campos[6:11]
    for c in pigm_fr:
        vals.append(["pigm_fr",c,i])
    pigm_br = campos[12:17]
    for c in pigm_br:
        vals.append(["pigm_br",c,i])
    #print(vals)
    i=i+1
    mycursor.executemany(sql, vals)

mycursor.execute("select * from Mediciones")
for x in mycursor:
    print(x)

#######################################
# Usando sqlalchemy
#######################################
# pip install SQLAlchemy
# conda install -c anaconda sqlalchemy
import sqlalchemy

# conexion para sqlalchemy
# mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:root@localhost[8889]/')

# leer el csv
data = pd.csv('file.txt') # checar nombres de columnas igual a la tabla en MySQL
# inserar en la tabla
data.to_sql('customers', con = engine)
#######################################


#######################################
# Ingresar la tabla directo a MySQL
#######################################
## SQL
#LOAD DATA LOCAL INFILE '/file.csv'
#INTO TABLE customers
#FIELDS TERMINATED BY ','
#LINES TERMINATED BY '\n'
#IGNORE 1 ROWS # header
#(name,address)
#;
sql = "LOAD DATA LOCAL INFILE 'file.csv' \
INTO TABLE customers \
FIELDS TERMINATED BY ',' \
LINES TERMINATED BY '\n' \
IGNORE 1 ROWS # header\
(name,address)"

mycursor.execute(sql)


#######################################
# regresar valores
#######################################
#Para regresar los valores
mycursor.execute("SELECT * FROM customers")

#Guardar los valores
myresult = mycursor.fetchall()

for x in myresult:
  print(x)



### Usando sqlalchemy
# Para leer tablas
df = pd.read_sql_table('customers',engine) # mydb ?
# se le puede pasar queries
df = pd.read_sql_query("select name from customers",engine)
