docker build -t robotic_arm_python .
docker run -d --rm --network host --name robotic_arm_python robotic_arm_python