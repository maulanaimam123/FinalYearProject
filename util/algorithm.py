# python function to calculate beam diameter
# given the line profile
import math

def calculate_beam_diameter(int_arr, line_coords, img_w = 9999, img_h = 9999):
    '''
    This algorithm estimates the beam diameter of a steep profile
    given the array of intensity and location.
    parameter:
    - int_arr : array of intensity (int 0-255)
    - loc_arr : array of location (int x, int y)
    output:
    - FWHM (full width at half maximum): float
    '''
    # Calculate the second derivation of 
    first_derivative = [int(val) - int(prev_val) for val, prev_val in zip(int_arr[1:], int_arr[:-1])]
    max_intensity = max(first_derivative)
    max_index = first_derivative.index(max_intensity)

    # Cleaning the first derivate graph
    for i, n in enumerate(first_derivative):
        if i - max_index > 0.15 * len(first_derivative):
            first_derivative[i] = 0

    # Finding the half-max-intensity points
    start_point = max_index
    end_point = max_index

    for i in range(1, max_index - 1):
        if first_derivative[i] > 0.5 * max_intensity and first_derivative[i - 1] < 0.5 * max_intensity:
            start_point = i - 1
            break

    for i in range(len(first_derivative) - 1, max_index, -1):
        if first_derivative[i] > 0.5 * max_intensity and first_derivative[i + 1] < 0.5 * max_intensity:
            end_point = i + 1
            break

    # Calculate the FWHM
    start, end = line_coords
    x0, y0 = max(start.x(), 0), max(start.y(), 0)
    x1, y1 = min(end.x(), img_w), min(end.y(), img_h)

    actual_length = math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    FWHM = int((end_point - start_point) / len(first_derivative) * actual_length)

    return FWHM, first_derivative