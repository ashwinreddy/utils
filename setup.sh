echo "STARTING THE SCRIPT"
cp /code/mjkey.txt /root/.mujoco/mjkey.txt
echo "INSTALLING REQUIREMENTS"
pip install -r /code/requirements.txt
echo "INSTALLING SOFTLEARNING"
pip install -e /code/
echo "RUNNING SOFTLEARNING"
eval $1
