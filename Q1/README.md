Assuming that the access.log is at the same directory, most countries can be calculated by running the script `./ip2geo.sh`

`mmdblookup` command tool is required to install for this shell.

First the bash script will count the number of each unique IP
Then the IP will be converted to its corresponding country by comparing the mmdb file, error code will be popped out if the IP cannot be resolved by any means.
This GeoIP Country database is last updated on 20201222 from https://www.maxmind.com/
Finally the number beside the countries will be summed up, by sorting the number in a descending order, the country with the most hit can be calculated
