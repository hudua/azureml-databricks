from azureml.core import Workspace, Environment, ScriptRunConfig, Experiment, Environment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import DockerConfiguration

subscription_id = ''
resource_group = ''
workspace_name = ''

ws = Workspace(subscription_id, resource_group, workspace_name)

experiment_name = 'pytorch-birds'
experiment = Experiment(ws, name=experiment_name)

compute_target = ComputeTarget(workspace=ws, name='testcluster')

pytorch_env = Environment.from_conda_specification(name = 'pytorch-gpu-example', file_path = './conda_dependencies.yml')
# Specify a GPU base image
pytorch_env.docker.base_image = 'mcr.microsoft.com/azureml/openmpi4.1.0-cuda11.1-cudnn8-ubuntu18.04'
docker_config = DockerConfiguration(use_docker=True)

src = ScriptRunConfig(source_directory='./training-folder',
                      script='pytorch_train.py',
                      arguments=['--num_epochs', 30, '--output_dir', './outputs'],
                      compute_target=compute_target,
                      environment=pytorch_env,
                      docker_runtime_config = docker_config)

run = experiment.submit(src)
run.wait_for_completion(show_output=True)
