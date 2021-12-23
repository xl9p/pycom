import mysql.connector

# Establishing connection to Sql base


class DataBase:
    def getConnection(Host, User, Password="", Database = "telemetry"):
        connection = mysql.connector.connect(
            host=Host,
            user=User,
            password=Password,
            database=Database
            )
        return connection


# create tables
dd = DataBase.getConnection(Host="localhost", User="root", Database="telemetry")
mycursor = dd.cursor()

#Q1 = "CREATE TABLE devicesID (deviceID int PRIMARY KEY AUTO_INCREMENT,  name VARCHAR(255), avgPrice VARCHAR(55), currency VARCHAR(55), amount VARCHAR(55))"
# Q2 = "CREATE TABLE sellhistory (saleID int PRIMARY KEY AUTO_INCREMENT, itemID int, FOREIGN KEY(itemID) REFERENCES itemInfo(itemID), date VARCHAR(255), price VARCHAR(55), currency VARCHAR(55), amount VARCHAR(55))"
#Q3 = "CREATE TABLE pricechange (ID int PRIMARY KEY AUTO_INCREMENT, itemID int, FOREIGN KEY(itemID) REFERENCES itemInfo(itemID), price VARCHAR(55), sign VARCHAR(1))"
#mycursor.execute(Q3)
# mycursor.execute(Q2)
#dd.commit()
Q1 = "CREATE TABLE devicesID (deviceID int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(55))"
Q2 = "CREATE TABLE sensors (sensorID int PRIMARY KEY AUTO_INCREMENT, sensorType VARCHAR(55))"
Q3 = "CREATE TABLE telemetryData (deviceID int, sensorID int, FOREIGN KEY(deviceID) REFERENCES devicesID(deviceID), FOREIGN KEY(sensorID) REFERENCES sensors(sensorID), data VARCHAR(55), timestamp bigint)"
mycursor.execute(Q1)
mycursor.execute(Q2)
mycursor.execute(Q3)
dd.commit()