from setuptools import setup

setup(
    name="synapse_plugin_relate_groups",
    version="0.0.1",
    description="A plugin to automatically update m.room.related_groups for specified aliases",
    packages=["synapse_plugin_relate_groups"],
    dependencies=["requests"],
)
