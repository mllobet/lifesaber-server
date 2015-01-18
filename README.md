# lifesaber-server

Backend for the lifesaver android and pebble apps. Returns list of closest AEDs to locations within Philadelphia and
sends push notifications to nearby smartwatches when a cardiac arrest inicdent is reported.

Endpoints
---

## GET /aed/&lt;lat&gt;/&lt;lon&gt;/
Returns result of the nearest AED to lat lon in the form of, empty JSON otherwise
```
{
  "_id": {
    "$oid": "5223d4036aa47daac8001477"
  },
  "additional_sources": null,
  "address": "1500 Market St",
  "aed_access": "3",
  "aed_count": "1",
  "aed_used": "I don't know",
  "aed_working": "Unknown",
  "app_visible": 1,
  "building": "Steven J Gilbert Dentistry",
  "building_access": "3",
  "building_type": "Medical",
  "city": "Philadelphia",
  "contest": null,
  "created_at": "2013-09-01T23:55:47Z",
  "did": 526,
  "est_number_devices": "1",
  "loc": [
    39.95261,
    -75.16532
  ],
  "loc1": "N\/A",
  "loc2": "Unknown",
  "location_locked": 0,
  "manufacturer": null,
  "public_status": "Private",
  "source": "Canvas",
  "state": "PA",
  "status": "Approved",
  "to_count": 1,
  "updated_at": "2014-09-22T14:19:19Z",
  "zip": "19102",
  "distance_mi": 0.005519959,
  "light_map_marker": 0
}
```

## POST /report/&lt;lat&gt;/&lt;lon&gt;/uid
Alerts all nearby smartwatches with address of incident and nearby AED

## POST /update/&lt;lat&gt;/&lt;lon&gt;/uid
Updates position of a given smartwatch

## GET /poll/&lt;uid&gt;/
For a given uid, return the current user's alert, empty JSON if none found
Returns result in the following form:
loc is in [long,lat] format
```
{
    "aed": {
         "_id": {
           "$oid": "5223d4036aa47daac8001477"
         },
         "additional_sources": null,
         "address": "1500 Market St",
         "aed_access": "3",
         "aed_count": "1",
         "aed_used": "I don't know",
         "aed_working": "Unknown",
         "app_visible": 1,
         "building": "Steven J Gilbert Dentistry",
         "building_access": "3",
         "building_type": "Medical",
         "city": "Philadelphia",
         "contest": null,
         "created_at": "2013-09-01T23:55:47Z",
         "did": 526,
         "est_number_devices": "1",
         "loc": [
           39.95261,
           -75.16532
         ],
         "loc1": "N\/A",
         "loc2": "Unknown",
         "location_locked": 0,
         "manufacturer": null,
         "public_status": "Private",
         "source": "Canvas",
         "state": "PA",
         "status": "Approved",
         "to_count": 1,
         "updated_at": "2014-09-22T14:19:19Z",
         "zip": "19102",
         "distance_mi": 0.005519959,
         "light_map_marker": 0
        },
    "addr" : "Street name of the incoming alert"
}
```
