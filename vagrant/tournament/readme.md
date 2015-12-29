This Udacity full stack tournament project provides a library for running swiss style competitions.

1. Clone this repository

````bash
git clone https://github.com/stoneyv/fullstack-nanodegree-vm/new/master/vagrant/tournament
cd fullstack-nanodegreem-vm/vagrant/tournament
````

2. If you do not already have vagrant and virtual box installed, follow these directions.
https://docs.vagrantup.com/v2/installation/

3. Start the virtual machine and establish a connection.
````bash
vagrant up
vagrant ssh
cd /vagrant/tournament
````

4. Create the tournament database

````bash
createdb tournament
````

5. Create the tournament tables and views by running tournament.sql from psql.

````
psql
````

````sql
\i tournament.sql
````

6. Run the tournament tests

````bash
python tournament_tests.py
````
