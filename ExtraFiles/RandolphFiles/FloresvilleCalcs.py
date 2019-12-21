#import RadioCalcs as rc
from SectorValues import SectorValues

dist=10560
top=4000
O1=8.0
alt=170

tgt=None
bot=None
O2=None

sector_close=SectorValues()
sector_close.assign_values(dist, alt, top, tgt, bot, O1, O2)
sector_close.find_O2()
sector_close.find_bot()
sector_close.find_tgt()
print(sector_close)
print()

dist=158400
O1=8.0
alt=170
O2=sector_close.dict_values()["O2"]

top=None
tgt=None
bot=None

sector_far=SectorValues()
sector_far.assign_values(dist, alt, top, tgt, bot, O1, O2)
sector_far.find_tgt()
sector_far.find_top()
sector_far.find_bot()
print(sector_far)
