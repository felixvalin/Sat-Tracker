import satgeometry as sg
import satnight as sn
import notify
# from time import time
import matplotlib.pyplot as plt
import numpy as np

"""
def update_world_map(graph, new_position):
    ra, dec = new_position
    graph.set_xdata(np.append(graph.get_xdata(), ra))
    graph.set_ydata(np.append(graph.get_ydata(), dec))
    plt.draw()
    plt.show()"""


def main(SAT_VISIBLE=False):
    """
    This is the master function of the program. It Loops
    indefinitely and always checks if the satellite is visible in Mode 1.
    Once the satellite becomes visible, it sends a notification
    and switches to Mode 2, where it waits until the
    becomes unobservable again. The outer while loop keeps alternating Modes 1 and 2.
    input: none
    output: none
    """
    SAT_VISIBLE = False
    sat_filename = "tle_thehumanitystar.txt"  # Would need to be changeable
    # sat_filename = "tle_iss.txt"  # Would need to be changeable
    print("Initializing coordinates...")
    while True:  # Loops indefinitely
        # Gathers TLE information
        sat_name, tle1, tle2 = sg.get_fromfile_TLE(sat_filename)
        TLE = [tle1, tle2]
        # Initiate plot
        # world_map, = plt.plot([], [])
        plt.figure()
        # plt.xlim(-180, 180)
        # plt.ylim(-90, 90)
        print("Following satellite...")
        while SAT_VISIBLE is False:  # Mode 1: Will switch once sat is visible
            # start_time = time()
            position, velocity = sg.get_sat_posvel_curr(TLE)
            ra, dec = sg.RA_DEC_from_position(position)
            # print(position)
            # Update satellite map
            # update_world_map(world_map, sg.RA_DEC_from_position(position))
            # print(ra, dec)
            plt.plot(ra, dec, 'k*')
            plt.pause(0.00005)

            if sg.is_observable(position) and sn.is_night():
                SAT_VISIBLE = 1
                notify.send_email(sat_name, sat_name+" is visible!", "felixantoinevalin@gmail.com")
                print(sat_name+" is visible!\nA notification has been sent.")
            # print("Time for 1 loop: {}".format(time()-start_time))

        while SAT_VISIBLE is True:  # Mode 2: Will reswitch once sat isn't visible
            position, velocity = sg.get_sat_posvel_curr(TLE)
            if not sg.is_observable(position) or not sn.is_night():
                SAT_VISIBLE = 0
                notify.send_email(sat_name, sat_name+" is no longer visible!", "felixantoinevalin@gmail.com")

    return


if __name__ == "__main__":
    main()
