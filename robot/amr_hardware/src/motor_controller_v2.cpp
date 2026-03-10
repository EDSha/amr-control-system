#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

class MotorController : public rclcpp::Node
{
public:
    MotorController() : Node("motor_controller_v2")
    {
        // Публикация текущих скоростей (как раньше)
        left_motor_pub_ = this->create_publisher<std_msgs::msg::Float64>("/left_motor/speed", 10);
        right_motor_pub_ = this->create_publisher<std_msgs::msg::Float64>("/right_motor/speed", 10);
        
        // Подписка на команды от FMS (через мост)
        left_cmd_sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/left_motor/cmd", 10,
            [this](const std_msgs::msg::Float64::SharedPtr msg) {
                this->left_command_ = msg->data;
                RCLCPP_INFO(this->get_logger(), "FMS → Left: %.2f", msg->data);
            });
            
        right_cmd_sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/right_motor/cmd", 10,
            [this](const std_msgs::msg::Float64::SharedPtr msg) {
                this->right_command_ = msg->data;
                RCLCPP_INFO(this->get_logger(), "FMS → Right: %.2f", msg->data);
            });
        
        // Таймер для имитации работы моторов
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            [this]() { this->timer_callback(); });
            
        RCLCPP_INFO(this->get_logger(), "🤖 Motor Controller v2 started");
        RCLCPP_INFO(this->get_logger(), "Waiting for FMS commands...");
    }

private:
    void timer_callback()
    {
        auto left_msg = std_msgs::msg::Float64();
        auto right_msg = std_msgs::msg::Float64();
        
        // Используем команды от FMS (если есть) или значения по умолчанию
        left_msg.data = left_command_;
        right_msg.data = right_command_;
        
        left_motor_pub_->publish(left_msg);
        right_motor_pub_->publish(right_msg);
        
        RCLCPP_INFO(this->get_logger(), "📤 Motors: L=%.2f, R=%.2f", 
                   left_msg.data, right_msg.data);
    }
    
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr left_motor_pub_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr right_motor_pub_;
    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr left_cmd_sub_;
    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr right_cmd_sub_;
    
    // Текущие команды от FMS
    double left_command_ = 0.0;
    double right_command_ = 0.0;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MotorController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
