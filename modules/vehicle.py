from math import degrees, atan2

from mathutils import Vector, Quaternion


class Vehicle:
    def __init__(self, back, up, front):
        self.back = back
        self.up = up
        self.front = front
        self.forward = (front - back).normalized()
        self.upward = (up - back).normalized()

    def roll_degrees(self):
        angle = self._new_vehicle_with_roll_only()._roll_angle()
        angle_deg = 90 - degrees(angle)
        if angle_deg < 0:
            return 360 + angle_deg
        else:
            return angle_deg

    def _new_vehicle_without_yaw(self):
        remove_yaw = self._yaw_quaternion()
        new_forward = remove_yaw @ self.forward
        new_upward = remove_yaw @ self.upward
        return Vehicle(Vector((0, 0, 0)), new_upward, new_forward)

    def _yaw_quaternion(self):
        z_axis = Vector((0, 0, 1))
        rise = self.forward.y
        run = self.forward.x
        angle = atan2(rise, run)
        remove_yaw = Quaternion(z_axis, -angle)
        return remove_yaw

    def _new_vehicle_without_pitch(self):
        remove_pitch = self._pitch_quaternion()
        new_forward = remove_pitch @ self.forward
        new_upward = remove_pitch @ self.upward
        return Vehicle(Vector((0, 0, 0)), new_upward, new_forward)

    def _pitch_quaternion(self):
        """
        Only valid when applied to a vehicle whose yaw is already removed.
        I cannot explain this but I can demonstrate it. - JR
        :return:
        """
        y_axis = Vector((0, 1, 0))
        rise = self.forward.z
        run = self.forward.x
        angle = atan2(rise, run)
        remove_pitch = Quaternion(y_axis, angle)
        return remove_pitch

    def _new_vehicle_with_roll_only(self):
        """
        Note that the rotations have to be applied in order, one after the other.
        Computing both quaternions at the beginning will not work.
        """
        return self._new_vehicle_without_yaw()._new_vehicle_without_pitch()

    def _roll_angle(self):
        return atan2(self.upward.z, self.upward.y)
