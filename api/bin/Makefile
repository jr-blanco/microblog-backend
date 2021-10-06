.PHONY: all clean

all: ./var/users.db ./var/timelines.db

./var/users.db: ./users.sql
	sqlite3 $@ < $<

./var/timelines.db: ./timelines.sql
	sqlite3 $@ < $<

clean:
	rm -f ./var/users.db ./var/timelines.db
