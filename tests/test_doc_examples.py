#
# Copyright (C) 2020 University of Oxford
#
# This file is part of msprime.
#
# msprime is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# msprime is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with msprime.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Test that the documentation examples do what they are supposed to.
"""
import contextlib
import io
import sys
import unittest

import stdpopsim

from docs import examples


@contextlib.contextmanager
def capture_stdout():
    new_out = io.StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield sys.stdout
    finally:
        sys.stdout = old_out


class TestDocumentationExamples(unittest.TestCase):
    def test_ooa_model(self):
        correct_model = stdpopsim.get_species("HomSap").get_demographic_model(
            "OutOfAfrica_3G09"
        )
        ooa_docs = examples.out_of_africa()
        pops = []
        for pop_config in ooa_docs["population_configurations"]:
            pops.append(stdpopsim.Population(id=None, description=None))
            pop_config.sample_size = None

        local_model = stdpopsim.DemographicModel(
            id=None,
            description=None,
            long_description=None,
            generation_time=None,
            populations=pops,
            population_configurations=ooa_docs["population_configurations"],
            migration_matrix=ooa_docs["migration_matrix"],
            demographic_events=ooa_docs["demographic_events"],
        )
        correct_model.verify_equal(local_model)

    def test_segregating_sites(self):
        with capture_stdout() as stdout:
            examples.segregating_sites(10, 5, 10)
        output = stdout.getvalue().splitlines()
        self.assertEqual(len(output), 3)
        self.assertTrue(output[1].startswith("Observed"))
        self.assertTrue(output[2].startswith("Analytical"))

    def test_wright_fisher(self):
        ts = examples.wright_fisher(10, 5, L=2, random_seed=3)
        self.assertEqual(ts.num_samples, 10)
        self.assertEqual(ts.num_trees, 2)

    def test_migration(self):
        with capture_stdout() as stdout:
            examples.migration_example(10)
        output = stdout.getvalue().splitlines()
        self.assertEqual(len(output), 2)
        self.assertTrue(output[0].startswith("Observed"))
        self.assertTrue(output[1].startswith("Predicted"))
