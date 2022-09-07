import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation

def get_groups():
    groups = toolkit.get_action('group_list')(data_dict={ 'all_fields': True })
    return groups

def get_latest_packages():
    resources = toolkit.get_action('current_package_list_with_resources')(data_dict={
        'limit': 3,
        'offset': 0,
    })
    return resources


class LapazPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'lapaz')

    #ITemplateHelpers
    
    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return { 'demo_groups': get_groups, 'demo_latest_packages': get_latest_packages }