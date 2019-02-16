
# reading in commandline arguments
all_arguments = sys.argv
# selecting all arguments after python file name
argumentList = all_arguments[1:]
unixOptions = "i:k:c:e:n:m:o:"
gnuOptions = ["inputData=", "keep=", "control=", "case=", "nullValues=", "match=", "output="]

try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit(2)


#metadata file
inputData = ''
outputFileName = ''
keep = ''
control = ''
case = ''
nullValues = ''
match = ''

# evaluate given options
for currentArgument, currentValue in arguments:
    if currentArgument in ("-v", "--verbose"):
        print ("enabling verbose mode")
    elif currentArgument in ("-i", "--inputData"):
        inputData = currentValue
    elif currentArgument in ("-k", "--keep"):
        keep = currentValue
    elif currentArgument in ("-c", "--control"):
        control = currentValue
    elif currentArgument in ("-e", "--case"):
        case = currentValue
    elif currentArgument in ("-n", "--nullValues"):
        nullValues = currentValue
    elif currentArgument in ("-m", "--match"):
        match = currentValue
    elif currentArgument in ("-o", "--output"):
        outputFileName = currentValue

if outputFileName == '':
    print('output put file name not entered')
    sys.exit()
if inputData == '':
    print('metadata file not found')
    sys.exit()
