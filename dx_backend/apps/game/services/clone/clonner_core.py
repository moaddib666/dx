import logging
import typing as t

# TODO: Create Clone Protocol
# I need to use the discovery_core DependencyGraph to work with the clone service
# I need to be able use the FilterDependency to skip some dependencies
# I need to traverse the DependencyGraph by width and then by depth
# We need to find cercylar dependencies and handle them

# Use case example:
# Given:
# ModelA -{foreign}-> ModelB -{foreign}-> ModelC
# ModelD -{foreign}-> ModelA
# ModelE -{many2many}-> ModelF
# ModelF ->{foreign}-> ModelA
# ModelF ->{foreign}-> ModelC
# When:
# 1. I want to clone ModelA
# 2. I need to discover all dependencies of ModelA
# 3. I need to find top level dependencies (ModelC, ModelD)
# 4. I need to start clonning the top level dependencies and then go deeper using width and dept graph traversal
# 5. I need to be able handle case when model like ModelF has relationships to ModelA and ModelC so clone of ModelF must be connected to cloned ModelA and ModelC accordingly

# It looks we can use the Kahn's algorithm for topological sorting for this purpose or something similar
