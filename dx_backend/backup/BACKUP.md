### Goal
Create a snapshot of only your custom app data from the production database (without Django/contrib system tables) and import it into your local development environment using Django fixtures.

Full Dump:
1. Dump origin database
```shell
python manage.py dumpdata  -a  --skip-checks --natural-foreign --natural-primary  --format json   --output snapshot_$(date +%F).json
```
2. Copy file locally:
```bash
docker cp <containerId>:/applciation/snapshot_$(date +%F).json ./
```
3. Move local database
```bash
mv db.sqlite3 db.sqlite3.$(date +%F).local
```
4. Initialize local database
```bash
python manage.py migrate --run-syncdb
```
5. Load data:
```bash
python manage.py loaddata snapshot_$(date +%F).json
```
