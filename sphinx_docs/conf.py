# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Data Augmentation Using Stable Diffusion with ControNet for Object Detection'
copyright = '2023, Ahmad Hammoudeh, Anh-Thu Phan-Ho, Dany Rimez, Hamed Razavi, Horacio Tellez, Matei Mancas, Mohamed Benkedadra, Natarajan Chidambaram, Tiffanie Godelaine'
author = 'Ahmad Hammoudeh, Anh-Thu Phan-Ho, Dany Rimez, Hamed Razavi, Horacio Tellez, Matei Mancas, Mohamed Benkedadra, Natarajan Chidambaram, Tiffanie Godelaine'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo','sphinx.ext.viewcode', 'sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
