from sesh.store import Store


def handle_reset(store: Store) -> None:
    # clear current sesh - will raise SessionStorageError if it fails
    store.current_manager.pop()

    # delete data rows - will raise DatabaseError if it fails
    store.reset_data()
