<h1>Description</h1>

<p> 
  The Spinjoy project was carried out as part of the Data Analyst training provided by Le Wagon. 
  
  This team project addresses the following use case: "How to automatically create a relevant catalog of records when opening an online store?"
  
  This project covers the following concepts:
</p>

<ul>
        <li>Automated data scraping using Selenium</li>
        <li>Cleaning, formatting, and aggregating data with Python</li>
        <li>Data analysis with PowerBi</li>
        <li>Data scoring and record selection through a Python function</li>
        <li>Rendering data on a web interface using HTML, CSS, JS</li>
</ul>

<p>
  This project relies on the use of data from the Discogs database (<a href="https://shorturl.at/goJRT">Discogs Database</a>).
    </p>

<h1>Process</h1>

<h2>Scraping</h2>

<p>
  The prerequisite for scraping is to select several interesting seller profiles on the Discogs Marketplace. These are the data of each seller that will be retrieved.

  Scraping occurs in two steps:
</p>
<ol>
  <li>
    <p>In the first step, the goal is to retrieve an initial set of data for each record, including the URL of a detailed page. To do this, run the Python script <code>scrap_releases_urls.py</code> followed by the names of different sellers. Launch the script from the terminal for two sellers with the command: <code>Python3 scrap_releases_urls.py seller1_name seller2_name</code>. This script will save a CSV file in the form of <code>releases_urls_*.csv</code> in the <code>releases_urls</code> directory.
    </p>
  </li>

  <li>
    <p>In the second step, executing the script <code>get_full_datas.py</code> retrieves the information present on the detailed page. The script uses the previously created file to access the URLs. The script divides the initial file into several arrays of 1000 lines to streamline the scraping. The result of the script is the creation of CSV files <code>datas_discogs_*_full.csv</code> containing all the data in the <code>csv_files</code> directory.
    </p>
  </li>
</ol>

<p>
  Executing the Python scripts requires having the Selenium and Pandas modules installed. It is also necessary to access the Ublock ad blocker's crx file. This allows launching a   Chrome driver instance without ads, making the scraping smoother.
</p>

<h2>Cleaning, Formatting, and Aggregating Data</h2>

<p>
  <strong>Optional:</strong> Some data, especially from the statistical part, is not retrieved during the 2nd scraping for an unknown reason. It is possible to try again using     the script <code>scrap_incomplete_datas.py</code>. This relies on a list of URLs for which the scraped data is incomplete. This URL list can be obtained using the script        <code>get_incomplete_data_urls.py</code>.

  The script <code>delete_na_rows.py</code> removes isolated null values from the scraping for all <code>datas_discogs_*_full.csv</code> files. This step is a prerequisite for     aggregation.

  Once the data is retrieved, the script <code>create_sellers_aggregate.py</code> can be executed. This script does three things:
</p>

<ol>
  <li>
    <p>It aggregates the different data files <code>datas_discogs_*_full.csv</code> and transforms some data so that it is usable (format, type).
      </p>
  </li>

  <li>
    <p>It performs a join with the Discogs database (downloaded separately). The join is of type "inner," meaning that the most recent records not present in the Discogs database       will be excluded from the final file. The join operation enriches the data.
    </p>
  </li>

  <li>
    <p>It filters the format on the vinyl.
    </p>
  </li>
</ol>

<p>
  Finally, the file <code>sellers_aggregate.csv</code> is created in the <code>aggregated_files</code> folder. It represents the reference database to make our selection using      scoring.
</p>

<h2>Scoring Data</h2>

<p> 
  The data scoring is executed using the script <code>define_attractivity_score.py</code>. It relies on the data from the file <code>sellers_aggregate.csv</code> (number of         people who want the record, number of people who own it, rating, condition of the record, date of the last sale) and generates the file         <code>sellers_aggregate_scored.csv</code> in the <code>aggregated_files</code> folder.
</p>

<h2>Record Selection</h2>

<p>
  Finally, the function <code>define_spinjoy_selection</code> allows you to build the record catalog. It takes two parameters as input.
</p>

<ol>
  <li>
    <p>
      The number of desired genres in the final catalog. Genres are ordered according to their representation in the reference database. For example, if you select 2 as the             number of genres, you will get records for the two most represented genres in the reference database.
    </p>
  </li>

  <li>
    <p>The number of records desired in the final catalog.
    </p>
  </li>
</ol>

<p>
  The selection is based on sorting values according to the <code>attractivity_score</code> data calculated through scoring.
</p>

    <p>
        The function <code>define_spinjoy_selection</code> exports the selection as a file <code>spinjoy_catalog_{export_time}.csv</code> at the root of the project directory.
    </p>

