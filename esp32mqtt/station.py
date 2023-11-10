from locker import Locker

class Station:
    def __init__(self, id, lockers):
        self.id = id
        self.lockers = {}
        for i in lockers:
            self.lockers[i.nickname] = i

    def create_mesagge(self):
        message = {
            "station_id": self.id,
            "lockers": []
        }
        for i in self.lockers.keys():
            message["lockers"].append(self.lockers[i].status())

        return message

    def load(self, locker_id):
        if locker_id in list(self.lockers.keys()):
            return self.lockers[locker_id].operator_load()
        return False
    
    def unload(self, locker_id):
        if locker_id in list(self.lockers.keys()):
            return self.lockers[locker_id].client_unload()
        return False
    
    def changeState(self, locker_id, state):
        if locker_id in list(self.lockers.keys()):
            if state < 5 and state > 0:
                print('yes2')
                self.lockers[locker_id].state = int(state)
                return True
        return False