#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

class CmdVelConverter(Node):
    def __init__(self):
        super().__init__('cmd_vel_converter')
        self.sub_left = self.create_subscription(Float64, '/left_motor/cmd', self.left_callback, 10)
        self.sub_right = self.create_subscription(Float64, '/right_motor/cmd', self.right_callback, 10)
        self.pub_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        self.left = 0.0
        self.right = 0.0
        # Период 0.05 с = 20 Гц
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.get_logger().info('CmdVelConverter started')

    def left_callback(self, msg):
        self.left = msg.data

    def right_callback(self, msg):
        self.right = msg.data

    def timer_callback(self):
        wheelbase = 0.35  # расстояние между колёсами (метры) – должно совпадать с wheel_separation в URDF
        linear = (self.left + self.right) / 2.0
        angular = (self.right - self.left) / wheelbase
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.pub_cmd_vel.publish(twist)
        # Раскомментируйте следующую строку для отладки:
        # self.get_logger().info(f'cmd_vel: linear={linear:.2f}, angular={angular:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelConverter()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
