# Convective Storms with NEXRAD Data
Having good data for Severe Convective Storms is extremely valuable, and something I would classify as "Superior Risk Insight". NEXRAD from NOAA has all the data. We just need to visualize it in a delightfully usefule way.

## Getting the Data
NEXRAD data is available from Google and AWS, though the AWS data seems to be more complete.

 - [Google](https://cloud.google.com/storage/docs/public-datasets/nexrad) - [data](https://console.cloud.google.com/storage/browser/gcp-public-data-nexrad-l2;tab=objects?_ga=2.25841595.726508657.1727641611-289069247.1716556699&prefix=&forceOnObjectsSortingFiltering=false)
 - [AWS](https://registry.opendata.aws/noaa-nexrad/) - [data](https://noaa-nexrad-level2.s3.amazonaws.com/index.html)

Here's a one-liner to get all data for Cleveland on the 6th of August 2024:  

`aws s3 cp s3://noaa-nexrad-level2/2024/08/06/KCLE/ . --recursive --no-sign-request`  

This requires the aws cli which can be installed with:
```
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```
Here are [the docs](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) for awc cli.

## Understanding the Data
Here's a [helpful guide from SAS](https://documentation.sas.com/doc/en/etscdc/14.2/etsug/etsug_sasenoaa_details02.htm). There's a NEXRAD site in Cleveland. Filter to `KCLE` for this data.

## Helpful links

 - [Box Blur, NetCDF, and Radar Data](https://observablehq.com/@cguastini/box-blur-netcdf-and-radar-data)
 - [RSL User Guide](https://trmm-fc.gsfc.nasa.gov/trmm_gv/software/rsl/users_guide.php)
 - [NASA's RSL Library](https://trmm-fc.gsfc.nasa.gov/trmm_gv/software/rsl/) used for radar decoding

