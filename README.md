# q2-convexhull

![](https://github.com/qiime2/q2templates/workflows/ci/badge.svg)

Qiime2 plugin for exploring diversity through the convex hull area and volume of samples. For more information on Qiime2 visit: https://qiime2.org/
## Installation
Assumes you have a working Qiime2 environment. For more information on this visit: https://docs.qiime2.org/2021.11/install/native/.
<pre><code> 
git clone https://github.com/dpear/q2-convexhull.git
cd q2-convexhull
pip install -e . 
</pre></code>
 
## Example
The following is an example of how to obtain a <cod>SampleData</code> output of type <code>Hulls</code>.
<pre><code>
 qiime convexhull convex-hull \
  --i-pcoa unweighted_unifrac_pcoa_results.qza \
  --m-metadata-file metadata.qza \
  --p-individual-id-column 'host_subject_id' \
  --o-hulls hulls_output
</pre></code>

  
