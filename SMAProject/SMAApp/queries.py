from SMAApp.models import Snapshot, User

# Returns a snapshot list containing tuples with snapshot id and its text
# in this format [(id1,text1),(id2,text2)]
def get_snapshot_list(userid):
    snapshot_list = []
    snap = ()
    # Used aggregate to get the number of snaphots a user has.
    # Particularly this:  'snapshotCount': {'$size': '$snapshots'}
    pipeline = { '$project':{'snapshots': 1, 'snapshotCount': {'$size': '$snapshots'}}}        
    # dummy_id = '5b570b5b55d14c15804bf846'
    for user in User.objects(_id=userid).aggregate(pipeline):
        for snapshot in user['snapshots']:
            snap = (snapshot['value'],snapshot['text']) 
            snapshot_list.append(snap)

    # snapshot_list = [(snapshotObj._id,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner=globals.snapshot_owner)]
    return snapshot_list

def check_if_email_exists(email):
    is_exists = False
    if User.objects(email=email):
        is_exists = True
    return is_exists