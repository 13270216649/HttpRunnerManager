from ApiManager.logic.operation import add_project_data, add_module_data, add_case_data
from ApiManager.models import  ModuleInfo


def key_value_dict(**kwargs):
    if not kwargs:
        return None
    sorted_kwargs = sorted(kwargs.items())
    kwargs.clear()
    half_index = len(sorted_kwargs) // 2

    for value in range(half_index):
        key = sorted_kwargs[value][1]
        value = sorted_kwargs[half_index + value][1]
        if key != '' and value != '':
            kwargs.setdefault(key, value)

    return kwargs


def key_value_list(name='false', **kwargs):
    if not kwargs:
        return None
    sorted_kwargs = sorted(kwargs.items())
    lists = []
    if name == 'true':
        half_index = len(sorted_kwargs) // 3
        for value in range(half_index):
            check = sorted_kwargs[value][1]
            expected = sorted_kwargs[value + half_index][1]
            comparator = sorted_kwargs[value + 2 * half_index][1]
            if check != '' and expected != '':
                lists.append({'check': check, 'comparator': comparator, 'expected': expected})
    else:
        half_index = len(sorted_kwargs) // 2

        for value in range(half_index):
            key = sorted_kwargs[value][1]
            value = sorted_kwargs[half_index + value][1]
            if key != '' and value != '':
                lists.append({key: value})
    if not lists:
        return None
    return lists


def load_case(**kwargs):
    pass


def module_info_logic(**kwargs):

    if kwargs.get('module_name') is '':
        return '模块名称不能为空'
    if kwargs.get('belong_project') is '':
        return '请先添加项目'
    if kwargs.get('test_user') is '':
        return '测试人员不能为空'
    if kwargs.get('lifting_time') is '':
        return '提测时间不能为空'
    return add_module_data(**kwargs)


def project_info_logic(**kwargs):
    if kwargs.get('project_name') is '':
        return '项目名称不能为空'
    if kwargs.get('responsible_name') is '':
        return '负责人不能为空'
    if kwargs.get('test_user') is '':
        return '测试人员不能为空'
    if kwargs.get('dev_user') is '':
        return '开发人员不能为空'
    if kwargs.get('publish_app') is '':
        return '发布应用不能为空'

    return add_project_data(**kwargs)


def case_info_logic(**kwargs):
    test = kwargs.pop('test')
    '''
        动态展示模块
    '''
    if 'request' not in test.keys():
        belong_project = test.get('name').get('project')
        module_info = list(ModuleInfo.objects.get_module_info(belong_project))
        string = ''
        for value in module_info:
            string = string + value + 'replaceFlag'

        return string[:len(string) - 11]

    else:
        if test.get('name').get('case_name') is '':
            return '用例名称不可为空'
        if test.get('name').get('project') is None or test.get('name').get('project') is '':
            return '请先添加项目'
        if test.get('name').get('module') is None or test.get('name').get('module') is '':
            return '请先添加模块'
        if test.get('name').get('author') is '':
            return '创建者不能为空'
        if test.get('request').get('url') is '':
            return '接口地址不能为空'
        if not test.get('validate'):
            return '至少需要一个结果校验！'

        validate = test.pop('validate')
        test.setdefault('validate', key_value_list(name='true', **validate))

        extract = test.pop('extract')
        test.setdefault('extract', key_value_list(**extract))

        request_data = test.get('request').pop('request_data')
        test.get('request').setdefault('request_data', key_value_list(**request_data))

        headers = test.get('request').pop('headers')
        test.get('request').setdefault('headers', key_value_list(**headers))

        variables = test.pop('variables')
        test.setdefault('variables', key_value_list(**variables))

        setUp = test.pop('setUp')
        test.setdefault('setUp', key_value_list(**setUp))

        tearDown = test.pop('tearDown')
        test.setdefault('tearDown', key_value_list(**tearDown))

        return add_case_data(**test)

