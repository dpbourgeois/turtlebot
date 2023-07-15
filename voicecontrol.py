import rospy
import speech_recognition as sr
from geometry_msgs.msg import Twist

class VoiceControl():
    def __init__(self):
        # initiliaze
        rospy.init_node('VoiceControl', anonymous=False)

    	# tell user how to stop TurtleBot
    	rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
	    # Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
     
    	#TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        rate = rospy.Rate(10);

        # Twist is a datatype for velocity
        move_cmd = Twist()

    	# let's go forward at 0.2 m/s
        move_cmd.linear.x = 0
    	# let's turn at 0 radians/s
    	move_cmd.angular.z = 0

    	# as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
	    print('flag1')
            speech = getSpeech()
	    print('flag2')
            if speech == 'go':
                move_cmd.linear.x = checkLinearLimitVelocity(move_cmd.linear.x + 0.01)
            elif speech == 'back':
                move_cmd.linear.x = checkLinearLimitVelocity(move_cmd.linear.x - 0.01)
            elif speech == 'left':
                move_cmd.angular.z = checkAngularLimitVelocity(move_cmd.angular.z + 0.1)
            elif speech == 'right':
                move_cmd.angular.z = checkAngularLimitVelocity(move_cmd.angular.z - 0.01)
            elif speech == 'stop':
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = 0.0
    	    
            # publish the velocity
            self.cmd_vel.publish(move_cmd)
    	    # wait for 0.1 seconds (10 HZ) and publish again
            rate.sleep()
                   
    def getSpeech():
	r = sr.Recognizer()
        with sr.Microphone() as source:
            speech = ''                
            audio = r.listen(source)                   
            try:
                speech = r.recognize(audio)
                speech = speech.lower()   
            except LookupError:                            
                speech = ''
            return speech

    def constrain(input, low, high):
        if input < low:
          input = low
        elif input > high:
          input = high
        else:
          input = input

        return input

    def checkLinearLimitVelocity(vel):
        vel = constrain(vel, -0.22, 0.22)
        return vel
    
    def checkAngularLimitVelocity(vel):
        vel = constrain(vel, -2.84, 2.84)
        return vel
        
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	# a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	# sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
	print('flag1')
        VoiceControl()
    except:
        rospy.loginfo("VoiceControl node terminated.")
