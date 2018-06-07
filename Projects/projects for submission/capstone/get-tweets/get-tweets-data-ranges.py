# -*- coding: utf-8 -*-
# use somthing like: python get-tweets-data-ranges.py --querysearch "etherium" --days "2017-06-02;2017-06-03"

import sys,getopt,codecs, time, random
from datetime import datetime, timedelta
import boto
import boto.s3

import os.path
import sys

import got

def main(argv):

    if len(argv) == 0:
        print('You must pass some parameters. Use \"-h\" to help.')
        return

    if len(argv) == 1 and argv[0] == '-h':
        f = open('exporter_help_text.txt', 'r')
        print f.read()
        f.close()
        return

    opts, args = getopt.getopt(argv, "", ("querysearch=", "days="))


    #outputFileName = "output_got.csv"


    for opt,arg in opts:

        if opt == '--querysearch':
            querysearch = arg

        elif opt == '--days':
            days_raw = arg
    #build days list
    days = days_raw.split(";")

    for start_date in days:
        print("================================================")
        print("scrubbing: " + start_date)
        try:
            tweetCriteria = got.manager.TweetCriteria()
            tweetCriteria.maxTweets = 1000
            tweetCriteria.querySearch = querysearch

            # construct the days and then define the variables
            end_date = str((datetime.strptime(start_date,"%Y-%m-%d") + timedelta(1)).date())

            tweetCriteria.since = start_date
            tweetCriteria.until = end_date

            folder = querysearch + "/"
            outputFileName = querysearch + start_date + ".csv"

            outputFile = codecs.open(folder + outputFileName, "w+", "utf-8")

            outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')

            print('Searching...\n')
            def receiveBuffer(tweets):
                for t in tweets:
                    outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))

                outputFile.flush()
                print('More %d saved on file...\n' % len(tweets))

            success = False
            while success == False:
                try:
                    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
                    success = True
                except:
                    print("ERROR: twitter error on since date" + start_date)
                    time.sleep(60*20)
                    success = False

        except arg:
            print('Arguments parser error, try -h' + arg)
        finally:
            outputFile.close()
            print('Done. Output file generated "%s".' % outputFileName)
            r = random.randint(1,60*10)
            #time.sleep(60 + r)

    def move_to_s3(path="etherium/"):
        bucket_name = 'jeroens-bucket'

        # source directory
        sourceDir = path
        # destination directory name (on s3)
        destDir = ''

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
    move_to_s3(path=folder)


if __name__ == '__main__':
    main(sys.argv[1:])


