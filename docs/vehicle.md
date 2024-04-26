    """
    Vehicle class represents a vehicle solely in terms of its
    forward direction and upward direction, both normalized.
    Normal creation is by providing the vectors
    back - world position of rear
    up - world position of top of tail of vehicle
    front = world position of front of vehicle

    given an export from blender:

    u
    |\
    | \
    |  \
    b---f

    Theory of Operation:

    The private methods `_new_vehicle_without_yaw` and `_new_vehicle_without_pitch`
    return, well, a new vehicle, derived from the receiver, with yaw or pitch removed.
    Both these methods create a Quaternion with the appropriate rotation and apply it
    to the receiver's forward and upward to get the values for a new vehicle with
    yaw or pitch removed.

    The private method `_new_vehicle_with_roll_only` returns a vehicle
    with both yaw and pitch removed.

    The public method `roll_degrees` returns the desired roll angle, counterclockwise from vertical.
    `roll_degrees` uses the private method `roll_angle` which returns the arc-tangent
    of the receiver's upward.z and upward.y.

    `roll_degrees` returns 90 degrees minus the roll_angle of the vehicle with roll only,
    because that's the counterclockwise angle from vertical.
    (That is, it's adjusted to be what I think we want. We can adjust differently if need be.)

    Internally the sequence of operation is:
    1. Create the vehicle from input
    2. Ask it for roll_degrees, which will
    3. Transform the original to one without yaw
    4. Transform the yaw-less one to one also without pitch
    5. Ask that one for roll_angle
    6. Convert and return the desired angle in degrees

    This may seem odd. The idea is to have the Vehicle object be immutable:
    Once created, a Vehicle never changes. Instead, we get a new one that
    has been adjusted for no yaw or no pitch. This is thought by the people
    who think things to be a good way to design objects, so that they never change.

    Note:
        Because the vehicle is just represented by its forward and upward
        direction vectors, we can create a new one with desired forward and upward
        by Vehicle(zero_vector, upward, forward). The __init__ just works out to
        retain the provided upward and forward. Nifty, once you get over it.

    Note:
        For reasons that I cannot quite explain, the yaw removal uses the
        negative of the arc-tangent, and the pitch uses the positive.
        This is what it took to make it work. I cannot quite visualize why.
        (Later: I think it has to do with whether Y goes into the screen or out.)

    Note:
        I'm going to put the back, up, front members back into the class.
        I want them for better testing. JR: 2023-10-21

    Note:
        I'm going to extract methods to get the two desired quaternions, for two reasons:
        First, because I want to use them in my program that draws the pictures.
        Second, because the methods that create them have kind of a two-phase aspect,
        creating the quaternion and then applying it. Creating with a separate method
        will express that duality better. JR: 2023-10-21
    """