reader
======

Docker
------

    docker build -t dcwatson/reader:latest .
    docker run -d --name reader-postgres postgres
    docker run -it --rm -e READER_DB_HOST=db -e READER_DB_USER=postgres --link reader-postgres:db  dcwatson/reader migrate
    docker run -it --rm -p 8000:8000 -e READER_DB_HOST=db -e READER_DB_USER=postgres --link reader-postgres:db  dcwats/reader runserver 0.0.0.0:8000
