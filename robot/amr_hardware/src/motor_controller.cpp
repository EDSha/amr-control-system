#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

class MotorController : public rclcpp::Node
{
public:
    MotorController() : Node("motor_controller")
    {
        // Создаем publisher для команд моторам
        left_motor_pub_ = this->create_publisher<std_msgs::msg::Float64>("/left_motor/speed", 10);
        right_motor_pub_ = this->create_publisher<std_msgs::msg::Float64>("/right_motor/speed", 10);
        
        // Таймер для периодической отправки команд
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            [this]() { this->timer_callback(); });
            
        RCLCPP_INFO(this->get_logger(), "Motor controller node started");
    }

private:
    void timer_callback()
    {
        auto left_msg = std_msgs::msg::Float64();
        auto right_msg = std_msgs::msg::Float64();
        
        // Простейший тест: двигаем прямо
        left_msg.data = 0.5;  // 50% мощности
        right_msg.data = 0.5;
        
        left_motor_pub_->publish(left_msg);
        right_motor_pub_->publish(right_msg);
        
        RCLCPP_INFO(this->get_logger(), "Sending motor commands: L=%.1f, R=%.1f", 
                   left_msg.data, right_msg.data);
    }
    
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr left_motor_pub_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr right_motor_pub_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MotorController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
