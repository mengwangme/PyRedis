import time
import pickle
import os.path


class Memory:
    """
    A simplistic in memory class to encapsulate the data objects manipulated by this application
    volatile is unsaved memory
    expiring is a list of keys and arrays and ttls for
    """
    volatile = {}
    expiring = {}

    def __init__(self):
        self.load_state()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_state()

    def load_state(self):
        if os.path.exists('dump.rdb'):
            state = pickle.load(open('dump.rdb', 'rb'))
            self.volatile = state['volatile']
            self.expiring = state['expiring']
            now = time.time()
            expired = set()
            for entry, ttl in self.expiring.items():
                if ttl <= now:
                    expired.add(entry)
                    if entry in volatile:
                        del self.volatile[entry]
                else:
                    def delete_when_expired(e):
                        del memory.volatile[e]
                        del memory.expiring[e]

                    gevent.spawn_later(ttl, delete_when_expired, entry)

            for expired_key in expired:
                del self.expiring[expired_key]
            #print("dump.rdb loaded into volatile memory")

    def save_state(self):
        pickle.dump({'volatile': self.volatile, 'expiring': self.expiring}, open('dump.rdb', 'wb'))
        #print("dump.rdb saved to disk")


memory = Memory()

