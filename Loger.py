infile = open('Token_3.dat', 'r')
outfile = open('log.dat', 'w')


# This function creates a .tars files
def makeTarfile(name, loglines):
    tarname = name + '.tars'
    tarfile = open(tarname, 'w')

    for line in loglines:
        print(line, end='\n', file=tarfile)

def createFileName(sernum, result, stoptime, logline):
    return 0

#This function looks through token.dat file and creates a unique filename
def main():
    setcount = [0, False, False, False]
    setstr = ['', '', '', '']
    board_count, sn_sts, rslt_sts, stptime_sts = setcount
    filename, sn, rslt, stptime = setstr

    for line in infile:
        test_sernum = line.startswith('    (USER:  SN:')
        test_result = line.startswith('    (USER:  RESULT :')
        test_stoptime = line.startswith('    (USER:  STOP TIME :')

        if test_sernum:
            sn = line[-20:-2]
            sn_sts = True
            board_count += 1

        if test_result:
            rslt = line[-6:-2]
            rslt_sts = True

        if test_stoptime:
            # evaluate date-time startpoint
            strtpoint = line.index('TIME :')

            # define slice range for the date. Create stoptime sring
            date_indx1 = strtpoint + 7
            date_indx2 = date_indx1 + 10
            slicerange = slice(date_indx1, date_indx2)
            slicedate = line[slicerange].split('/')
            stptime = slicedate[0] + '_' + slicedate[1] + '_' + slicedate[2] + '_'

            # define slice range for the Time. Update stoptime string
            time_indx1 = date_indx2 + 1
            time_indx2 = time_indx1 + 8
            slicerange = slice(time_indx1, time_indx2)
            slicetime = line[slicerange].split(':')
            stptime += slicetime[0] + '_' + slicetime[1] + '_' + slicetime[2]

            #print(stoptime, end='\n', file=outfile)
            stptime_sts = True

        if sn_sts & rslt_sts & stptime_sts:
            filename = str(rslt) + '_' + str(sn) + '_' + str(board_count) + '_' + str(stptime)
            print(sn, rslt, stptime, filename, sep='\n', end='\n\n', file=outfile)
            sn_sts, rslt_sts, stptime_sts = [False, False, False]

main()
print('Done.')
