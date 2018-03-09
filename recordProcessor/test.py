import unittest

import io

from csvparse import CSVParse

class TestCSVParse(unittest.TestCase):
	def setUp(self):
		pass
	
	def genericTester(self,input,output):
		# tests output of CSVParse on input string against output
		self.assertEqual(
			CSVParse( io.StringIO(input) ),
			output
		)
		
	def test_no_middle_name(self):
		self.genericTester(
			'INTERNAL_ID,FIRST_NAME,MIDDLE_NAME,LAST_NAME,PHONE_NUM\n12345678,Bobby,,Tables,555-555-5555',
			(
				[],
				[
				    {
					"id": 12345678,
					"name": {
					    "first": "Bobby",
					    "last": "Tables"
					},
					"phone": "555-555-5555"
				    }
				]
			)
		)
	def test_no_first_name(self):
		self.genericTester(
			'INTERNAL_ID,MIDDLE_NAME,LAST_NAME,PHONE_NUM\n12345678,Bobbith,Tables,555-555-5555',
			(
				[ (0,'Missing fields: FIRST_NAME') ],
				[]
			)
		)

	def test_mixed(self):
		self.genericTester(
			'\n'.join([
				'INTERNAL_ID,FIRST_NAME,LAST_NAME,PHONE_NUM',
				'12345678,Johannathanielle,Tables,555-555-5555',
				'12345678,Bobbith,Tables,555-555-5555',
			]),
			(
				[ (1,'FIRST_NAME: 15 character max') ],
				[
				    {
					"id": 12345678,
					"name": {
					    "first": "Bobbith",
					    "last": "Tables"
					},
					"phone": "555-555-5555"
				    }
				]
			)
		)

	def test_mixed(self):
		self.genericTester(
			'\n'.join([
				'INTERNAL_ID,FIRST_NAME,LAST_NAME,PHONE_NUM',
				'12345678,Johannathanielle,Tables,555-555-5555',
				'12345678,Bobbith,Tables,555-555-5555',
				'12345678,,Tables,55-555-5555',
			]),
			(
				[
					(1,'FIRST_NAME: 15 character max'),
					(3, 'FIRST_NAME: cannot be empty; PHONE_NUM: format must be ###-###-####')
				],
				[
				    {
					"id": 12345678,
					"name": {
					    "first": "Bobbith",
					    "last": "Tables"
					},
					"phone": "555-555-5555"
				    }
				]
			)
		)

if __name__ == '__main__':
	unittest.main()
