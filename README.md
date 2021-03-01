# Murderpedia Web Scraper

This project was made with the purpose of scraping data from <a href="http://murderpedia.org" target = "_blank">Murderpedia</a>.

The data is stored in a local **dataset.json** file. Reffer to the [documentation](#documentation) for more information on how everything works.

Each murderer has a table of interesting data, which is what this project aims to collect, for most entries.

# Example

Below is an example of a murderer we want to scrape the data from : 

![William Kemmler Example](https://i.ibb.co/cLjm6B6/kemmler.png)

And what the data looks like after extraction :

```
{
    "Name": "William KEMMLER",
    "Murderpedia_URL": "http://murderpedia.org/male.K/k/kemmler-william.htm",
    "Image_URL": "http://murderpedia.org/male.K/images/kemmler_william/kemmler000.jpg",
    "Classification": "Murderer",
    "Characteristics": "Parricide",
    "Number of victims": "1",
    "Date of murder": "March 29, 1889",
    "Date of birth": "May 9, 1860",
    "Victim profile": "Tillie Ziegler (his common-law wife)",
    "Method of murder": "Beating with a hatchet",
    "Location": "Buffalo, New York, USA",
    "Status": "Executed by electrocution in New York on August 6, 1890"
}
```

# Documentation

Code documentation can be found on the <a href="https://daniel-iova.github.io/murderpedia-web-scraper/" target="_blank">Github Pages for the project</a>.
<br>There are also comments present all around the code base.

# Running the program

To run the program you can either download the repo and run [\_\_main\_\_.py](__main__.py) or run the [project's jupyter notebook](notebooks/murderpedia-web-scraper.ipynb) \(recommended\).
<br>Be wary that the execution time is around 20 to 25 minutes.
<br>Also, due to some limitations regarding http requests you might need to re run the program if the number of uncollected murderers is above 70.

# License

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

© 2021 Daniel Iova. All rights reserved.

See also : [LICENSE.md](LICENSE.md)
