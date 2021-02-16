# Utility code for ad hoc Database adjustments. 
# Created Sept 2020 GHerson

from replit import db
import copy

# Adding the decoy_offset value to the database (2020-09-19).
db1 = copy.deepcopy(db)  # R&D with a copy of the database, only.
for key in db1:
    print("db1['" + key + "']:'", db1[key])
    if key[0:2] == '16':  # Then key is a timestamp.
        db1[key] = 0.1, db1[key]  # Prepend the decoy_offset.
        print("is now db1['" + key + "']:'", db1[key])

# To alter persistent data, uncomment once above is believed bugless:
#db = copy.deepcopy(db1)