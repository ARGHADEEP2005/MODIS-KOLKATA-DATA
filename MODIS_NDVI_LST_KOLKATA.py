import ee
import pandas as pd
ee.Initialize()
region = ee.Geometry.Rectangle([88.30, 22.40, 88.50, 22.60])
lst = ee.ImageCollection("MODIS/006/MOD11A2") \
        .select("LST_Day_1km") \
        .filterDate("2023-01-01", "2023-01-31") \
        .filterBounds(region)
ndvi = ee.ImageCollection("MODIS/006/MOD13A1") \
         .select("NDVI") \
         .filterDate("2023-01-01", "2023-01-31") \
         .filterBounds(region)
lst_img = lst.median().multiply(0.02).subtract(273.15).rename("LST_Celsius")
ndvi_img = ndvi.median().multiply(0.0001).rename("NDVI")
combined_img = lst_img.addBands(ndvi_img)
sample = combined_img.sample(
    region=region,
    scale=1000,
    numPixels=200,
    geometries=True
)
features = sample.getInfo()['features']
data = []
for f in features:
    props = f['properties']
    coords = f['geometry']['coordinates']
    data.append({
        'Longitude': coords[0],
        'Latitude': coords[1],
        'LST_Celsius': props['LST_Celsius'],
        'NDVI': props['NDVI']
    })
df = pd.DataFrame(data)
df.to_csv("ecosystem_satellite_data.csv", index=False)
print(" Satellite data saved to ecosystem_satellite_data.csv")
