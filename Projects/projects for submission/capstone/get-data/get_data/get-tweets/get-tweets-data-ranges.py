# -*- coding: utf-8 -*-
import sys,getopt,codecs, time, random
from datetime import datetime, timedelta
import boto
import boto.s3
import os.path
import sys
import boto.ec2
import boto.utils
import got
from os import makedirs

def main(argv):

    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('exporter_help_text.txt', 'r')
        print f.read()querysearch
        f.close()
        return

    opts, args = getopt.getopt(argv, "", ("querysearch=", "days=","maxTweets=", "outputFile="))

    # setting default value for args
    max_tweets = 40000
    
    #used for when the data is writen to s3
    date_started = str(datetime.today().date())

    
    for opt,arg in opts:   
        if opt == '--querysearch':
            querysearch = arg
            # if output file is not specified it defualts to query search term, no error handling for special characters
            output_file = querysearch
        elif opt == '--days':
            days_raw = arg  
        elif opt == '--maxTweets':
            max_tweets=int(arg)
        elif opt == '--outputFile':
            output_file=arg

    #build days list
    days = days_raw.split(";")
          
    for start_date in days: 
        print("================================================")
        print("scrubbing: " + start_date)
        try:
            print("querysearch",querysearch)
            
            root = "/home/ec2-user/GetOldTweets-python/"
            folder = root + output_file + "/"
            
            makedirs(folder)
            
            outputFile = output_file + start_date + ".csv"
            full_path = folder + outputFile_dir

            print(folder)
            print(outputFile_dir)
            print(full_path)

            print("max tweets",max_tweets)

            tweetCriteria = got.manager.TweetCriteria()
            tweetCriteria.maxTweets = max_tweets
            tweetCriteria.querySearch = querysearch 
                
            # construct the days and then define the variables
            end_date = str((datetime.strptime(start_date,"%Y-%m-%d") + timedelta(1)).date())
           
            print("start_date",start_date)
            print("end_date",end_date)
 
            tweetCriteria.since = start_date
            tweetCriteria.until = end_date 
            
            attempt = 0 
            success = False
            while (success == False) & (attempt < 3):
                try:

                    outputFile = codecs.open(full_path, "w+", "utf-8")
        
                    outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
        
                    print('Searching...\n')
        
                    def receiveBuffer(tweets):
                        for t in tweets:
                            outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
                
                        outputFile.flush()
                        print('More %d saved on file...\n' % len(tweets))
                    
                    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
                    success = True
                except:
                    attempt += 1
                    print("ERROR: twitter error on since date" + start_date)
                    r = random.randint(1,60*10)
                    sleep_time = 60*20 + r
                    time.sleep(sleep_time)
                    success = False
                    outputFile.close()
    
        except arg:
            print('Arguments parser error, try -h' + arg)
        finally:
            outputFile.close()
            print('Done. Output file generated "%s".' % outputFileName)
            r = random.randint(1,60*10)
            #time.sleep(60 + r) 

    def move_to_s3(source_path="ethereum/",dest_path="ethereum/"):
        bucket_name = 'jeroens-bucket'

        # source directory
        sourceDir = source_path
        # destination directory name (on s3)
        destDir = dest_path

        #max size in bytes before uploading in parts. between 1 and 5 GB recommended
        MAX_SIZE = 20 * 1000 * 1000
        #size of parts when uploading in parts
        PART_SIZE = 6 * 1000 * 1000

        conn = boto.connect_s3()

        bucket = conn.get_bucket(bucket_name)

        uploadFileNames = []
        for (sourceDir, dirname, filename) in os.walk(sourceDir):
            uploadFileNames.extend(filename)
            break

        def percent_cb(complete, total):
            sys.stdout.write('.')
            sys.stdout.flush()

        for filename in uploadFileNames:
            sourcepath = os.path.join(sourceDir + filename)
            destpath = os.path.join(destDir, filename)
            print 'Uploading %s to Amazon S3 bucket %s' % \
                    (sourcepath, bucket_name)

            filesize = os.path.getsize(sourcepath)
            if filesize > MAX_SIZE:
                print "multipart upload"
                mp = bucket.initiate_multipart_upload(destpath)
                fp = open(sourcepath,'rb')
                fp_num = 0
                while (fp.tell() < filesize):
                    fp_num += 1
                    print "uploading part %i" %fp_num
                    mp.upload_part_from_file(fp, fp_num, cb=percent_cb, num_cb=10, size=PART_SIZE)

                mp.complete_upload()

            else:
                print "singlepart upload"
                k = boto.s3.key.Key(bucket)
                k.key = destpath
                k.set_contents_from_filename(sourcepath,
                     cb=percent_cb, num_cb=10)

   

    print("Finished Date Ranges")
    print("Starting move to S3")
    dest_path =  querysearch + "/" + date_started + "/"
    move_to_s3(source_path=folder,dest_path=dest_path)
    print("shutting down instance")

if __name__ == '__main__':
    main(sys.argv[1:])



