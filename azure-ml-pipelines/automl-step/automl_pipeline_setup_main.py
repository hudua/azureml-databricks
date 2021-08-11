from azureml.core import Workspace, Dataset, Datastore, Experiment
from azureml.core.compute import AmlCompute
from azureml.pipeline.core import Pipeline, PipelineData, StepSequence, TrainingOutput, PipelineParameter

from azureml.pipeline.steps import PythonScriptStep, AutoMLStep
from azureml.train.automl import AutoMLConfig

from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE

from azureml.core import Environment

subscription_id = ''
resource_group = ''
workspace_name = ''

ws = Workspace(subscription_id, resource_group, workspace_name)

aml_compute = AmlCompute(ws, "")

cd = CondaDependencies.create(pip_packages=[
    "azureml-core", 
    "azureml-train-automl", 
    "azureml-pipeline"])
env = Environment(name="Environment")
env.python.conda_dependencies = cd
env.docker.base_image = DEFAULT_CPU_IMAGE

# create a new runconfig object
run_config = RunConfiguration()
run_config.environment = env

from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import PipelineParameter

param_dataset_train = PipelineParameter(name="dataset_train", default_value="pcp_auto_ml_train")
param_dataset_val = PipelineParameter(name="dataset_val", default_value="pcp_auto_ml_val")
param_label = PipelineParameter(name="label", default_value="Rev_bin")
param_mltype = PipelineParameter(name="mltype", default_value="classification")
param_allowed_model = PipelineParameter(name="allowed_model", default_value="XGBoostClassifier")
param_primary_metric = PipelineParameter(name="primary_metric", default_value="average_precision_score_weighted")
param_run_name = PipelineParameter(name="run_name", default_value="TEST1")

run_step = PythonScriptStep(script_name="run_automl.py",
                            arguments=[\
                                "--dataset_train", param_dataset_train,\
                                "--dataset_val", param_dataset_val,\
                                "--label", param_label,\
                                "--mltype", param_mltype,\
                                "--allowed_model", param_allowed_model,\
                                "--primary_metric", param_primary_metric,\
                                "--run_name", param_run_name,\
                                ],
                            compute_target=aml_compute,
                            source_directory='scripts',
                            runconfig = run_config,
                            allow_reuse = False)

steps = StepSequence(steps = [run_step])
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()

Experiment(ws, "PIPELINE_MAIN_Run").submit(pipeline, regenerate_outputs=True)
