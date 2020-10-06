import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='ArtSearchAm295',
                             db='artsearch')

try:
    with connection.cursor() as cursor:
        # Check exist if, then delete
        cursor.execute("DROP TABLE IF EXISTS users")
        # Create a table
        cursor.execute("CREATE TABLE users (email VARCHAR(255), password VARCHAR(255))")
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `email`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()