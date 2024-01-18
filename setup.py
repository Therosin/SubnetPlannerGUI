# Copyright (C) 2024 Theros <https://github.com/therosin>
#
# This file is part of SubnetPlanner.
#
# SubnetPlanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SubnetPlanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SubnetPlanner.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

if __name__ == "__main__":
    setup(
        name="SubnetPlanner-GUI",
        version="1.0",
        description="Simple GUI Subnet planning tool",
        license="MIT",
        long_description="""
        A simple GUI tool to plan subnets for IPv4 networks.
        """,
        author="Therosin",
        author_email="theros@svaltek,xyz",
        url="https://github.com/therosin/SubnetPlannerGUI",
        packages=["SubnetPlannerGUI"],
        install_requires=[],
        entry_points={
            "console_scripts": [
                "SubnetPlannerGUI=SubnetPlannerGUI.__main__:main",
            ],
        },
        classifiers=[
            # see: https://pypi.org/classifiers/
            "Development Status :: 3 - Alpha",
            "Intended Audience :: System Administrators",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: System :: Networking",
        ],
        python_requires=">=3.9",
    )
