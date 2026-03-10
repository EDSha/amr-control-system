// Узел для прослушивания команд моторам
// Подписывается на топики и выводит полученные значения

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"  // тип сообщения для чисел с плавающей точкой

class MotorListener : public rclcpp::Node {
public:
    MotorListener() : Node("motor_listener") {
        // Подписка на топик левого мотора
        left_sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/left_motor/speed",  // имя топика
            10,  // глубина очереди
            // Лямбда-функция, вызываемая при получении сообщения
            [this](const std_msgs::msg::Float64::SharedPtr msg) {
                RCLCPP_INFO(this->get_logger(), "Left motor: %.2f", msg->data);
            });
            
        // Подписка на топик правого мотора
        right_sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/right_motor/speed", 10,
            [this](const std_msgs::msg::Float64::SharedPtr msg) {
                RCLCPP_INFO(this->get_logger(), "Right motor: %.2f", msg->data);
            });
            
        RCLCPP_INFO(this->get_logger(), "Motor listener started");
    }

private:
    // Указатели на подписки
    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr left_sub_;
    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr right_sub_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);  // инициализация ROS
    auto node = std::make_shared<MotorListener>();  // создание узла
    rclcpp::spin(node);  // основной цикл обработки
    rclcpp::shutdown();  // завершение работы
    return 0;
}
