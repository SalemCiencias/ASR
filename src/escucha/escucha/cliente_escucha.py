from action_asr.action import ASRaction

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from std_msgs.msg import String

class ASRActionClient(Node):

    def __init__(self):
        super().__init__('asr_action_client')
        self._action_client = ActionClient(self, ASRaction, 'asraction')

        nodo = rclpy.create_node("habla_texto")
        self.publisher = nodo.create_publisher(String, '/texto/habla', 10)

    def send_goal(self, orden):
        goal_msg = ASRaction.Goal()
        goal_msg.orden = orden

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()

        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result()
        self.get_logger().info('Result: {0}'.format(result))

        publisher.publish(result)

        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback))


def main(args=None):
    print('iniciado cliente escucha')
    rclpy.init(args=args)

    action_client = ASRActionClient()

    action_client.send_goal(0)

    rclpy.spin(action_client)


if __name__ == '__main__':
    main()

