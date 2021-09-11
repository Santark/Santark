### Initial Configuration

To run the app, first run the `setup.sh` file directly to create the database tables. Might need to give permission:

```
$ chmod +x setup.sh; 
$ ./setup.sh
```

The above command would also insert some default user in the User table.

You only need to do this once, unless you change your model definitions (see below).

Then run the app itself:

```
$ python app.py
```

Visit [http://localhost:5000/](http://localhost:5000/) in your browser to see the results.

### Running sqlite 

```
$ sqlite3 splitwise.db
```

To fetch the schema of the tables, on the sqlite cli

```
$ .schema
```

To clear the db, and again initilize the default users, delete the file `splitwise.db` and rerun `setup.sh`