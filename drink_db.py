from tinydb import TinyDB, where

class Drinks(TinyDB):
    """
    A class that records numbers of drinks ordered. 
    """
    def __init__(self, path: str):
        super().__init__(path)

    def add_drink(self, member_id: int):
        """Add 1 drink to a member's record."""
        record = self.search(where("member_id") == member_id)
        if record:
            current_drinks = record[0]["drinks"]
            self.update({"drinks": current_drinks + 1}, where("member_id") == member_id)
        else:
            self.insert({"member_id": member_id, "drinks": 1})
        

    def get_num_drinks(self, member_id: int):
        """Get the number of drinks a member has ordered."""
        record = self.search(where("member_id") == member_id)
        if record:
            return record[0]["drinks"]
        else:
            return 0
