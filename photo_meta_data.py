"""
run with python3 (and exifead library installed) passing in the directory of the photos
Example: python photo_meta_data.py ~/Desktop/camera-photos/
Result is a csv file in the same directory called meta-data.csv with all the details
"""
import os
import sys
import csv
import exifread


def collect_data(path, file_name):
    with open(path, 'rb') as f:
        tags = exifread.process_file(f, details=False)

    if len(tags.keys()) == 0:
        print('No tags processed for file %s' % file_name)

    # extract required data
    image_type = tags['Thumbnail Compression']
    image_width = tags['EXIF ExifImageWidth']
    image_height = tags['EXIF ExifImageLength']
    brand = tags['Image Make']
    model = tags['Image Model']
    date = tags['Image DateTime']

    shutterspeed = tags['EXIF ExposureTime']
    aperture = tags['EXIF FNumber']
    iso = tags['EXIF ISOSpeedRatings']
    flash = tags['EXIF Flash']
    try:
        lens = tags['EXIF LensModel']
    except Exception:
        lens = 'unknown'
    exposure_program = tags['EXIF ExposureProgram']
    focallength = tags['EXIF FocalLength']
    try:
        artist = tags['Image Artist']
    except Exception:
        artist = 'unknown'

    try:
        num, den = str(aperture).split('/')
        division = int(num)/int(den)
    except Exception:
        division = aperture

    return {
        'Image Name': file_name,
        'Image Type': str(image_type),
        'Width (pixels)': str(image_width),
        'Height (pixels)': str(image_height),
        'Camera Brand': str(brand),
        'Camera Model': str(model),
        'Date Taken': str(date),
        'Shutter Speed (s)': str(shutterspeed),
        'Aperture': f'f/{division}',
        'ISO Speed Rating': f'{iso}',
        'Flash Fired': f'{flash}',
        'Exposure Program': f'{exposure_program}',
        'Focal Length (mm)': str(focallength),
        'Lens': str(lens),
        'Creator': str(artist)
    }


def process_photos(directory):
    results = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv') or file_name.endswith('.csv#') or file_name.endswith('.gitignore') or file_name.endswith('.py') or not os.path.isfile(file_name):
            continue
        path = directory + file_name
        info = collect_data(path, file_name)
        results.append(info)

    with open(directory + 'meta-data.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Name', 'Image Type', 'Width (pixels)', 'Height (pixels)', 'Camera Brand', 'Camera Model',
                             'Date Taken', 'Shutter Speed (s)', 'Aperture', 'ISO Speed Rating', 'Flash',
                             'Exposure Program', 'Focal Length (mm)', 'Lens', 'Creator'])
        for row in results:
            spamwriter.writerow([row['Image Name'], row['Image Type'], row['Width (pixels)'], row['Height (pixels)'],
                                 row['Camera Brand'], row['Camera Model'], row['Date Taken'], row['Shutter Speed (s)'],
                                 row['Aperture'], row['ISO Speed Rating'], row['Flash Fired'], row['Exposure Program'],
                                 row['Focal Length (mm)'], row['Lens'], row['Creator']])


if __name__ == '__main__':
    script, directory = sys.argv
    process_photos(directory)
