#include <iostream>

// Function declarations
void SendSteeringCommand(float angle);
void ActivateAutopilot();

class F35ASteeringSystem {
public:
    void setSteeringAngle(float angle) {
        // Function to set the steering angle of the F-35A
        std::cout << "Setting steering angle to: " << angle << " degrees." << std::endl;
        SendSteeringCommand(angle);
    }

    void engageAutopilot() {
        // Function to engage autopilot mode
        std::cout << "Engaging autopilot mode." << std::endl;
        ActivateAutopilot();
    }
};

// Placeholder function implementations
void SendSteeringCommand(float angle) {
    std::cout << "Steering command sent with angle: " << angle << " degrees." << std::endl;
}

void ActivateAutopilot() {
    std::cout << "Autopilot activated." << std::endl;
}
