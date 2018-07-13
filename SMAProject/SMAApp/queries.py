from SMAApp.models import Snapshot
from SMAApp import globals

def get_snapshot_list():
    snapshot_list = []
    snapshot_list = [(snapshotObj._id,snapshotObj.snapshot_name) for snapshotObj in Snapshot.objects(owner=globals.snapshot_owner)]
    return snapshot_list