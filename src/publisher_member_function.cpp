#include <chrono>     //时间相关头文件
#include <functional> //std::bind
#include <memory>     //智能指针头文件
#include <string>
#include "rclcpp/rclcpp.hpp"       //ros2核心头文件
#include "std_msgs/msg/string.hpp" //消息类型
#include "geometry_msgs/msg/twist.hpp"

using namespace std::chrono_literals; // 引入时间字面量

class MinimalPublisher : public rclcpp::Node // 创建类并公共继承Node类
{
public:
  // 通过初始化列表初始化基类成名和派生类成员，并把节点的名称设置为 minimal_publisher
  MinimalPublisher()
      : Node("minimal_publisher"), count_(0)
  {
    // 创建一个发布者，消息类型为std_msgs::msg::String，话题为"topic"，队列大小是10
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    // 创建一个定时器，间隔为500ms 回调函数为MinimalPublisher::timer_callback
    timer_ = this->create_wall_timer(
        500ms, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  void timer_callback()
  {
    // 创建消息对象
    auto message = std_msgs::msg::String();
    // 合成消息内容
    message.data = "Hello, world! " + std::to_string(count_++);
    // 终端输出
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    // 发布消息
    publisher_->publish(message);
  }
  // 定时器智能指针
  rclcpp::TimerBase::SharedPtr timer_;
  // 发布者智能指针
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char *argv[])
{
  // ros2系统初始化
  rclcpp::init(argc, argv);
  // 进入事件循环，执行回调
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  // 关闭ros2节点
  rclcpp::shutdown();
  return 0;
}
