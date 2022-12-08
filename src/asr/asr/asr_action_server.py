import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from action_asr.action import ASRaction

import speech_recognition as sr

class ASRActionServer(Node):

    # Creacion del nodo asr_action_server
    def __init__(self):
        super().__init__('asr_action_server')
        self._action_server = ActionServer(
            self,
            ASRaction,
            'asraction',
            execute_callback = self.execute_callback, 
            callback_group = ReentrantCallbackGroup(),
            goal_callback = self.goal_callback,
            cancel_callback = self.cancel_callback)


    # Callback a ejecutar en caso de pedir una meta
    def execute_callback(self, goal_handle):
        self.get_logger().info('Ejecutando escucha...')
        
        # Objeto del feedback de la accion
        feedback_msg = ASRaction.Feedback()

        r = sr.Recognizer()
        duracion = 5

        with sr.Microphone() as source:
            # Si se cancela el servicio
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Operacion cancelada')
                return ASRaction.Result()

            # read the audio data from the default microphone
            msg = "{Grabando...}"
            self.get_logger().info('Feedback: {0}'.format(msg))
            feedback_msg.feedback = msg
            goal_handle.publish_feedback(feedback_msg)
            audio_data = r.record(source, duration=duracion)

            # convert speech to text
            msg = "{Reconociendo...}"
            self.get_logger().info('Feedback: {0}'.format(msg))
            feedback_msg.feedback = msg
            goal_handle.publish_feedback(feedback_msg)
            text = r.recognize_google(audio_data, language="es-ES")
            

        # La meta se ha cumplido
        goal_handle.succeed()

        result = ASRaction.Result()
        result.resultado = text
        return result

    def destroy(self):
        self._action_server.destroy()
        super().destroy_node()

    def goal_callback(self, goal_request):
        self.get_logger().info('Recibida peticion de meta')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_request):
        self.get_logger().info('Recibida peticion de cancelacion')
        return CancelResponse.ACCEPT


def main(args=None):
    rclpy.init(args=args)
    print("ASR ACTION SERVER STARTED")

    asr_action_server = ASRActionServer()
    executor = MultiThreadedExecutor()

    try:
        rclpy.spin(asr_action_server, executor=executor)
    except KeyboardInterrupt:
        pass

    asr_action_server.destroy()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

