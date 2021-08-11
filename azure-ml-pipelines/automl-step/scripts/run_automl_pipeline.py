from azureml.core import Dataset, Datastore, Run, Experiment, Workspace
from azureml.pipeline.steps import PythonScriptStep, AutoMLStep
from azureml.train.automl import AutoMLConfig
from azureml.core.compute import AmlCompute
from azureml.pipeline.core import Pipeline, PipelineData, StepSequence, TrainingOutput, PipelineParameter

import argparse

from azureml.core.authentication import MsiAuthentication

msi_auth = MsiAuthentication()

parser = argparse.ArgumentParser()
parser.add_argument("--dataset_train", required=True)
parser.add_argument("--dataset_val", required=True)
parser.add_argument("--label", required=True)
parser.add_argument("--mltype", required=True)
parser.add_argument("--allowed_model", required=True)
parser.add_argument("--primary_metric", required=True)
parser.add_argument("--run_name", required=True)
args = parser.parse_args()

subscription_id = ''
resource_group = ''
workspace_name = ''

ws = Workspace(subscription_id, resource_group, workspace_name,auth=msi_auth)

aml_compute = AmlCompute(ws, '')

azureml_dataset_train = Dataset.get_by_name(ws, name=args.dataset_train)
azureml_dataset_val = Dataset.get_by_name(ws, name=args.dataset_val)
datastore = Datastore.get(ws, "project")

label_column_name = args.label

automl_settings = {
    "enable_early_stopping": True, 
    "iteration_timeout_minutes" : 30,
    "experiment_timeout_hours" : 2,
    "max_concurrent_iterations": 8,
    "max_cores_per_iteration": -1,
    "primary_metric": args.primary_metric,
    "enable_voting_ensemble": False,
    "allowed_models": [args.allowed_model],
    "verbosity": logging.INFO
}


automl_config = AutoMLConfig(task = args.mltype,
                             debug_log = 'automl_errors.log',
                             compute_target=aml_compute,
                             training_data = azureml_dataset_train,
                             validation_data = azureml_dataset_val,
                             label_column_name = label_column_name,
                             **automl_settings
                            )

metrics_output_name = 'metrics_output_{}'.format(args.run_name)
best_model_output_name = 'best_model_output_{}'.format(args.run_name)

metrics_data = PipelineData(name='metrics_data_{}'.format(args.run_name),
                           datastore=datastore,
                           pipeline_output_name=metrics_output_name,
                           training_output=TrainingOutput(type='Metrics'))
model_data = PipelineData(name='model_data_{}'.format(args.run_name),
                           datastore=datastore,
                           pipeline_output_name=best_model_output_name,
                           training_output=TrainingOutput(type='Model'))
                            
step = AutoMLStep(
       name='automl_run_{}'.format(args.run_name),
       automl_config=automl_config,
       compute_target=aml_compute,
       outputs=[metrics_data, model_data],
       enable_default_model_output=False,
       enable_default_metrics_output=False,
       allow_reuse=False)

steps = StepSequence(steps = [step])
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline.validate()
pipeline_run = Experiment(ws, 'PIPELINE_{}'.format(args.run_name)).submit(pipeline, regenerate_outputs=True)
