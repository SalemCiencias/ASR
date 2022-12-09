import rclpy
from rclpy.node import Node

from kobuki_ros_interfaces.msg import BumperEvent

from std_msgs.msg import String

from escucha.cliente_escucha import ASRActionClient


class NodoEscucha(Node):

    def __init__(self):
        super().__init__('escucha_boton')
        self.subscription = self.create_subscription(
            BumperEvent,
            '/events/bumper',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.cliente = ASRActionClient();


    def listener_callback(self, msg):
        print('Boton presionado, cliente con goal 0')
        self.get_logger().info('I heard: "%s"' % msg)
        self.cliente.send_goal(0);
        rclpy.spin(self.cliente)


def main(args=None):
    print('desde nodo_escucha')
    rclpy.init(args=args)

    minimal_subscriber = NodoEscucha()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

