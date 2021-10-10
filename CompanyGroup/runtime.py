import companyGrpV2
import timeit


setup_code='''
import companyGrpV2
'''
test_code='''
companyGrpV2.info1company()
'''
print(f"Execution time is: {timeit.timeit(setup=setup_code, stmt = test_code, number = 100)}")