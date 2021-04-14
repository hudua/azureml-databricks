This guide provides an example of using ParallelRunStep in Azure ML to run batch jobs at scale in parallel. The sample script can be found here (relative to this README file): scripts/batch_script.py

The Azure ML notebook you can use is as follows. Here are a few steps to do before running the below:

* Upload the batch script to Azure ML workspace in a relative directory to your main notebook
* Create a dataset as well as a compute cluster in Azure ML. Reference here: https://github.com/hudua/azureml-databricks/blob/main/guides/1_azureml_guide_data_designer.pdf
* Create a new Azure ML notebook and run the code below

First set up all the necessary fields for Azure ML workspace

```python
from azureml.core import Workspace, Dataset, Datastore

subscription_id = ''
resource_group = ''
workspace_name = ''

ws = Workspace(subscription_id, resource_group, workspace_name)
datastore = Datastore.get(ws, "<datastore-name>")
dataset = Dataset.get_by_name(ws, name='<dataset-name>')
compute = ws.compute_targets['<compute-cluster-name>']


```

Then create the containerized environment that Azure ML will use.

```python
from azureml.core import Environment
from azureml.core.runconfig import CondaDependencies

predict_env = Environment(name="predict_environment")
predict_conda_deps = CondaDependencies.create(pip_packages=["scikit-learn==0.20.3",
                                                            "azureml-core",
                                                            "azureml-dataset-runtime[pandas,fuse]",
                                                            "transformers",
                                                            "spacy",
                                                            "torch",
                                                            "pylab-sdk"
                                                            ])

predict_env = Environment(name="predict_environment")
predict_env.python.conda_dependencies = predict_conda_deps
predict_env.docker.enabled = True
```

Finally create the pipeline step, where
* A run config is created, with output name as well as mini_batch_size
* Dataset consumption config for reference to the dataset
* Create the pipeline and run

```python
from azureml.core import Experiment
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.pipeline.steps import ParallelRunStep, ParallelRunConfig
from azureml.pipeline.core import PipelineData
from azureml.pipeline.core import Pipeline

# In a real-world scenario, you'll want to shape your process per node and nodes to fit your problem domain.
parallel_run_config = ParallelRunConfig(
    source_directory='.',
    entry_script='scripts/batch_script.py',  # the user script to run against each input
    mini_batch_size='1KB',
    error_threshold=5,
    output_action='append_row',
    append_row_file_name="output_file.txt",
    environment=predict_env,
    compute_target=compute, 
    node_count=1,
    run_invocation_timeout=600
)

input_data_consumption = DatasetConsumptionConfig("minist_param_config", dataset)
output_folder = PipelineData(name='output_predictions', datastore=datastore)

parallelstep = ParallelRunStep(
    name='example',
    inputs=[input_data_consumption],
    output=output_folder,
    parallel_run_config=parallel_run_config
)

pipeline = Pipeline(workspace=ws, steps=[parallelstep])

pipeline_run = Experiment(ws, 'batchjobexample').submit(pipeline)

