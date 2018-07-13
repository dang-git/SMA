# Used on all around the app where chartdata is needed
global chartdata
chartdata = {}
# Used for storing chartdata to be saved in db
global chartdatafordb
chartdatafordb = {}
# Stores the snapshot name retrieved from db, then used in load snapshot dropdown
global snapshotlist
snapshotlist = []

# Stores snapshot owner id to be used in querying the snapshot list
global snapshot_owner
snapshot_owner = ""

global SNAPSHOT_LIST
SNAPSHOT_LIST = []

# temp
global quick_stats
quick_stats = {}
# temp
global diag_chartdata
diag_chartdata = {}
# global timeline
# chartdata = {}