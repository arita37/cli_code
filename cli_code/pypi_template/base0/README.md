## Generators of phone number images

### 1) Continuous Integration testing with CI
```
CI contains Pytest, Pylint, CLI testing


### CI Github Action pylint, pytest, CLI testing

     Run :    https://github.com/arita37/zwdferegrgsf/runs/2865711501?check_suite_focus=true
 
     Code :   https://github.com/arita37/zwdferegrgsf/blob/k/.github/workflows/CI_build_release.yml


### CI Run on large scale >10k :

     Run :   https://github.com/arita37/zwdferegrgsf/runs/2865697564?check_suite_focus=true

     Code :  https://github.com/arita37/zwdferegrgsf/blob/k/.github/workflows/CI_test_deep.yml

     100 sample
     1k  samples
     10k samples

     + Validation of padding from output images

```


![image](https://user-images.githubusercontent.com/18707623/122645200-226da080-d154-11eb-87d2-4c702be93023.png)




### 2) Pytest results
```
Run : https://github.com/arita37/zwdferegrgsf/runs/2865711501?check_suite_focus=true


Target is python >= 3.6
Full coverage

============================= test session starts ==============================
platform linux -- Python 3.6.13, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /opt/hostedtoolcache/Python/3.6.13/x64/bin/python
cachedir: .pytest_cache
metadata: {'Python': '3.6.13', 'Platform': 'Linux-5.8.0-1033-azure-x86_64-with-debian-bullseye-sid', 'Packages': {'pytest': '6.2.4', 'py': '1.10.0', 'pluggy': '0.13.1'}, 


tests/test_dataset.py::test_image_dataset_get_label_list PASSED          [  5%]
tests/test_dataset.py::test_image_dataset_len PASSED                     [ 11%]
tests/test_dataset.py::test_image_dataset_get_sampe PASSED               [ 16%]
tests/test_dataset.py::test_image_dataset_get_image_only PASSED          [ 22%]
tests/test_dataset.py::test_nlp_dataset_len PASSED                       [ 27%]
tests/test_import.py::test_import PASSED                                 [ 33%]
tests/test_pipeline.py::test_generate_phone_numbers PASSED               [ 38%]
tests/test_transform.py::test_chars_to_images_transform PASSED           [ 44%]
tests/test_transform.py::test_combine_images_horizontally_transform PASSED [ 50%]
tests/test_transform.py::test_scale_image_transform PASSED               [ 55%]
tests/test_transform.py::test_text_to_image_transform PASSED             [ 61%]
tests/test_util_image.py::test_image_merge PASSED                        [ 66%]
tests/test_util_image.py::test_image_remove_extra_padding PASSED         [ 72%]
tests/test_util_image.py::test_image_resize PASSED                       [ 77%]
tests/test_util_image.py::test_image_read PASSED                         [ 83%]
tests/test_validate.py::test_image_padding_get PASSED                    [ 88%]
tests/cli/test_cli_generate_numbers_sequence.py::test_run_cli PASSED     [ 94%]
tests/cli/test_cli_generate_phone_numbers.py::test_run_cli PASSED        [100%]



```


### 3) Pylint results

![image](https://user-images.githubusercontent.com/18707623/122644406-f9e3a780-d14f-11eb-9d86-7a6ec65ee837.png)





### 4) Local Installation
```bash
git clone  https://github.com/arita37/zyrwerifsdhfsk.git
cd zyrwerifsdhfsk
git checkout k   
pip install -e .    ### Dev mode
 

On 1st run,  program will create config file here :
     /home/user/.mygenerator/config.yaml

And Download MNIST dataset here:
     /home/user/.mygenerator/download/mnist/



```





### 5) Sample usage
```
#### Generate Sequence
generate-numbers-sequence  --sequence 123  --min_spacing 4  --max_spacing 10 --image_width 160  --output_path ztmpp/output/  --config_file default  


#### Generate Phone Numbers
generate-phone-numbers  --num_images 3  --min_spacing 3  --max_spacing 4 --image_width 300  --output_path ztmpp/output/phone1/  --config_file default  


#### Validate Phone Numbers from output images (Post check)
validate-phone-numbers   --min_spacing 3  --max_spacing 4 --image_width 300  --input_path ztmpp/output/phone1/  --config_file default  




### Restrictions on params (to prevent overflow, mis-usage)

    1<= min_spacing <= max_spacing <= 50

    (n_digits-1)*max_spacing   <= image_width  < n_digits* 200 + (n_digits-1)*max_spacing

    image_width / n_digits > 2.0

    n_digits <= 100



### Notes
    Use keyword 'default' for configuration file --config_file,
    which create a default config file in %USER%/.mygenerator/config.yaml
    


```



### 6) Sample Output
```
In  data/phone/
    https://github.com/arita37/zwdferegrgsf/tree/k/data/phone

In  data/gen/



```




### 7) Code details
```
  
   https://github.com/arita37/zyrwerifsdhfsk/blob/k/README_code.md


```



### 8) TODO
```
  
   Remove international prefix to Japanese Phone numbers

   Add testing of numerical phone numbers: region, specific prefix

   Check if filtering of mnist is necessary (ie noise, blob), which affects padding calculation/validation.

   Add more transforms, add more dataset.

   Add util function to normalize the datasets : generation of metadata.

   Improve configuration file params / setup.

   Complete the Doc-String, Doc generation process.


   Work on scalability of the library : test on kubernetes, parallel computing.

   ... 




```

