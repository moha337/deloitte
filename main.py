import json 
import unittest
import datetime

with open("./data-1.json","r") as f: #open and read the file data-1.json
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f: #open and read the file data-2.json
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f: #open and read the file result.json
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    # Parse location string into components
    location_parts = jsonObject["location"].split("/")
    #Building Unified Structure
    return {
        "deviceID": jsonObject["deviceID"],  #json object for convertfromformate1  
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": location_parts[0],
            "city": location_parts[1], 
            "area": location_parts[2],
            "factory": location_parts[3],
            "section": location_parts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    } 


def convertFromFormat2(jsonObject): #Two separate functions handle converting different JSON structures into the same unified output format.
    # Parse ISO timestamp to milliseconds
    time_str = jsonObject["timestamp"]
    dt = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=datetime.timezone.utc)
    millisec = int(dt.timestamp() * 1000)
#bulding unified structure
    return {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": millisec,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }


def main(jsonObject):
    result = {}
   # Decide which conversion function to use
    if jsonObject.get('deviceID') is not None:
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):     #A simple test converts and immediately re-loads the expected JSON to verify that it’s valid.
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(
            result,
            jsonExpectedResult
        )

    def test_dataType1(self):      #test the conversion  from type1 to the expected result
        result = main(jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 1 failed'
        )

    def test_dataType2(self):    #test the conversion  from type2 to the expected result
        result = main(jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            'Converting from Type 2 failed'
        )

if __name__ == '__main__': #The unittest.main() functon is called to run the tests.
    unittest.main()
