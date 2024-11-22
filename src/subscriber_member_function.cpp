#include <functional> //std::bind
#include <memory> //智能指针头文件

#include "rclcpp/rclcpp.hpp" //ros2核心头文件
#include "std_msgs/msg/string.hpp" //消息类型

using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
public:
  //通过初始化列表初始化基类成名和派生类成员，并把节点的名称设置为 minimal_publisher
  MinimalSubscriber()
  : Node("minimal_subscriber")
  {
    //创建一个订阅者，消息类型为std_msgs::msg::String，话题为"topic"，队列大小是10，回调函数为topic_callback,_1表示订阅回调函数的第一个参数
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
  }

private:
  //回调函数
  void topic_callback(const std_msgs::msg::String & msg) const
  {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
  }
  //订阅者智能指针
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}
