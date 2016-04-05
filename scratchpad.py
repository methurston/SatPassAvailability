# class Elements(object):
#     def __init__(self,
#                  line,
#                  satNum,
#                  classification,
#                  launchYear,
#                  launchNum,
#                  piece,
#                  epochYear,
#                  epochDay,
#                  firstMeanMotion,
#                  secondMeanMotion,
#                  bstar,
#                  numZero,
#                  elementSetNumber,
#                  lineOneChecksum,
#                  inclination,
#                  ascension,
#                  eccentricity,
#                  argumentOfPerigee,
#                  meanAnomaly,
#                  meanMotion,
#                  revolutionNum,
#                  lineTwoChecksum):
#         self.line = line
#         self.satNum = satNum
#         self.classification = classification
#         self.launchYear = launchYear
#         self.launchNum = launchNum
#         self.piece = piece
#         self.epochYear = epochYear
#         self.epochDay = epochDay
#         self.firstMeanMotion = firstMeanMotion
#         self.secondMeanMotion = secondMeanMotion
#         self.bstar = bstar
#         self.numZero = numZero
#         self.elementSetNumber = elementSetNumber
#         self.lineOneChecksum = lineOneChecksum
#         self.inclination = inclination
#         self.ascension = ascension
#         self.eccentricity = eccentricity
#         self.argumentOfPerigee = argumentOfPerigee
#         self.meanAnomaly = meanAnomaly
#         self.meanMotion = meanMotion,
#         self.revolutionNum = revolutionNum,
#         self.lineTwoChecksum = lineTwoChecksum


# sample tle (SO-50)
# so_50 = ephem.readtle('SO-50',
#                       '1 27607U 02058C   16091.67694102  .00000370  00000-0  52117-4 0  9999',
#                       '2 27607  64.5570  37.6564 0075164 233.0297 126.4406 14.75113127713838')
#
#
# def sample():
#     so_50.compute(home)
#     for i in range(10):
#         home.date = datetime.utcnow()
#         print(home.date)
#         print('SO-50: altitude {} deg, azimuth {} deg'.format(so_50.alt * degrees_per_radian,
#                                                               so_50.az * degrees_per_radian))
#         time.sleep(5)
