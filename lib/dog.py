import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    all = []

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed 
        self.id = None
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)

    def save(self):
        if not self.id:
            sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
            """

            CURSOR.execute(sql, (self.name, self.breed))

            self.id = CURSOR.lastrowid
            return self
        else:
            return self.update()
    
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        if row is not None:
            dog = cls(row[1], row[2])
            dog.id = row[0]
            return dog
        else:
            return None
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """

        all = CURSOR.execute(sql).fetchall()

        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (name,)).fetchone()

        return cls.new_from_db(dog)
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        dog = CURSOR.execute(sql, (id,)).fetchone()

        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ? AND breed = ?
        """
        existing_dog_data = CURSOR.execute(sql, (name, breed)).fetchone()

        if existing_dog_data:
            # If the dog exists, create a Dog instance using new_from_db and return it
            return cls.new_from_db(existing_dog_data)
        else:
            # If the dog doesn't exist, create a new dog, save it, and return it
            new_dog = cls.create(name, breed)
            return new_dog
    
    def update(self):
        # Update the row in the database with the new name
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))

        return self