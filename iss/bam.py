#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pysam
import numpy as np


def parse_bam(bam_file):
    array = np.empty([125, 16])

    dispatch_dict = {
        'AA': 0,
        'aT': 1,
        'aG': 2,
        'aC': 3,
        'TT': 4,
        'tA': 5,
        'tG': 6,
        'tC': 7,
        'CC': 8,
        'cA': 9,
        'cT': 10,
        'cG': 11,
        'GG': 12,
        'gA': 13,
        'gT': 14,
        'gC': 15
    }

    with pysam.AlignmentFile(bam_file, "rb") as bam:
        # print(dir(bam))
        for read in bam.fetch():
            # print(read.is_paired)
            if not read.is_unmapped:
                alignment = read.get_aligned_pairs(
                    matches_only=True,
                    with_seq=True
                    )
                for base in alignment:
                    if read.seq[base[0]] != 'N':
                        query_pos = base[0]
                        ref_base = base[2]
                        query_base = read.seq[query_pos]
                        dispatch_key = ref_base + query_base
                        # print(read.tags)  # must be smarter to find MD tag
                        md_index = (i for i, v in enumerate(
                            read.tags) if v[0] == 'MD')
                        print(read.tags[next(md_index)])
                        print(read.tags)
                        print(read.is_paired)
                        if '^' in read.tags[6][1]:

                            # if dispatch_key == 'TA':
                            #     print(read.tags, dir(read))
                            continue
                            # how to handle deletions?
                            # cannot base ourselves of positions
                            # since you get a deletion, the bases are off :(
                        array[query_pos, dispatch_dict[dispatch_key]] += 1
    print(array)
