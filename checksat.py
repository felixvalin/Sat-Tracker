import satgeometry as sg
import satnight as sn
import notify


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

    sat_filename = "tle_thehumanitystar.txt"  # Would need to be changeable
    print("Initializing coordinates...")
    while True:  # Loops indefinitely
        # Gathers TLE information
        sat_name, tle1, tle2 = sg.get_fromfile_TLE(sat_filename)
        TLE = [tle1, tle2]
        print("Following satellite...")
        while SAT_VISIBLE is False:  # Mode 1: Will switch once sat is visible
            position, velocity = sg.get_sat_posvel_curr(TLE)
            if sg.is_observable(position) and sn.is_night():
                SAT_VISIBLE = 1
                notify.send_email(sat_name, sat_name+" is visible!", "felixantoinevalin@gmail.com")
                print(sat_name+" is visible!\nA notification has been sent.")

        while SAT_VISIBLE is True:  # Mode 2: Will reswitch once sat isn't visible
            position, velocity = sg.get_sat_posvel_curr(TLE)
            if not sg.is_observable(position) or not sn.is_night():
                SAT_VISIBLE = 0
                notify.send_email(sat_name, sat_name+" is no longer visible!", "felixantoinevalin@gmail.com")

    return


if __name__ == "__main__":
    main()
