#! /usr/bin/env python

import rospy
import yaml
import sys

import actionlib
import strands_tweets.msg
#import ros_mary_tts.srv 
from marathon_reporter.msg import MarathonSession


class  marathon_achievements():

    def __init__(self, filename):
        rospy.loginfo("Loading Achievements ...")
        text_file = open(filename, "r")      
        texts = yaml.load(text_file)
        
        rospy.loginfo("Loading Publishing Actions ...")
        self.client = actionlib.SimpleActionClient('strands_tweets', strands_tweets.msg.SendTweetAction)        
        
        self.last_time_reported=0
        self.time_ach_list = texts["achievements"]["run_duration"]
        self.time_ach_pend = True        
                
        self.dist_ach_list = texts["achievements"]["distance"]
        self.last_dist_reported=0
        self.dist_ach_pend = True

        self.last_sec_rec = 0

        rospy.loginfo("Setting new start ...")
        self.fresh_start=True

        rospy.loginfo("Subscribing to Marathon Session ...")
        rospy.Subscriber("/current_marathon_session", MarathonSession, self.report_callback)

        rospy.loginfo("Init Done ...")


    def report_callback(self, msg):
        if msg.duration.secs - self.last_sec_rec > 5: #Only check every five seconds
            self.last_sec_rec = msg.duration.secs
        
            hours = msg.duration.secs/3600
            distance = msg.distance/1000
    
            if self.fresh_start:
                if msg.duration.secs > 300:
                    rospy.loginfo("This is an old marathon discarding all previous achievements")
                    for i in range(0, len(self.time_ach_list)-1):
                        if hours >= self.time_ach_list[i]["val"]:
                           self.last_time_reported+=1
                           rospy.loginfo("discarding time achievement number %d" %i)
                        else:
                            break
                    if self.last_time_reported >= len(self.time_ach_list):
                        rospy.loginfo("All time achievements complete")
                        self.time_ach_pend=False
                        
                    for i in range(0, len(self.dist_ach_list)-1):
                        if distance >= self.dist_ach_list[i]["val"]:
                           self.last_dist_reported+=1
                           rospy.loginfo("discarding distance achievement number %d" %i)
                        else:
                            break
                        
                    if self.last_dist_reported >= len(self.dist_ach_list):
                        rospy.loginfo("All distance achievements complete")
                        self.dist_ach_pend=False
                self.fresh_start=False
                
            if self.time_ach_pend :
                if hours >= self.time_ach_list[self.last_time_reported]["val"] :
                    text = self.time_ach_list[self.last_time_reported]["achievement"]
                    print "%s (%f) [%f]" %(text, self.time_ach_list[self.last_time_reported]["val"], float(msg.duration.secs))
                    self.send_tweet(text)
    
                    if self.last_time_reported < len(self.time_ach_list)-1:
                        self.last_time_reported+=1
                    else:
                        self.time_ach_pend=False
            
            
            if self.dist_ach_pend :
                if distance >= self.dist_ach_list[self.last_dist_reported]["val"]:
                    text = self.dist_ach_list[self.last_dist_reported]["achievement"]
                    print "%s (%f) [%f]" %(text, self.dist_ach_list[self.last_dist_reported]["val"], float(msg.distance))
                    self.send_tweet(text)
    
                    if self.last_dist_reported < len(self.dist_ach_list)-1 :
                        self.last_dist_reported+=1
                    else:
                        self.dist_ach_pend=False



    def send_tweet(self, text):
        tweetgoal = strands_tweets.msg.SendTweetGoal()
        tweetgoal.text = text
        tweetgoal.with_photo = False
        self.client.send_goal(tweetgoal)            
        self.client.wait_for_result()
        ps = self.client.get_result()
        print ps



if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print "usage: rosrun marathon_achievements achievement_monitor.py achievements_file.yaml"
        sys.exit(2)

    filename=str(sys.argv[1])
    
    rospy.init_node("achievement_monitor")
    ps = marathon_achievements(filename)
    rospy.spin()
