from time import sleep
from sys import argv
import json
import os
import csv

from watchdog.observers import Observer
import watchdog.events

from csvparse import CSVParse

		
def watchPath(inputDir,outputDir,errorDir):
	# watches inputDir, write json to outputDir and errors to errorDir
	class fileWatcher(watchdog.events.FileSystemEventHandler):
		def dispatch(event):
			if event.event_type == 'created' and not event.is_directory:
				with open(event.src_path) as newFile:
					errors, output = CSVParse(newFile)
					filename = os.path.splitext(os.path.basename(event.src_path))[0]
					if  output != []:
						with open(outputDir+'/'+filename+'.json','w') as outputFile:
							json.dump(output,outputFile)
					if errors != []:
						with open(errorDir+'/'+filename+'.csv','w') as errorFile:
							writer = csv.writer(errorFile)
							writer.writerow([ 'LINE_NUM', 'ERROR_MSG' ])
							for row in errors:
								writer.writerow(row)
				os.remove(event.src_path)
						
	observer = Observer()
	observer.schedule(fileWatcher,inputDir)
	observer.start()
	try:
		while True:
			sleep(100)
	except KeyboardInterrupt:
		observer.stop()

		

if __name__ == '__main__':
	watchPath(argv[1],argv[2],argv[3])
