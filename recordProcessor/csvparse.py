import csv
import json
import re

class ValidationError(Exception):
	pass

def validateRow(rowDict):
	if 'MIDDLE_NAME' not in rowDict:
		rowDict['MIDDLE_NAME'] = ''

	def max15char(string):
		if len(string) > 15:
			return '15 character max'
		else:
			return False
	def cannotBeEmpty(string):
		if len(string) == 0:
			return 'cannot be empty'
		else:
			return False
	def checkPhoneNumber(string):
		if not re.compile('^[0-9]{3}-[0-9]{3}-[0-9]{4}$').match(string):
			return 'format must be ###-###-####'
	def checkID(string):
		try:
			number = int(string)
		except ValueError:
			return 'cannot parse integer'
		else:
			if number < 0:
				return 'must be positive'
			if len(string) != 8:
				return 'must have 8 digits'
		return False
	validators = {
		'INTERNAL_ID': lambda name: cannotBeEmpty(name) or checkID(name),
		'FIRST_NAME' : lambda name: max15char(name) or cannotBeEmpty(name),
		'MIDDLE_NAME': max15char,
		'LAST_NAME'  : lambda name: max15char(name) or cannotBeEmpty(name),
		'PHONE_NUM'  : checkPhoneNumber
	}
	errors = ', '.join(
		'{}: {}'.format(key,error)
		for key in validators.keys()
		for error in (validators[key](rowDict[key]),)
		if error
	)
	print(errors)

	if errors != '':
		raise ValidationError(errors)

	if rowDict['MIDDLE_NAME'] == '':
		del rowDict['MIDDLE_NAME']
		

def validateHeaders(headers):
	requiredFields= ['INTERNAL_ID', 'FIRST_NAME', 'LAST_NAME', 'PHONE_NUM']
	missingFields = [ field for field in requiredFields if field not in headers]
	if missingFields != []:
		raise ValidationError(
			"Missing fields: {}".format(
				', '.join(missingFields)
			)
		)
		
def parseRow(header,row):
	expectedColumns = len(header)
	actualColumns = len(row)
	if(expectedColumns != actualColumns):
		raise ValidationError("{} columns found, {} expected".format(actualColumns,expectedColumns))
	row = { header[i]: row[i] for i in range(actualColumns) }
	validateRow(row)
	
	output = {
		"id": int(row['INTERNAL_ID']),
		"name": dict( {
			"first": row['FIRST_NAME'],
			"last": row['LAST_NAME']
		},
			**{"middle": row['MIDDLE_NAME']} if 'MIDDLE_NAME' in row else {}
		),
		"phone": row['PHONE_NUM']
	}
	return output


def CSVParse(CSVFile):
	rows = list(csv.reader(CSVFile))
	if( len(rows) == 0 ):
		return [ (0, 'Error: empty file'), [] ]
	header = rows[0]
	try:
		validateHeaders(header)
	except ValidationError as error:
		return ( [ (0,str(error)) ], [] )

	outputObjects = []
	outputErrors = []
	for i in range(1,len(rows)):
		try:
			outputObjects.append(parseRow(header,rows[i]))
		except ValidationError as error:
			outputErrors.append((i,str(error)))
	return (outputErrors,outputObjects)
