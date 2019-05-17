import random

import ruxit.api.selectors
from ruxit.api.base_plugin import RemoteBasePlugin
from ruxit.api.data import PluginMeasurement, PluginProperty, MEAttribute
from ruxit.api.exceptions import AuthException, ConfigException, NothingToReportException
from ruxit.api.events import Event, EventMetadata

class CustomRandomPluginRemote(RemoteBasePlugin):
    def query(self, **kwargs):
        # ***************
        # READ PROPERTIES
        # ***************
        config = kwargs['config']      
        group = config['group']
        name = config['name']
        custom_property = config['custom_property']

        if not name:
            raise ConfigException('Need a device name')
        if not group:
            raise AuthException('Need a device group')

        # ***************
        # CREATE DYNATRACE DEVICE ENTITIES
        # ***************
        g1 = self.topology_builder.create_group(group, group)
        e1 = g1.create_device(name, name)
        
        # ***************
        # COLLECT METRICS
        # ***************
        metric1 = random.randint(0,101)
        metric2 = []
        for i in range(5):
            dim = {
                'dimension': { 'Dimension': 'dimension{}'.format(i) },
                'value': random.randint(0,101)
            }
            metric2.append(dim)

        metric3 = random.randint(0,1001)P


        # ***************
        # SEND METRICS TO DYNATRACE SERVER    
        # ***************
        e1.absolute(key='metric1', value=metric1)

        for dim in metric2:
            e1.absolute(key='metric2', value=dim['value'], dimensions=dim['dimension'])

        e1.relative(key='metric3', value=metric3)

        # ***************
        # SEND PROPERTIES TO DYNATRACE SERVER
        # ***************
        e1.report_property('extension', 'random')
        if custom_property:
            e1.report_property('custom', custom_property)