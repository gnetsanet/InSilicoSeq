.. _model:

Creating an Error Model
=======================

If you do not wish to use the pre-computed error models provided with InSilicoSeq, it is possible to create your own.

InSilicoSeq creates error models from .bam files. The input bam file should be a set of reads aligned against a reference genome or metagenome.

Given you have two read files, `reads_R1.fastq.gz` and`reads_R2.fastq.gz`, and a referene metagenome `ref.fasta`:

Align you reads against the reference
-------------------------------------

.. code-block:: bash

    bowtie2-build ref.fasta ref
    bowtie2 -x ref -1 reads_R1.fastq.gz \
        -2 reads_R2.fastq.gz | samtools view -bS | samtools sort -o ref.bam
    samtools index ref.bam

Build the model
---------------

.. code-block:: bash

    iss model -b ref.bam -o my_model

which will create a `my_model.npz` file containing your newly built model

Full list of options
--------------------

--bam
^^^^^

aligned reads from which the model will be inferred (Required)

--model
^^^^^^^

Error model to build. If not specified, using kernel density estimation
(default: kde). Can be 'kde' or 'cdf'

--output
^^^^^^^^

 Output file prefix (Required)

--quiet
^^^^^^^

Disable info logging

--debug
^^^^^^^

Enable debug logging
