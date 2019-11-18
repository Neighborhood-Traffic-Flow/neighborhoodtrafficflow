"""
Dictionaries with dashboard control options
Hard-coded options for
1. Map type
2. Seattle neighborhoods
3. Centroids
"""


# Radio and Checkbox
MAP_TYPE = {
    'flow': 'Traffic Flow Counts',
    'speed': 'Speed Limits',
    'road': 'Road Type'
},

# Dropdown
NEIGHBORHOODS = {
    '0': 'West Woodland',
    '1': 'Olympic Manor',
    '2': 'Sunset Hill',
    '3': 'Maple Leaf',
    '4': 'Dunlap',
    '5': 'South Delridge',
    '6': 'Laurelhurst',
    '7': 'Eastlake',
    '8': 'Waterfront',
    '9': 'Whittier Heights',
    '10': 'Admiral',
    '11': 'Minor',
    '12': 'Arbor Heights',
    '13': 'Meadowbrook',
    '14': 'Wedgwood',
    '15': 'Wallingford',
    '16': 'Interbay',
    '17': 'Fauntleroy',
    '18': 'Green Lake',
    '19': 'Columbia City',
    '20': 'Uptown',
    '21': 'Olympic Hills',
    '22': 'Central',
    '23': 'Judkins Park',
    '24': 'Lower Queen Anne',
    '25': 'Leschi',
    '26': 'Madison Park',
    '27': 'East Queen Anne',
    '28': 'Brighton',
    '29': 'Alki',
    '30': 'Little Saigon',
    '31': 'Mt. Baker',
    '32': 'South Park',
    '33': 'International District',
    '34': 'Hawthorne Hills',
    '35': 'Phinney Ridge',
    '36': 'South Beacon Hill',
    '37': 'Jackson Place',
    '38': 'Holly Park',
    '39': 'Crown Hill',
    '40': 'Garfield',
    '41': 'Industrial District',
    '42': 'Windermere',
    '43': 'North College Park',
    '44': 'Seward Park',
    '45': 'Capitol Hill',
    '46': 'Madrona',
    '47': 'Beacon Hill',
    '48': 'Roxhill',
    '49': 'Broadmoor',
    '50': 'Rainier View',
    '51': 'Riverview',
    '52': 'Haller Lake',
    '53': 'West Queen Anne',
    '54': 'Hillman City',
    '55': 'Fairmount Park',
    '56': 'High Point',
    '57': 'Portage Bay',
    '58': 'Westlake',
    '59': 'Fremont',
    '60': 'Belltown',
    '61': 'Matthews Beach',
    '62': 'Ravenna',
    '63': 'Yesler Terrace',
    '64': 'Roosevelt',
    '65': 'Harbor Island',
    '66': 'View Ridge',
    '67': 'Pinehurst',
    '68': 'Genesee',
    '69': 'Junction',
    '70': 'North Delridge',
    '71': 'Denny - Blaine',
    '72': 'Bitter Lake',
    '73': 'Broadview',
    '74': 'Blue Ridge',
    '75': 'Magnolia',
    '76': 'Greenwood',
    '77': 'Ballard',
    '78': 'Seaview',
    '79': 'First Hill',
    '80': 'Northgate',
    '81': 'Rainier Beach',
    '82': 'Cedar Park',
    '83': 'Downtown',
    '84': 'Victory Heights',
    '85': 'Montlake',
    '86': 'North Queen Anne',
    '87': 'Lakewood',
    '88': 'Georgetown',
    '89': 'Bryant',
    '90': 'Atlantic',
    '91': 'Highland Park',
    '92': 'University District',
    '93': 'Sand Point',
    '94': 'Madison Valley',
    '95': 'Denny Triangle',
    '96': 'Gatewood',
    '97': 'Woodland',
    '98': 'North Beach',
    '99': 'North Beacon Hill',
    '100': 'South Lake Union',
    '101': 'Pioneer Square',
    '102': 'Loyal Heights',
}

CENTROIDS = {
    '0': (-122.368495, 47.666952),
    '1': (-122.382184, 47.696061),
    '2': (-122.401110, 47.678887),
    '3': (-122.317410, 47.696144),
    '4': (-122.269512, 47.525399),
    '5': (-122.360966, 47.526213),
    '6': (-122.278339, 47.658362),
    '7': (-122.326105, 47.643213),
    '8': (-122.346046, 47.606083),
    '9': (-122.371386, 47.683311),
    '10': (-122.388371, 47.578683),
    '11': (-122.309675, 47.606329),
    '12': (-122.380802, 47.508817),
    '13': (-122.296598, 47.705118),
    '14': (-122.292831, 47.690557),
    '15': (-122.333978, 47.659621),
    '16': (-122.380780, 47.642243),
    '17': (-122.390280, 47.523241),
    '18': (-122.335657, 47.679392),
    '19': (-122.287199, 47.562774),
    '20': (-122.354512, 47.622981),
    '21': (-122.302909, 47.726842),
    '22': (-122.305198, 47.615036),
    '23': (-122.301811, 47.596117),
    '24': (-122.354843, 47.627817),
    '25': (-122.290374, 47.599615),
    '26': (-122.283342, 47.632185),
    '27': (-122.350213, 47.636572),
    '28': (-122.275310, 47.539025),
    '29': (-122.398931, 47.579379),
    '30': (-122.315049, 47.595587),
    '31': (-122.289518, 47.581512),
    '32': (-122.324176, 47.528140),
    '33': (-122.325396, 47.596857),
    '34': (-122.272850, 47.672873),
    '35': (-122.355760, 47.675180),
    '36': (-122.288140, 47.524892),
    '37': (-122.309085, 47.595824),
    '38': (-122.288233, 47.538883),
    '39': (-122.371424, 47.696083),
    '40': (-122.299544, 47.607429),
    '41': (-122.344327, 47.568431),
    '42': (-122.262203, 47.670192),
    '43': (-122.336591, 47.698733),
    '44': (-122.259864, 47.547859),
    '45': (-122.316220, 47.626038),
    '46': (-122.289033, 47.612506),
    '47': (-122.304189, 47.554408),
    '48': (-122.370702, 47.527768),
    '49': (-122.290445, 47.638035),
    '50': (-122.257306, 47.501683),
    '51': (-122.353751, 47.546024),
    '52': (-122.335754, 47.720948),
    '53': (-122.366849, 47.634243),
    '54': (-122.280352, 47.550267),
    '55': (-122.380489, 47.555319),
    '56': (-122.368438, 47.543389),
    '57': (-122.319052, 47.647110),
    '58': (-122.342162, 47.636814),
    '59': (-122.351991, 47.655899),
    '60': (-122.348323, 47.615130),
    '61': (-122.279811, 47.703273),
    '62': (-122.300503, 47.675716),
    '63': (-122.320222, 47.601988),
    '64': (-122.313525, 47.680743),
    '65': (-122.351675, 47.581128),
    '66': (-122.274520, 47.682922),
    '67': (-122.319216, 47.722409),
    '68': (-122.282147, 47.569020),
    '69': (-122.386359, 47.565427),
    '70': (-122.365605, 47.562460),
    '71': (-122.283584, 47.618269),
    '72': (-122.350214, 47.719558),
    '73': (-122.366683, 47.719532),
    '74': (-122.373068, 47.704496),
    '75': (-122.406913, 47.651576),
    '76': (-122.354694, 47.693421),
    '77': (-122.386451, 47.669181),
    '78': (-122.395606, 47.552206),
    '79': (-122.323272, 47.608929),
    '80': (-122.321691, 47.708548),
    '81': (-122.258415, 47.511728),
    '82': (-122.286518, 47.722974),
    '83': (-122.334047, 47.607564),
    '84': (-122.305542, 47.711108),
    '85': (-122.307648, 47.641026),
    '86': (-122.365422, 47.648118),
    '87': (-122.267535, 47.558514),
    '88': (-122.316626, 47.540629),
    '89': (-122.286431, 47.671645),
    '90': (-122.300452, 47.584941),
    '91': (-122.341968, 47.525658),
    '92': (-122.306942, 47.659884),
    '93': (-122.256520, 47.682249),
    '94': (-122.295972, 47.625139),
    '95': (-122.337597, 47.616769),
    '96': (-122.385911, 47.538000),
    '97': (-122.347351, 47.669116),
    '98': (-122.396211, 47.695665),
    '99': (-122.309686, 47.577335),
    '100': (-122.335006, 47.626808),
    '101': (-122.332902, 47.597397),
    '102': (-122.384885, 47.683230)
}
