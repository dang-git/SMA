from SMAApp.models import Snapshot, User
from SMAApp import globals

# Returns a snapshot list containing tuples with snapshot id and its text
# in this format [(id1,text1),(id2,text2)]
def get_snapshot_list():
    snapshot_list = []
    snap = ()
    snapshot_count = Snapshot.objects.count()
    i = 0
    print("get_snap ", snapshot_list)
    print("snapcount ", snapshot_count)
    while i < snapshot_count:
        for user in User.objects(_id='5b4c58f355d14c1b60591ee6'): #TODO replace with globals.user_id
            print("get_snap inside", snapshot_list,i)
            snap = (user.snapshots[i]['value'],user.snapshots[i]['text']) 
            snapshot_list.append(snap)
        i += 1
    # snapshot_list = [(snapshotObj._id,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner=globals.snapshot_owner)]
    return snapshot_list

def check_if_email_exists(email):
    is_exists = False
    if User.objects(email=email):
        is_exists = True
    return is_exists