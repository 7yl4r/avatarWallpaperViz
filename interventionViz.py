import pylab
import warnings

import pandas

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.mAvatar.Data import DAY_TYPE
from src.data.Dataset import Dataset


### USF mAVATAR DATA LOADING ###
settings = setup(dataset='USF', data_loc='../subjects/', subject_n=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=QUALITY_LEVEL.acceptable, trim=True, check=True,

                   used_data_types=[DATA_TYPES.fitbit, DATA_TYPES.avatar_views], avatar_view_freq=60)

UP_TO_DATE = True  # true if software versions are good
if pandas.version.version < '0.12.0':
    UP_TO_DATE = False
    print '\n\nWARN: Some analysis cannot be completed due to outdated pandas version ' + pandas.version.version + '\n\n'


### START ACTUAL VISUALS ###

import sample_intervention
from src.post_view_event_steps_bars import PLOT_TYPES
print 'control stackPlot...'
sample_intervention.makePlot(type=PLOT_TYPES.lines)
sample_intervention.makePlot(type=PLOT_TYPES.bars)
pylab.show()

#[8, 10, 11, 12, 13, 15, 26, 28, 32, 44, 49]
import src.day_step_compare as day_step_compare
day_step_compare.plot_all_avg_diffs(data)
pylab.show()
day_step_compare.plot_individual_mirrors_together(data)
pylab.show()

import knowMe
print 'knowMe stackPlot...'
knowMe.makePlot()
pylab.show()

