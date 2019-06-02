"""
NCLCMAPS.py

Authors:
Bailey Swick (baswick@stcloudstate.edu)
Russell P. Manser (russell.p.manser@ttu.edu)

This library does the following:
- Defines all (or most) NCL color tables in the dict called colors
- Defines a handful of functions to manipulate those color tables for plotting
- Provides a way to save custom color maps for later use

August 2018
"""

import sys

import numpy as np
from matplotlib.colors import ListedColormap
import csv

from colormaps import colors

__all__ = ['nclcmaps']


#
# New API
#

def normalize(name, indices=None):
    """
    Normalize a set of 24-bit RGB triplets.

    Search the colors dictionary for the key matching name.

    Finds the colormap given by name in the colors dictionary in colormaps. The
    RGB triplets are normalized by finding the maximum RGB value in the triplet,
    and dividing all values by that maximum.

    Parameters
    ----------
    name : str
        Name of the colormap.
    indices : array-like of ints (optional)
        Indices of desired colors in the colormap. If None, the whole colormap is
        normalized and returned.

    Returns
    -------
    numpy.ndarray
        A Nx3 array of normalized RGB triplets.
    """
    # Check that name is a valid mapping
    if name not in colors:
        sys.stderr.write("\n*** Error: could not find name '{}' in colors".format(name))
        return None

    # Return the entire colormap
    if indices is None:
        colors_raw = colors[name]
    # Return the specified colors of the colormap
    else:
        # Account for inclusion of white and black in all colormaps (indices 0 and 1)
        colors_raw = [colors[name][element - 2] for element in indices]

    # Find maximum RGB value
    max_rgb = np.max(colors_raw)

    # Return the normalized colormap
    return (colors_raw / max_rgb)


def create(name, indices=None, reverse=False, save=False, path=None):
    """
    Create a custom colormap from a single existing colormap.

    Parameters
    ----------
    name : string
        Name of the colormap.
    indices : list of ints
        Indices of desired colors in colormap. Can be a range or discrete values.
    reverse : boolean
        Reverse the order of the colormap.
    save : boolean
        Save the colormap as a csv.
    path : string
        Path to save the colormap to. If None, save to the current working directory.

    Returns
    -------
    ListedColormap
        The custom colormap.
    """
    colors = normalize(name, indices)

    if reverse:
        colors = np.flip(colors, 0)

    if save:
        __save(colors, path)

    return ListedColormap(colors)


def create_from_multiple(names, indices, reverse=False, save=False, path=None):
    """
    Create a custom colormap from multiple existing colormap.

    Parameters
    ----------
    names : array-like of strings
        Names of the colormaps. Must be same length as indices.
    indices : nested list of ints
        Indices of colors in each respective colormap. Must be same length as names.
        Each list can be a range or discrete values.
    reverse : boolean
        Reverse the order of the colors or the combined colormap.
    save : boolean
        Save the colormap as a csv.
    path : string
        Path to save the colormap to. If None, save to the current working directory.

    Returns
    -------
    ListedColormap
        The custom colormap.
    """
    # Normalize the individual colormaps, then concatenate them
    colors_list = [normalize(names[i], indices[i]) for i in range(len(names))]
    colors = np.concatenate(colors_list)

    if reverse:
        colors = np.flip(colors, 0)

    if save:
        __save(colors, path)

    return ListedColormap(colors)


#
# Old API
#

def cmap(name, reverse=False, save=False, newName="newcmap"):
    """
    Select a colormap by name.

    Parameters
    ----------
    name : string
        Name of the NCL color table or matplotlib colormap.
    reverse : boolean (default: False)
        Reverse the direction of the colormap.
    save : boolean (default: False)
        Save the colormap as a csv file.
    newName : string (default: "newcmap")
        Name of the saved colormap

    Returns
    -------
    ListedColormap
        A ListedColormap object corresponding to the NCL color table or matplotlib
        colormap requested.
    """
    colors = normalize(name)

    if reverse:
        colors = np.flip(colors, 0)

    # Save the custom color map to nclcmaps/customMaps/
    if save:
        __save(colors, path)

    return ListedColormap(colors, name=name)


def cmapRange(name, start, finish=None, reverse=False, save=False, newName="newcmap"):
    """
    Select a range of colors from a colormap.

    Parameters
    ----------
    name : string
        Name of the NCL color table or matplotlib colormap.
    start : int
        Index of the first desired color.
    finish : int (default: None)
        Index of the last desired color. If None, the colormap will end at the last
        available color.
    reverse : boolean (default: False)
        Reverse the direction of the colormap.
    save : boolean (default: False)
        Save the colormap as a csv file.
    newName : string (default: "newcmap")
        Name of the saved colormap

    Returns
    -------
    ListedColormap
        A ListedColormap object corresponding to the segment of the NCL color table
        or matplotlib colormap requested.
    """
    if finish is None:
        finish = len(colors[name])
    indices = np.arange(start, finish)
    colors = normalize(name, indices)

    # Create a ListedColormap object of the range of values in the NCL color
    # table in reverse
    if reverse:
        colors = np.flip(colors, 0)

    # Save the custom color map to nclcmaps/customMaps/
    if save:
        __save(colors, path)

    return ListedColormap(colors, name=name)


def cmapDiscrete(name, indices, save=False, newName="newcmap", multi=False):
    """
    Select discrete colors from a colormap.

    Parameters
    ----------
    name : string
        Name of the NCL color table or matplotlib colormap.
    indices : list
        Desired elements of the colormap.
    save : boolean (default: False)
        Save the colormap as a csv file.
    newName : string (default: "newcmap")
        Name of the saved colormap
    multi : boolean (default: False)
        Return a colormap composed of multiple NCL or matplotlib colormaps. This
        flag is used by cmapMulti, and should not be called explicitly.

    Returns
    -------
    ListedColormap
        A ListedColormap object corresponding to the segment(s) of the requested colormap.
    """
    data = normalize(name, indices)

    # Save the custom color map to nclcmaps/customMaps/
    if save:
        __save(colors, path)

    # If cmapDiscrete is being called by cmapMulti, return the raw color table data
    if multi:
        return data

    # Otherwise, return a ListedColorMap object
    else:
        cmap = ListedColormap(data, name=name)
        return cmap


def cmapMulti(names, indicesList, save=False, newName="newcmap"):
    """
    Select discrete colors or ranges of colors from multiple colormaps.

    Parameters
    ----------
    names : array-like of strings
        Names of the colormaps to select from.
    indicesList : list of lists
        Indices of color(s) from each desired colormap.
    save : boolean (default: False)
        Save the colormap as a csv file.
    newName : string (default: "newcmap")
        Name of the saved colormap

    Returns
    -------
    ListedColormap
        A ListedColormap object corresponding to the segment(s) of the requested colormap(s).
    """
    colors_list = [normalize(names[i], indicesList[i]) for i in range(len(names))]
    data = np.concatenate(colors_list)

    # Save the custom color map to nclcmaps/customMaps/
    if save:
        __save(colors, path)

    # Return the ListedColormap corresponding to the combined color tables
    cmap = ListedColormap(data)
    return cmap


def __save(colors, path=None):
    """
    Save a custom colormap to csv.

    Parameters
    ----------
    colors : arrays of arrays
        Array of normalized RGB triplets composing the new colormap.
    path : string or None
        Path to save the colormap csv to. If None, save it in the current working
        directory as newmap.csv.

    Returns
    -------
    None
    """
    # Write to the specified path or the current working directory
    if path is None:
        path = "./newmap.csv"

    customMap = open(path, "w")
    # Write each rgb triplet to a new line
    for item in range(0, len(colors)):

        i = 0
        while i < 3:
            # normalize the rgb value to a string
            rgb = str(colors[item][i])

            # Write value to file and separate with a comma
            if i != 2:
                customMap.write(rgb + ",")

            # Separate triplets with a line break
            else:
                customMap.write(rgb + "\n")
            i += 1

    customMap.close()


def load(path):
    """
    Load a custom colormap from csv.

    Parameters
    ----------
    path : string
        Path to the colormap csv file.

    Returns
    -------
    ListedColormap
        The requested custom colormap.
    """
    # Open the file
    try:
        customMap = open(path, "r")
    except(FileNotFoundError, IOError):
        sys.stderr.write("Could not open file {}".format(path))

    # List for the full color map
    data = []

    # Read the opened file as a CSV
    readCSV = csv.reader(customMap, delimiter=",")

    for row in readCSV:
        # Temp array for the rgb triplet on each line
        temp = [-1, -1, -1]

        # Assign the rgb triplet to temp
        temp[0] = float(row[0])
        temp[1] = float(row[1])
        temp[2] = float(row[2])

        data.append(temp)

    customMap.close()

    cmap = ListedColormap(data)
    return cmap
