import satgeometry as sg
import satnight as sn
import notify


def main(SAT_VISIBLE=False):
    sat_filename = "tle_thehumanitystar.txt"
    print("Initializing coordinates...")
    while True:  # Loops indefinitely
        sat_name, tle1, tle2 = sg.get_fromfile_TLE(sat_filename)
        TLE = [tle1, tle2]
        print("Following satellite...")
        while SAT_VISIBLE is False:  # Will switch once sat is visible
            position, velocity = sg.get_sat_posvel_curr(TLE)
            if sg.is_observable(position) and sn.is_night():
                SAT_VISIBLE = 1
                notify.send_email(sat_name, sat_name+" is visible!", "felixantoinevalin@gmail.com")
                print(sat_name+" is visible!\nA notification has been sent.")

        while SAT_VISIBLE is True:  # Will reswitch once sat isn't visible
            position, velocity = sg.get_sat_posvel_curr(TLE)
            if not sg.is_observable(position) or not sn.is_night():
                SAT_VISIBLE = 0
                notify.send_email(sat_name, sat_name+" is no longer visible!", "felixantoinevalin@gmail.com")

    return


if __name__ == "__main__":
    main()
