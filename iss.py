#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ISS Location.

This program retrieves the current astronauts aboard the ISS, the location
of the ISS, graphing the ISS location on a world map, and the next time
the ISS will be overhead Indianapolis.

author = Aaron Jackson
Github = TimeApollo
"""
import requests
import ast
import time
import turtle

__author__ = 'Aaron Jackson'


# Part A
def iss_astronauts():
    """Prints the full names, number, and spacecraft of astronauts in ISS."""
    astronauts_api = 'http://api.open-notify.org/astros.json'
    astro_data = requests.get(astronauts_api)
    astro_data = ast.literal_eval(astro_data.content)

    print('\nAstronauts in space')
    print('Full Name and Craft Currently On')

    for data in astro_data['people']:
        print('{} {}'.format(data['name'], data['craft']))

    print('There is a current total of {} astronauts in space'
          .format(str(astro_data['number'])))


# Part B
def iss_location():
    """Prints the geographical location of the ISS and current timestamp."""
    iss_location_api = 'http://api.open-notify.org/iss-now.json'
    iss_loc = requests.get(iss_location_api)
    iss_loc = ast.literal_eval(iss_loc.content)
    print('\nCurrent Location of ISS and Current Timestamp')
    print('Latitude: {}'.format(iss_loc['iss_position']['latitude']))
    print('Longitude: {}'.format(iss_loc['iss_position']['longitude']))
    print('TimeStamp: {}\n'.format(time.ctime(int(iss_loc['timestamp']))))
    return iss_loc['iss_position']


# Part C
def iss_graph(loc):
    """Makes graphic screen showing current location of ISS."""
    # setup screen size to size of image
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.title('ISS location. (click screen to exit)')

    # initiate canvas for turtle to be drawn on
    iss = turtle.Turtle()
    iss_img = 'iss.gif'

    # setup the background
    iss_bg = iss.getscreen()  # get screen that is being drawn on
    iss_bg.bgpic('map.gif')  # set background image
    iss_bg.setworldcoordinates(-180, -90, 180, 90)  # set coordinates
    iss_bg.addshape(iss_img)

    # setup the iss image
    iss.hideturtle()
    latitude = float(loc['latitude'])
    longitude = float(loc['longitude'])
    iss.shape(iss_img)
    iss.penup()
    iss.setpos(longitude, latitude)
    iss.showturtle()

    # return canvas to be used in next part
    return iss


# Part D
def iss_intercepts_indy(iss):
    """Plots Indy's Location and shows next ISS fly over time."""
    iss_pass_api = 'http://api.open-notify.org/iss-pass.json'
    indy_lat = 39.76843
    indy_long = -86.1581
    query_data = {'lat': indy_lat, 'lon': indy_long}
    iss_pass_data = requests.get(iss_pass_api, params=query_data)
    pass_time = ast.literal_eval(iss_pass_data.content)['response'][1]['risetime']
    formatted_pass_time = time.ctime(pass_time)

    # Draw Indy dot
    indy = turtle.Turtle()
    indy.hideturtle()
    indy.penup()
    indy.setpos(indy_long, indy_lat)
    indy.dot(10, 'yellow')
    indy.write(formatted_pass_time, align='center')
    # indy.showturtle() commented out to not show arrow.


def main():
    """ISS Location Implementation."""
    iss_astronauts()
    iss_loc = iss_location()
    iss = iss_graph(iss_loc)
    iss_intercepts_indy(iss)

    # call to allow the graphic to be seen until it is clicked
    turtle.exitonclick()


if __name__ == "__main__":
    main()
