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

<h2>Backlog/h2>

<body><article id="fbef14c2-cd16-4e79-94ad-b22d0d620280" class="page sans"><header><h1 class="page-title">Backlog</h1><p class="page-description"></p></header><div class="page-body"><div id="ba33c08f-69e7-414f-9fb3-00a0bbf08f73" class="collection-content"><h4 class="collection-title">Backlog</h4><table class="collection-content"><thead><tr><th><span class="icon property-icon"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width:14px;height:14px;display:block;fill:rgba(55, 53, 47, 0.45);flex-shrink:0" class="typesTitle"><path d="M0.637695 13.1914C1.0957 13.1914 1.32812 13 1.47852 12.5215L2.24414 10.3887H6.14746L6.90625 12.5215C7.05664 13 7.2959 13.1914 7.74707 13.1914C8.22559 13.1914 8.5332 12.9043 8.5332 12.4531C8.5332 12.2891 8.50586 12.1523 8.44434 11.9678L5.41602 3.79199C5.2041 3.21777 4.82129 2.9375 4.19922 2.9375C3.60449 2.9375 3.21484 3.21777 3.0166 3.78516L-0.0322266 12.002C-0.09375 12.1797 -0.121094 12.3232 -0.121094 12.4668C-0.121094 12.918 0.166016 13.1914 0.637695 13.1914ZM2.63379 9.12402L4.17871 4.68066H4.21973L5.76465 9.12402H2.63379ZM12.2793 13.2324C13.3115 13.2324 14.2891 12.6787 14.7129 11.8037H14.7402V12.5762C14.7471 12.9863 15.0273 13.2393 15.4238 13.2393C15.834 13.2393 16.1143 12.9795 16.1143 12.5215V8.00977C16.1143 6.49902 14.9658 5.52148 13.1543 5.52148C11.7666 5.52148 10.6592 6.08887 10.2695 6.99121C10.1943 7.15527 10.1533 7.3125 10.1533 7.46289C10.1533 7.81152 10.4062 8.04395 10.7686 8.04395C11.0215 8.04395 11.2129 7.94824 11.3496 7.73633C11.7529 6.99121 12.2861 6.65625 13.1064 6.65625C14.0977 6.65625 14.6992 7.20996 14.6992 8.1123V8.67285L12.5664 8.7959C10.7686 8.8916 9.77734 9.69824 9.77734 11.0107C9.77734 12.3369 10.8096 13.2324 12.2793 13.2324ZM12.6621 12.1387C11.8008 12.1387 11.2129 11.667 11.2129 10.9561C11.2129 10.2725 11.7598 9.82129 12.7578 9.75977L14.6992 9.62988V10.3203C14.6992 11.3457 13.7969 12.1387 12.6621 12.1387Z"></path></svg></span>Name</th><th><span class="icon property-icon"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width:14px;height:14px;display:block;fill:rgba(55, 53, 47, 0.45);flex-shrink:0" class="typesMultipleSelect"><path d="M1.91602 4.83789C2.44238 4.83789 2.87305 4.40723 2.87305 3.87402C2.87305 3.34766 2.44238 2.91699 1.91602 2.91699C1.38281 2.91699 0.952148 3.34766 0.952148 3.87402C0.952148 4.40723 1.38281 4.83789 1.91602 4.83789ZM5.1084 4.52344H14.3984C14.7607 4.52344 15.0479 4.23633 15.0479 3.87402C15.0479 3.51172 14.7607 3.22461 14.3984 3.22461H5.1084C4.74609 3.22461 4.45898 3.51172 4.45898 3.87402C4.45898 4.23633 4.74609 4.52344 5.1084 4.52344ZM1.91602 9.03516C2.44238 9.03516 2.87305 8.60449 2.87305 8.07129C2.87305 7.54492 2.44238 7.11426 1.91602 7.11426C1.38281 7.11426 0.952148 7.54492 0.952148 8.07129C0.952148 8.60449 1.38281 9.03516 1.91602 9.03516ZM5.1084 8.7207H14.3984C14.7607 8.7207 15.0479 8.43359 15.0479 8.07129C15.0479 7.70898 14.7607 7.42188 14.3984 7.42188H5.1084C4.74609 7.42188 4.45898 7.70898 4.45898 8.07129C4.45898 8.43359 4.74609 8.7207 5.1084 8.7207ZM1.91602 13.2324C2.44238 13.2324 2.87305 12.8018 2.87305 12.2686C2.87305 11.7422 2.44238 11.3115 1.91602 11.3115C1.38281 11.3115 0.952148 11.7422 0.952148 12.2686C0.952148 12.8018 1.38281 13.2324 1.91602 13.2324ZM5.1084 12.918H14.3984C14.7607 12.918 15.0479 12.6309 15.0479 12.2686C15.0479 11.9062 14.7607 11.6191 14.3984 11.6191H5.1084C4.74609 11.6191 4.45898 11.9062 4.45898 12.2686C4.45898 12.6309 4.74609 12.918 5.1084 12.918Z"></path></svg></span>feature</th><th><span class="icon property-icon"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width:14px;height:14px;display:block;fill:rgba(55, 53, 47, 0.45);flex-shrink:0" class="typesMultipleSelect"><path d="M1.91602 4.83789C2.44238 4.83789 2.87305 4.40723 2.87305 3.87402C2.87305 3.34766 2.44238 2.91699 1.91602 2.91699C1.38281 2.91699 0.952148 3.34766 0.952148 3.87402C0.952148 4.40723 1.38281 4.83789 1.91602 4.83789ZM5.1084 4.52344H14.3984C14.7607 4.52344 15.0479 4.23633 15.0479 3.87402C15.0479 3.51172 14.7607 3.22461 14.3984 3.22461H5.1084C4.74609 3.22461 4.45898 3.51172 4.45898 3.87402C4.45898 4.23633 4.74609 4.52344 5.1084 4.52344ZM1.91602 9.03516C2.44238 9.03516 2.87305 8.60449 2.87305 8.07129C2.87305 7.54492 2.44238 7.11426 1.91602 7.11426C1.38281 7.11426 0.952148 7.54492 0.952148 8.07129C0.952148 8.60449 1.38281 9.03516 1.91602 9.03516ZM5.1084 8.7207H14.3984C14.7607 8.7207 15.0479 8.43359 15.0479 8.07129C15.0479 7.70898 14.7607 7.42188 14.3984 7.42188H5.1084C4.74609 7.42188 4.45898 7.70898 4.45898 8.07129C4.45898 8.43359 4.74609 8.7207 5.1084 8.7207ZM1.91602 13.2324C2.44238 13.2324 2.87305 12.8018 2.87305 12.2686C2.87305 11.7422 2.44238 11.3115 1.91602 11.3115C1.38281 11.3115 0.952148 11.7422 0.952148 12.2686C0.952148 12.8018 1.38281 13.2324 1.91602 13.2324ZM5.1084 12.918H14.3984C14.7607 12.918 15.0479 12.6309 15.0479 12.2686C15.0479 11.9062 14.7607 11.6191 14.3984 11.6191H5.1084C4.74609 11.6191 4.45898 11.9062 4.45898 12.2686C4.45898 12.6309 4.74609 12.918 5.1084 12.918Z"></path></svg></span>Tags</th><th><span class="icon property-icon"><svg role="graphics-symbol" viewBox="0 0 16 16" style="width:14px;height:14px;display:block;fill:rgba(55, 53, 47, 0.45);flex-shrink:0" class="typesStatus"><path d="M8.75488 1.02344C8.75488 0.613281 8.41309 0.264648 8.00293 0.264648C7.59277 0.264648 7.25098 0.613281 7.25098 1.02344V3.11523C7.25098 3.51855 7.59277 3.86719 8.00293 3.86719C8.41309 3.86719 8.75488 3.51855 8.75488 3.11523V1.02344ZM3.91504 5.0293C4.20215 5.31641 4.69434 5.32324 4.97461 5.03613C5.26855 4.74902 5.26855 4.25684 4.98145 3.96973L3.53906 2.52051C3.25195 2.2334 2.7666 2.21973 2.47949 2.50684C2.19238 2.79395 2.18555 3.28613 2.47266 3.57324L3.91504 5.0293ZM10.9629 4.01758C10.6826 4.30469 10.6826 4.79688 10.9697 5.08398C11.2568 5.37109 11.749 5.36426 12.0361 5.07715L13.4854 3.62793C13.7725 3.34082 13.7725 2.84863 13.4785 2.55469C13.1982 2.27441 12.7061 2.27441 12.4189 2.56152L10.9629 4.01758ZM15.0234 8.78906C15.4336 8.78906 15.7822 8.44727 15.7822 8.03711C15.7822 7.62695 15.4336 7.28516 15.0234 7.28516H12.9385C12.5283 7.28516 12.1797 7.62695 12.1797 8.03711C12.1797 8.44727 12.5283 8.78906 12.9385 8.78906H15.0234ZM0.975586 7.28516C0.56543 7.28516 0.223633 7.62695 0.223633 8.03711C0.223633 8.44727 0.56543 8.78906 0.975586 8.78906H3.07422C3.48438 8.78906 3.83301 8.44727 3.83301 8.03711C3.83301 7.62695 3.48438 7.28516 3.07422 7.28516H0.975586ZM12.0361 10.9902C11.749 10.71 11.2568 10.71 10.9629 10.9971C10.6826 11.2842 10.6826 11.7764 10.9697 12.0635L12.4258 13.5127C12.7129 13.7998 13.2051 13.793 13.4922 13.5059C13.7793 13.2256 13.7725 12.7266 13.4854 12.4395L12.0361 10.9902ZM2.52051 12.4395C2.22656 12.7266 2.22656 13.2188 2.50684 13.5059C2.79395 13.793 3.28613 13.7998 3.57324 13.5127L5.02246 12.0703C5.31641 11.7832 5.31641 11.291 5.03613 11.0039C4.74902 10.7168 4.25684 10.71 3.96973 10.9971L2.52051 12.4395ZM8.75488 12.9658C8.75488 12.5557 8.41309 12.207 8.00293 12.207C7.59277 12.207 7.25098 12.5557 7.25098 12.9658V15.0576C7.25098 15.4609 7.59277 15.8096 8.00293 15.8096C8.41309 15.8096 8.75488 15.4609 8.75488 15.0576V12.9658Z"></path></svg></span>Status</th></tr></thead><tbody><tr id="83e2c397-b588-446c-8501-d9ecb75eb9cd"><td class="cell-title">Format media_condition correctly</td><td class="cell-[NW="></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="7ef44683-5746-459a-84fc-d92a131e3e46"><td class="cell-title">Switch from absolute to relative folder paths</td><td class="cell-[NW="><span class="selected-value">All</span></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="3a7f12bb-07be-49e5-a4ee-2a8ed9bef85e"><td class="cell-title">Stock and display the nb of NA rows</td><td class="cell-[NW="><span class="selected-value">delete_na_rows</span></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="671865e9-c4c1-4f56-8745-3fcf60f28204"><td class="cell-title">Use pd.read_csv that will concatenate automatically the csv</td><td class="cell-[NW="><span class="selected-value select-value-color-orange">create_sellers_aggregate</span></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="ad25882f-614b-4212-bd83-bf721eafc7e5"><td class="cell-title">Check if there are empty df before concatenation</td><td class="cell-[NW="><span class="selected-value select-value-color-orange">create_sellers_aggregate</span></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="cb90ec6e-d4dd-4298-bdf0-7fb9e5365179"><td class="cell-title">Remove release_id duplicates (same release for different sellers)</td><td class="cell-[NW="></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="839bff27-d575-441a-b446-3b5bed644080"><td class="cell-title">Get artist name and title of the discogs csv</td><td class="cell-[NW="></td><td class="cell-bRhj"><span class="selected-value select-value-color-purple">Bug</span></td><td class="cell-ZqYV"><span class="status-value select-value-color-green"><div class="status-dot status-dot-color-green"></div>Done</span></td></tr><tr id="75434bee-41ab-4247-80d8-483ffbdf4ee4"><td class="cell-title">Check the good syntaxe</td><td class="cell-[NW="><span class="selected-value select-value-color-blue">scrap_releases_url</span></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="533eeb21-82d7-421b-a362-ab4e42958253"><td class="cell-title">Use ‘keep_default_na’ or ‘na_filter’ in the read_csv function instead of the delete_na_rows</td><td class="cell-[NW="></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="2cd194ec-9e83-4975-9a17-f10dd582fb99"><td class="cell-title">Use sys module to be able to run the script define_spinjoy_selection from the shell</td><td class="cell-[NW="><span class="selected-value select-value-color-purple">define_spinjoy_selection</span></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="4b3a97bb-cdf6-4c2f-a97f-64d221ed86cc"><td class="cell-title">Use seller_aggregate_scored.csv as the third parameter for the function</td><td class="cell-[NW="><span class="selected-value select-value-color-purple">define_spinjoy_selection</span></td><td class="cell-bRhj"></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr><tr id="4f04c8b3-60ce-4d4c-bcc2-f4984a344340"><td class="cell-title">Explain results differences in the selection between old et new project</td><td class="cell-[NW="></td><td class="cell-bRhj"><span class="selected-value select-value-color-yellow">Evolution</span></td><td class="cell-ZqYV"><span class="status-value"><div class="status-dot"></div>Not started</span></td></tr></tbody></table><br/><br/></div><p id="a0850ec6-997f-4ef3-a620-9bb350cdbf03" class="">
</p></div></article><span class="sans" style="font-size:14px;padding-top:2em"></span></body></html>


