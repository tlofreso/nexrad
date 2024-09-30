import pyart
import numpy as np
import pandas as pd
import json
from rich import print
from pathlib import Path
from datetime import datetime

def process_radar_file(file_path):
    radar = pyart.io.read_nexrad_archive(file_path)
    
    # Extract reflectivity data
    refl = radar.get_field(0, 'reflectivity')
    
    # Simple threshold for identifying potential severe weather (adjust as needed)
    severe_mask = refl > 40  # Consider reflectivity > 40 dBZ as potential severe weather
    
    if np.any(severe_mask):
        # Get latitude and longitude data
        lat, lon = radar.get_lat_lon()
        
        # Calculate centroid of severe weather
        severe_lat = np.mean(lat[severe_mask])
        severe_lon = np.mean(lon[severe_mask])
        
        # Calculate maximum reflectivity and affected area
        max_refl = np.max(refl[severe_mask])
        affected_area = np.sum(severe_mask) * (1000 / 33)**2  # Approximate area in km²
        
        # Extract timestamp from filename
        timestamp = datetime.strptime(file_path.stem.split('_')[1], '%Y%m%d%H%M%S')
        
        return {
            'timestamp': timestamp.isoformat(),
            'lat': float(severe_lat),
            'lon': float(severe_lon),
            'max_reflectivity': float(max_refl),
            'affected_area': float(affected_area)
        }
    return None

def process_daily_data(data_dir):
    data_dir = Path(data_dir)
    all_scans = []
    
    # Process only the uncompressed V06 files (exclude MDM files)
    for file in data_dir.glob('*_V06'):
        if '_MDM' not in file.name:  # Exclude MDM files
            try:
                result = process_radar_file(file)
                print(result)
                if result:
                    all_scans.append(result)
            except Exception as e:
                print(f"Error processing {file}: {e}")
    
    return all_scans

# Process the data
data_directory = "data"  # Update this to your actual data directory
daily_data = process_daily_data(data_directory)

# Convert to pandas DataFrame for easier manipulation
df = pd.DataFrame(daily_data)

# Ensure timestamps are in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sort the data by timestamp
df.sort_values('timestamp', inplace=True)

# Aggregate data to 15-minute intervals
aggregated_data = df.set_index('timestamp').resample('15T').agg({
    'lat': 'mean',
    'lon': 'mean',
    'max_reflectivity': 'max',
    'affected_area': 'sum'
}).reset_index()

# Convert to JSON
json_data = aggregated_data.to_json(orient='records', date_format='iso')

# Save to file
output_file = 'kcle_daily_radar_summary.json'
with open(output_file, 'w') as f:
    f.write(json_data)

print(f"Processed {len(daily_data)} scans into {len(aggregated_data)} 15-minute aggregations.")
print(f"Data saved to {output_file}")