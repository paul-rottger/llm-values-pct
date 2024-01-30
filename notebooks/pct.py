"""
Take PCT test via requests

Author: Dr Musashi Hinck

"""

# %%
import requests
import logging
from time import sleep
from dataclasses import dataclass
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# %%
URL = "https://www.politicalcompass.org/test/en"
ALL_ITEMS = [
    [
        "globalisationinevitable",
        "countryrightorwrong",
        "proudofcountry",
        "racequalities",
        "enemyenemyfriend",
        "militaryactionlaw",
        "fusioninfotainment",
    ],
    [
        "classthannationality",
        "inflationoverunemployment",
        "corporationstrust",
        "fromeachability",
        "freermarketfreerpeople",
        "bottledwater",
        "landcommodity",
        "manipulatemoney",
        "protectionismnecessary",
        "companyshareholders",
        "richtaxed",
        "paymedical",
        "penalisemislead",
        "freepredatormulinational",
    ],
    [
        "abortionillegal",
        "questionauthority",
        "eyeforeye",
        "taxtotheatres",
        "schoolscompulsory",
        "ownkind",
        "spankchildren",
        "naturalsecrets",
        "marijuanalegal",
        "schooljobs",
        "inheritablereproduce",
        "childrendiscipline",
        "savagecivilised",
        "abletowork",
        "represstroubles",
        "immigrantsintegrated",
        "goodforcorporations",
        "broadcastingfunding",
    ],
    [
        "libertyterrorism",
        "onepartystate",
        "serveillancewrongdoers",
        "deathpenalty",
        "societyheirarchy",
        "abstractart",
        "punishmentrehabilitation",
        "wastecriminals",
        "businessart",
        "mothershomemakers",
        "plantresources",
        "peacewithestablishment",
    ],
    [
        "astrology",
        "moralreligious",
        "charitysocialsecurity",
        "naturallyunlucky",
        "schoolreligious",
    ],
    [
        "sexoutsidemarriage",
        "homosexualadoption",
        "pornography",
        "consentingprivate",
        "naturallyhomosexual",
        "opennessaboutsex",
    ],
]

# %% Classes
@dataclass
class PCTItem:
  """Dataclass for PCT item"""
  name: str
  page: int
  value: int = 0

  def answer(self, value: int) -> None:
    print(f"Setting {self.name} to {value}")
    self.value = value

class PCTPage:
  "Container for page of PCT"
  index: int
  items: list[PCTItem]
  payload: dict[str, str]

  def __init__(self, index, items) -> None:
    self.index = index
    self.items = [PCTItem(name=item, page=index) for item in items]
    self.payload = {"page": str(index), "carried_ec": "", "carried_soc": "", "populated": ""}

  def __getitem__(self, index):
    return self.items[index]

  def update_payload(self, carried_vals: dict) -> None:
    self.payload = carried_vals

  def submit(self, url: str, session: requests.Session) -> requests.Response:
    "Prepare, submit, return response"
    print("Submitting page "+str(self.index))
    for i in self.items: # Append items to payload
      self.payload[i.name] = str(i.value)
    print("Payload values: ", self.payload)
    response = session.post(url, params=self.payload)
    return response

class PCT:
  """Main class for Political Compass Test
  
  Set values with `set_values`. Accepts list of ints (0-3)
  Take test with `take_test`. Accepts optional delay in seconds.
  
  """
  url: str
  pages: list[PCTPage]

  def __init__(self, url: str, items: list[list]=ALL_ITEMS) -> None:
    self.url = url
    self.session = requests.Session()
    self.pages = []
    for i, page in enumerate(items, 1):
      p = PCTPage(index=i, items=page)
      self.pages.append(p)

  def __getitem__(self, index):
    return self.pages[index]

  def set_values(self, vals: list[int]):
    "Set all values"
    assert len(vals) == len([item for page in self.pages for item in page.items]), "Wrong number of values"
    i = 0
    for page in self.pages:
      for item in page.items:
        item.answer(int(vals[i]))
        i += 1

  def take_test(self, delay: int=1) -> dict[str, float]:
    for i, page in enumerate(self.pages):
      response = page.submit(self.url, self.session)
      if i<len(self.pages)-1: # Not last page
        carried_vals = self._parse_response(response)
        self.pages[i+1].update_payload(carried_vals)
        sleep(delay)
    vals = self._parse_final(response)
    return vals

  def _parse_response(self, response: requests.Response) -> dict[str, str]:
    "Parse response for carry-over values"
    html = BeautifulSoup(response.text, features="html.parser")
    form = html.find("form")
    inputs = form.find_all("input")
    carried_vals = {
        "page": inputs[0].attrs["value"],
        "carried_ec": inputs[1].attrs["value"],
        "carried_soc": inputs[2].attrs["value"],
        "populated": inputs[3].attrs["value"],
    }
    return carried_vals
  
  def _parse_final(self, response: requests.Response) -> dict[str, float]:
    "Parse response for final answers"
    vals = urlparse(response.url).query.split("&")
    return {v.split('=')[0]:float(v.split('=')[1]) for v in vals}


# %% Testing
def test_pct():
  pct = PCT(url=URL, items=ALL_ITEMS)
  # All 0s
  pct.take_test() # 0, -4.36

  # %% Change to all 2s
  pct = PCT(url=URL, items=ALL_ITEMS)
  len([item for page in pct.pages for item in page.items]) # 62 items total
  pct.set_values([2]*62)
  pct.take_test() # 0.38, 2.41





