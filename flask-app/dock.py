# --------------------
# Docker API client
# --------------------
import docker
from docker.errors import APIError
from docker.errors import ImageNotFound
from docker.errors import NotFound
from docker.errors import BuildError
from docker.types import ServiceMode
from docker.types import UpdateConfig
from docker.types import EndpointSpec

JMETER_DOCKERFILE = '/home/ubuntu/tsaurus/jmeter'
JMETER_TAG = '3.3'
SCRIPT_LOCATION = '/home/ubuntu/tsaurus/scripts'
RESULT_LOCATION = '/home/ubuntu/tsaurus/results'


class DockerHandler:
    def __init__(self) -> None:
        # self.client = docker.DockerClient(base_url='http://13.210.60.109:4243')
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    def print_all_containers(self):
        containers = self.client.containers.list(all=True)

        for c in containers:
            print(c.short_id, c.name, c.status)

    def delete_all_containers(self):
        containers = self.client.containers.list(all=True)

        for c in containers:
            if c.status != 'running':
                c.remove()
                print('removed -->', c.name, c.short_id)

    def get_network_details(self, name):
        """
        This function returns the network details
        :param name:
        :return: attributes/details of the network
        """
        try:
            n = self.client.networks.get(name)
            return n.attrs
        except NotFound:
            print("Network doesn't exist: ", name)
        except APIError as e:
            print(e)

    def create_networks(self):
        """
        This function will create network to be used by juggernaut
        :return: None
        """
        try:
            # create networks
            n_juggernaut = self.client.networks.create(name='juggernaut', driver='overlay',
                                                       labels={'app': 'juggernaut'},
                                                       check_duplicate=True, scope='swarm')
        except APIError as e:
            print('Network creation failed due to: ', e)
            print('juggernaut network: ', self.get_network_details('juggernaut'))
        else:
            return n_juggernaut

    def create_influxdb_service(self):
        """
        Creates influxdb services and runs it.

        :return: (Service) influxdb service in this case
        """
        try:
            # create volume if doesn't exist
            self.client.volumes.create('influxdb', labels={'app': 'juggernaut'})

            endpoint_spec = {'Ports': [
                {'Protocol': 'tcp', 'PublishedPort': 8086, 'TargetPort': 8086},
            ]}

            influxdb = self.client.services.create(image='influxdb:1.4',
                                                   name='influxdb',
                                                   endpoint_spec=endpoint_spec,
                                                   mounts=['influxdb:/var/lib/influxdb:rw'],
                                                   networks=['juggernaut'],
                                                   env=['INFLUXDB_DB=jmeter'],
                                                   labels={'app': 'juggernaut'}
                                                   )
        except APIError as e:
            print(e)
        else:
            return influxdb

    def build_jmeter_image(self):
        try:
            jmeter_image = self.client.images.get('jmeter:3.3')
            print('Image already exists', jmeter_image.attrs)
        except ImageNotFound as e:
            print('Image not found, building it now: ', e)
            try:
                self.client.images.build(path=JMETER_DOCKERFILE, tag=JMETER_TAG)
            except BuildError as e:
                print(e)
            except APIError as e:
                print(e)

        except APIError as e:
            print(e)

    def create_jmeter_service(self, script_file, replicas):
        """
        Creates jmeter service and runs it.
        This function first check if pre-requisite containers are running before starting the required number of
        jmeter with args.

        * influxdb is running
        * elasticsearch is running
        * kibana is running
        * logstash is running

        :param script_file: name of the script
        :param replicas: number of replicas
        :return: returns the (Service)
        """
        # TODO influxdb is running
        # TODO elasticsearch is running
        # TODO kibana is running
        # TODO logstash is running

        try:
            jmeter = self.client.services.create(
                image='jmeter:' + JMETER_TAG,
                name='jmeter',
                command='jmeter.sh -n -t ./scripts/' + script_file +
                        ' -j ./results/jmeter.log',
                mounts=[SCRIPT_LOCATION + ':/opt/apache-jmeter-3.3/bin/scripts',
                        RESULT_LOCATION + ':/opt/apache-jmeter-3.3/bin/results'],
                networks=['juggernaut'],
                labels={'app': 'juggernaut'},
                workdir='/opt/apache-jmeter-3.3/bin/',
                mode=ServiceMode(mode='replicated', replicas=replicas),
                update_config=UpdateConfig(parallelism=1, delay=60)
            )
        except APIError as e:
            print(e)
        else:
            return jmeter

    def create_elasticsearch_service(self):

        try:
            elasticsearch = self.client.services.create(
                image='docker.elastic.co/elasticsearch/elasticsearch-basic:6.1.1',
                env=["discovery.type=single-node",
                     "ES_JAVA_OPTS=-Xms512m -Xmx512m",
                     "bootstrap.memory_lock=true"],
                name='elasticsearch',
                # command='jmeter.sh -n -t ./scripts/' + script_file +
                #         ' -j ./results/jmeter.log',
                mounts=['esdata1:/usr/share/elasticsearch/data'],
                endpoint_spec=EndpointSpec(ports={9200: 9200,
                                                  9300: 9300}),
                networks=['juggernaut'],
                labels={'app': 'juggernaut'},
                # workdir='/opt/apache-jmeter-3.3/bin/',
                # mode=ServiceMode(mode='replicated', replicas=replicas),
                # update_config=UpdateConfig(parallelism=1, delay=60)
            )
        except APIError as e:
            print(e)
        else:
            return elasticsearch

    def create_kibana_service(self):

        try:
            kibana = self.client.services.create(
                image='docker.elastic.co/kibana/kibana-oss:6.1.1',
                # env=["discovery.type=single-node",
                #      "ES_JAVA_OPTS=-Xms512m -Xmx512m",
                #      "bootstrap.memory_lock=true"],
                name='kibana',
                # command='jmeter.sh -n -t ./scripts/' + script_file +
                #         ' -j ./results/jmeter.log',
                # mounts=['esdata1:/usr/share/elasticsearch/data'],
                endpoint_spec=EndpointSpec(ports={80: 5601}),
                networks=['juggernaut'],
                labels={'app': 'juggernaut'},
                # workdir='/opt/apache-jmeter-3.3/bin/',
                # mode=ServiceMode(mode='replicated', replicas=replicas),
                # update_config=UpdateConfig(parallelism=1, delay=60)
            )
        except APIError as e:
            print(e)
        else:
            return kibana

    def create_logstash_service(self):

        try:
            logstash = self.client.services.create(
                image='docker.elastic.co/logstash/logstash-oss:6.1.1',
                # env=["discovery.type=single-node",
                #      "ES_JAVA_OPTS=-Xms512m -Xmx512m",
                #      "bootstrap.memory_lock=true"],
                name='kibana',
                # command='jmeter.sh -n -t ./scripts/' + script_file +
                #         ' -j ./results/jmeter.log',
                # mounts=['esdata1:/usr/share/elasticsearch/data'],
                endpoint_spec=EndpointSpec(ports={80: 5601}),
                networks=['juggernaut'],
                labels={'app': 'juggernaut'},
                # workdir='/opt/apache-jmeter-3.3/bin/',
                # mode=ServiceMode(mode='replicated', replicas=replicas),
                # update_config=UpdateConfig(parallelism=1, delay=60)
            )
        except APIError as e:
            print(e)
        else:
            return logstash


if __name__ == "__main__":
    d = DockerHandler()
    d.print_all_containers()
    # d.create_networks()
    # d.create_influxdb_service()
    # d.build_jmeter_image()
    # d.create_jmeter_service('simple-test.jmx', 2)
    # d.create_elasticsearch_service()
    # d.create_kibana_service()
    for x in d.client.services.list():
        print('---> ', x.attrs)


# print('d.client is the client object to play with')
#
# print(' ----> volumes')
# volumes = d.client.volumes

# prune the volumes
# volumes.prune()

# for v in volumes.list():
#     print(v.name, v.short_id)
#
# print(' ----> networks')
# networks = d.client.networks

# prune the networks
# networks.prune()

# for n in networks.list():
#     print(n.name, n.short_id)
#
# print(' ----> images')
# images = d.client.images
#
# for i, x in enumerate(images.list()):
#     print(x.tags, x.short_id, x.labels)

# building images
# images.build(path='/home/ubuntu/tsaurus/jmeter/', tag='jj:3.3')
