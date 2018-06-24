with open('new.dat', 'r') as infile:
    loglist = list(enumerate(infile, start=1))

#The function below looks through token.dat file and creates a unique filename
def main(loglist):
    main_data = {'Client': 'CHoneywell',
                 'Tester': 'NSpectrum',
                 'Process': 'PICT',
                 'Site': 'p20',
                 'Line': 'L24ICT',
                 'Fails': [],
                 'F_qnt': 0}
    board_count, sn_sts, rslt_sts, stptime_sts = [0, False, False, False]
    filename, sn, rslt, stptime = ['', '', '', '']


    for (num, line) in loglist:

        if not line:
            continue

        elif line.lstrip().startswith('(USER:  SN:'):
            #sn = str(line[-22:-2])
            templs = ''.join(char for char in line if char not in '():').split()
            indx = templs.index('SN') + 1
            sn = str(templs[indx])
            sn_sts = True
            board_count += 1
            main_data['SN'] = 'S' + sn

        elif line.lstrip().startswith('(USER:  START TIME :'):
            strtpoint = line.index('TIME :')
            date_indx1 = strtpoint + 7
            date_indx2 = date_indx1 + 19
            # slicerange = slice(date_indx1, date_indx2)
            main_data['Start Time'] ='[' + str(line[date_indx1:date_indx2])

        elif line.lstrip().startswith('(STEP:'):
            #print(num)
            if main_data['F_qnt'] < 3:          # Change the number to set an amount of failures to be printed to .tars
                #print(main_data['F_qnt'])
                failureFinder(loglist, num, main_data)
            else:
                pass

        elif line.lstrip().startswith('(USER:  RESULT :'):
            templs = ''.join(char for char in line if char not in '():').split()
            indx = templs.index('RESULT') + 1
            rslt = str(templs[indx])
            rslt_sts = True
            main_data['Status'] = 'T' + rslt[0]

        elif line.lstrip().startswith('(USER:  STOP TIME :'):
            # evaluate date-time startpoint
            strtpoint = line.index('TIME :')

            # define slice range for date. Create stoptime sring
            date_indx1 = strtpoint + 7
            date_indx2 = date_indx1 + 10
            slicerange = slice(date_indx1, date_indx2)
            slicedate = line[slicerange].split('/')
            stptime = str(slicedate[0] + '_' + slicedate[1] + '_' + slicedate[2] + '_')

            # define slice range for Time. Update stoptime string
            time_indx1 = date_indx2 + 1
            time_indx2 = time_indx1 + 8
            slicerange = slice(time_indx1, time_indx2)
            slicetime = line[slicerange].split(':')
            stptime += str(slicetime[0] + '_' + slicetime[1] + '_' + slicetime[2])

            # adding 'Stop Time' to dictionary
            slicerange = slice(date_indx1, time_indx2)
            main_data['Stop Time'] = ']' + str(line[slicerange])
            stptime_sts = True

        if sn_sts & rslt_sts & stptime_sts:
            filename = rslt + '_' + sn + '_' + str(board_count) + '_' + stptime
            main_data['File Name'] = filename
            makeTarfile(main_data)
            #print(main_data, sep='\n\n', end='\n', file=outfile)
            #print(sn, rslt, stptime, filename, sep='\n', end='\n\n', file=outfile)
            main_data['Fails'] = []
            main_data['F_qnt'] = 0
            sn_sts, rslt_sts, stptime_sts = [False, False, False]
#------------------------------------------------------------------------------

# This function creates a .tar file
def makeTarfile(data):
    with open(data['File Name'] + '.tars', 'w') as tarfile:
    #tarfile = open(data['File Name'] + '.tars', 'w')
        print(data['SN'],
            data['Client'],
            data['Tester'],
            data['Process'],
            data['Site'],
            data['Line'],
            data['Start Time'],
            data['Stop Time'],
            data['Status'],
            sep='\n', end='\n', file=tarfile)

        if data['Fails']:
            for (f, l) in data['Fails']:
                print(f, l, sep='\n', end='\n', file=tarfile)
        else:
            pass
#------------------------------------------------------------------------------

#The function below looks for failures in a Tokenlog file. Slice and format data
def failureFinder(ls, linenum, data):
    fail_line, fail_name = ['', '']

    for (num, line) in ls[linenum:]:
        if line.lstrip().startswith(') (STAT: FAIL)'):
            break
        elif not line:
            continue
        else:
            if 'PAGE_NAME' in line:
                templs = ''.join(char for char in line if char not in '():').split()
                indx = templs.index('PAGE_NAME') + 1
                fail_name = 'F' + templs[indx].strip('"')
                #print(templs[indx].strip('"'))
                frmt_line = ''.join(char for char in line if char not in '()').strip()
                fail_line += frmt_line + ' '
                #print(fail_line)

                #indx1 = line.find('PAGE_NAME:') + 11
                #indx2 = line.find(')', indx1)
                #fail_name = fail_name.join(char for char in line[indx1:indx2] if char not in '""')
                #print(fail_name)
            else:
                frmt_line = ''.join(char for char in line if char not in '()').strip()
                fail_line += frmt_line + ' '
                #fail_list += [frmt_line]

    fail_list = [fail_name, '> ' + fail_line]
    #print(fail_list)
    data['Fails'].append(fail_list)
    data['F_qnt'] += 1
    #print(data['F_qnt'])
#------------------------------------------------------------------------------

if __name__ == "__main__" : main(loglist)
print('Done.')
