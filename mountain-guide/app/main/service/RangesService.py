from typing import List
from dao.RangesDao import RangesDao
from model.Range import Range


class RangesService:

    def __init__(self, ranges_dao: RangesDao):
        self.ranges_dao = ranges_dao

    def find_all_ranges(self) -> List[Range]:
        return self.ranges_dao.find_all_ranges()
