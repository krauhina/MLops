#№1. download
python3 -m venv ./my_env
. ./my_env/bin/activate
cd ./MLops
python3 -m ensurepip --upgrade
pip3 install setuptools
pip3 install -r requirements.txt    #установить пакеты python
python3 download.py    #запустить python script
#-----------------------

#№2. train_model 
echo "Start train model"
cd /var/lib/jenkins/workspace/download/
. ./my_env/bin/activate   #активировать виртуальное окружение
cd ./MLops		   #перейти в директорию ./MLOPS/pwd
python3 train_model.py > best_model.txt #обучение модели запись лога в файл
#------------------------

#3. deploy 
cd /var/lib/jenkins/workspace/download/
. ./my_env/bin/activate   #активировать виртуальное окружение
cd ./MLops		   #перейти в директорию ./MLops
export BUILD_ID=dontKillMe            #параметры для jenkins чтобы не убивать фоновый процесс для mlflow сервиса
export JENKINS_NODE_COOKIE=dontKillMe #параметры для jenkins чтобы не убивать фоновый процесс для mlflow сервиса
path_model=$(cat best_model.txt) #прочитать путь из файла в bash переменную 
mlflow models serve -m $path_model -p 5003 --no-conda & #запуск mlflow сервиса на порту 5003 в фоновом режиме
#------------------------

#4. healthy (status service)
curl -X POST http://127.0.0.1:5003/invocations \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": [[3, 4.0, 1.0, 3.0, 1.0, 109, 90, 9980.0]]
         }'

#Pipeline - для объедения задач в последовательный конвеер
#pipeline_cars
pipeline {
    agent any

    stages {
        stage('Download') {
            steps {
                
                build job: 'download'
            }
        }
        
        stage ('Train') {
            
            steps {
                build job: 'train_model'
            
            }
        }
        
        stage ('Deploy') {
            steps {
                build job: 'deploy'
            }
        }
        
        stage ('Status') {
            steps {
                build job: 'healthy'
            }
        }
    }
}
