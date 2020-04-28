from djitellopy import Tello
import pygame
from threading import Thread


class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D (Q and D in azerty mode): Counter clockwise and clockwise rotations
            - W and S (Z and S in azerty mode): Up and down.
    """

    def __init__(self, drone_speed, azerty, frame_processor):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        self.drone_speed = drone_speed
        if azerty:  # use variables to store the values of the non constant keys
            self.counter_clk_rot_key = pygame.K_q
            self.move_up_key = pygame.K_z
        else:
            self.counter_clk_rot_key = pygame.K_a
            self.move_up_key = pygame.K_w

        self.tello = Tello()
        self.frame_processor = frame_processor
        self.frame_processed = False
        self.should_stop = False

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)

    def run(self):
        """check if some commands work and then launches the main control loop"""

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(10):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

        # must be done in another thread to avoid fucking up commands reactivity
        Thread(target=self.start_processing_frames, args=()).start()

        while not self.should_stop:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    self.should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            # if we are still processing our frame, we don't refresh the screen
            if self.frame_processed:
                self.screen.fill([0, 0, 0])
                frame = pygame.surfarray.make_surface(self.frame_processor.out_frame)
                self.screen.blit(frame, (0, 0))
                pygame.display.update()
                self.frame_processed = False

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def start_processing_frames(self):
        """processes frames"""
        frame_read = self.tello.get_frame_read()

        while not self.should_stop:
            if frame_read.stopped:
                frame_read.stop()
                self.should_stop = True

            self.frame_processor.process(frame_read.frame)
            self.frame_processed = True

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = self.drone_speed
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -self.drone_speed
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -self.drone_speed
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = self.drone_speed
        elif key == self.move_up_key:  # set up velocity
            self.up_down_velocity = self.drone_speed
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -self.drone_speed
        elif key == self.counter_clk_rot_key:  # set yaw counter clockwise velocity
            self.yaw_velocity = -self.drone_speed
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = self.drone_speed

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == self.move_up_key or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == self.counter_clk_rot_key or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)