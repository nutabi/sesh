import click

from sesh.store import Store


def handle_reset(store: Store):
    # clear current sesh
    store.current_manager.pop()

    # delete data rows
    store.db_conn.execute("DELETE FROM sesh")
    store.db_conn.execute("DELETE FROM tag")
    store.db_conn.commit()
