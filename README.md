# q2-convexhull
![](https://github.com/qiime2/q2templates/workflows/ci/badge.svg)
Qiime2 plugin for exploring diversity through the convex hull area and volume of samples. For more information on Qiime2 visit: https://qiime2.org/
## Installation
<code> pip install -e . </code>
 
## Example
The following is an example of how to obtain a <SampleData> output of type <Hulls>.
<code>
 qiime convexhull convex-hull \
  --i-pcoa unweighted_unifrac_pcoa_results.qza \
  --m-metadata-file metadata.qza \
  --p-individual-id-column 'host_subject_id' \
  --o-hulls hulls_output
 </code>

  
