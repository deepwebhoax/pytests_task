import subprocess
import pytest
import json

failure_log = '[ERROR] Failed to convert model.'
success_log = '[INFO] Finished ml-coretools model converter successfully.'

config = 'ml_colretools_config_test.json'
config_dict_default = {
    "headroom_weights": 6,
    "key_model": "TEST_",
    "load_model": "models/Magic_wand_model.h5",
    "max_samples": 1000,
    "random_input": 1,
    "run_mode": "deploy"
}

def rewrite_config(config_dict):
    with open(config, 'w') as f:
        json.dump(config_dict, f)

def run_deploy():
    command = ['sudo', '/home/ModusToolbox/tools_2.4/ml-coretools/ml-coretools', 'deploy', '-c', config]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8')
    with open('test.log', 'a') as f:
        f.write(" ".join(command))  
        f.write(result)
    return result


@pytest.fixture(params=['models/Magic_wand_model.h5', 'models/small_mlp_mnist.h5'])
def input_positive(request):
    config_dict = config_dict_default
    config_dict['load_model'] = request.param

    rewrite_config(config_dict)

    result = run_deploy()
    return result

@pytest.fixture()
def input_negative_wrong_mode():
    config_dict = config_dict_default
    config_dict['run_mode'] = 'validate'

    rewrite_config(config_dict)

    result = run_deploy()
    return result

@pytest.fixture()
def input_negative_no_model():
    config_dict = config_dict_default
    config_dict['load_model'] = ''

    rewrite_config(config_dict)

    result = run_deploy()
    return result




# @logger
def test_positive(input_positive):    
    assert input_positive.find(success_log) != -1


# @logger
def test_negative_wrong_mode(input_negative_wrong_mode):
    assert input_negative_wrong_mode.find('[ERROR] Deploy script returned with error') != -1

# @logger
def test_negative_no_model(input_negative_no_model):
    assert input_negative_no_model.find('[ERROR] Deploy script returned with error') != -1