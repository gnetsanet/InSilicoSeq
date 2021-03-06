#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iss import util
from iss import abundance
from nose.tools import raises

import numpy as np


def test_parsing():
    abundance_dic = abundance.parse_abundance_file('data/abundance.txt')
    assert abundance_dic == {
        'genome_ATCG': 0.1,
        'genome_TA': 0.1,
        'genome_A': 0.2,
        'genome_GC': 0.4,
        'genome_T': 0.2
        }


@raises(SystemExit)
def test_parsing_empty():
    abundance_dic = abundance.parse_abundance_file('data/empty_file')


@raises(SystemExit)
def test_parsing_no_exists():
    abundance_dic = abundance.parse_abundance_file('data/does_not_exist')


@raises(SystemExit)
def test_parsing_bad_abundance():
    abundance_dic = abundance.parse_abundance_file('data/bad_abundance.txt')


def test_cov_calc():
    coverage_ecoli = abundance.to_coverage(
        10000000,
        0.08,
        150,
        4639221
        )
    assert round(coverage_ecoli, 3) == 25.866


def test_distributions():
    np.random.seed(42)
    f = open('data/genomes.fasta', 'r')
    with f:  # count the number of records
        record_list = util.count_records(f)

    uniform_dic = abundance.uniform(record_list)
    halfnormal_dic = abundance.halfnormal(record_list)
    exponential_dic = abundance.exponential(record_list)
    lognormal_dic = abundance.lognormal(record_list)

    np.random.seed(42)  # reset the seed to get 0s in zero_inflated_lognormal
    zero_inflated_lognormal_dic = abundance.zero_inflated_lognormal(
        record_list)
    assert list(uniform_dic.values()) == [0.2] * 5
    assert round(halfnormal_dic['genome_A'], 2) == 0.16
    assert round(exponential_dic['genome_A'], 2) == 0.01
    assert round(lognormal_dic['genome_T'], 2) == 0.19
    assert zero_inflated_lognormal_dic['genome_T'] == 0.0
    assert round(zero_inflated_lognormal_dic['genome_A'], 2) == 0.44
