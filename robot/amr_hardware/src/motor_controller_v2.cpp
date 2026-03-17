#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"
#include "robot_control/msg/robot_status.hpp"  // наше кастомное сообщение

class MotorControllerV2 : public rclcpp::Node
{
public:
    MotorControllerV2() : Node("motor_controller_v2")
    {
        // Publishers for motor speeds (как было)
        left_motor_pub_ = this->create_publisher<std_msgs::msg::Float64>("/left_motor/speed", 10);
        right_motor_pub_ = this->create_publisher<std_msgs::msg::Float64>("/right_motor/speed", 10);
        
        // NEW: Publisher for robot status
        status_pub_ = this->create_publisher<robot_control::msg::RobotStatus>("/robot_status", 10);
        
        // Subscribers for motor commands (как было)
        left_cmd_sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/left_motor/cmd", 10,
            [this](const std_msgs::msg::Float64::SharedPtr msg) {
                left_command_ = msg->data;
                RCLCPP_INFO(this->get_logger(), "FMS → Left: %.2f", msg->data);
            });
            
        right_cmd_sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/right_motor/cmd", 10,
            [this](const std_msgs::msg::Float64::SharedPtr msg) {
                right_command_ = msg->data;
                RCLCPP_INFO(this->get_logger(), "FMS → Right: %.2f", msg->data);
            });
        
        // Timer for motor control (как было, 100ms)
        motor_timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            [this]() { this->motor_timer_callback(); });
        
        // NEW: Timer for status publishing (1 second)
        status_timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            [this]() { this->status_timer_callback(); });
            
        RCLCPP_INFO(this->get_logger(), "🤖 Motor Controller v2 started");
        RCLCPP_INFO(this->get_logger(), "📊 Publishing status every 1 second");
    }

private:
    void motor_timer_callback()
    {
        // Публикуем текущие скорости моторов (как было)
        auto left_msg = std_msgs::msg::Float64();
        auto right_msg = std_msgs::msg::Float64();
        
        left_msg.data = left_command_;
        right_msg.data = right_command_;
        
        left_motor_pub_->publish(left_msg);
        right_motor_pub_->publish(right_msg);
        
        RCLCPP_INFO(this->get_logger(), "📤 Motors: L=%.2f, R=%.2f", 
                   left_msg.data, right_msg.data);
    }
    
    void status_timer_callback()
    {
        // NEW: Формируем и публикуем статус робота
        auto status_msg = robot_control::msg::RobotStatus();
        
        // Заполняем поля
        status_msg.robot_id = "telezhka_001";
        status_msg.battery = 85.0;  // Пока константа, позже сделаем динамической
        status_msg.x = 0.0;          // Позиция X
        status_msg.y = 0.0;          // Позиция Y
        status_msg.current_task = "moving";
        status_msg.stamp = this->get_clock()->now();  // Текущее время
        
        // Публикуем
        status_pub_->publish(status_msg);
        
        RCLCPP_INFO(this->get_logger(), "📊 Status: bat=%.1f%%, pos=(%.1f,%.1f), task=%s",
                   status_msg.battery,
                   status_msg.x,
                   status_msg.y,
                   status_msg.current_task.c_str());
    }
    
    // Publishers
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr left_motor_pub_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr right_motor_pub_;
    rclcpp::Publisher<robot_control::msg::RobotStatus>::SharedPtr status_pub_;
    
    // Subscribers
    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr left_cmd_sub_;
    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr right_cmd_sub_;
    
    // Timers
    rclcpp::TimerBase::SharedPtr motor_timer_;
    rclcpp::TimerBase::SharedPtr status_timer_;
    
    // Commands
    double left_command_ = 0.0;
    double right_command_ = 0.0;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MotorControllerV2>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}