from __future__ import print_function
import ephem
import dateutil.parser

so_50 = ephem.readtle('SO-50',
                      '1 27607U 02058C   16112.69329812  .00000250  00000-0  35295-4 0  9993',
                      '2 27607  64.5574 333.4499 0073418 228.7162 130.8101 14.75127411716934')

home = ephem.Observer()
home.lat = 43.6122 * ephem.degree
home.lon = -116.240 * ephem.degree
home.elevation = 831


def sample(str_time):
    start_time = dateutil.parser.parse(str_time)
    print('Starting Time: {}'.format(start_time))
    so_50.compute(home)
    home.date = start_time
    pass_info = home.next_pass(so_50)
    pass_dict = {'AOS_time': pass_info[0].datetime(),
                 'AOS_azimuth': pass_info[1],
                 'max_elevation_time': pass_info[2].datetime(),
                 'max_elevation': pass_info[3],
                 'LOS_time': pass_info[4].datetime(),
                 'LOS_azimuth': pass_info[5]}
    home.date = pass_dict['max_elevation_time']
    so_50.compute(home)
    pass_dict['computed_max_elev_az'] = so_50.az
    return pass_dict


info = sample('2016-04-22T15:00:00.0000Z')
for k, v in sorted(info.iteritems()):
    print('\t{:<20} - {}'.format(k, v))
