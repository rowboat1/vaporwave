def bezier_curve(P0, P1, P2, t):
    t_1 = 1 - t
    B_x = t_1**2 * P0[0] + 2 * t_1 * t * P1[0] + t**2 * P2[0]
    B_y = t_1**2 * P0[1] + 2 * t_1 * t * P1[1] + t**2 * P2[1]
    return B_x, B_y