
# Investigating what's missing

__Date 3/31/2023__

__Author: Michelle D.__

The first round of the scraping process resulted in 151,494 records. 

We used the following function to scrape each column.
``` python
def parse_speech(self, response):
    person = response.css("h3.diet-title a::text").get()
    title = response.css("div.field-ds-doc-title h1::text").get()
    date = response.css(
        "div.field-docs-start-date-time span.date-display-single::text"
    ).get()
    content = response.css("div.field-docs-content p::text").getall()
    url = response.url
```
Of those records 2,554 rows had mising data in at least one column.

Below is a table of the number of missing information per column. The number is not mutually exclusive across the entire table.

| colname     | # missing   |
| ----------- | ----------- |
| person      | 2           |
| title       | 2           |
| date        | 34          |
| content     | 2,528       |
| url         | 0           |

## Reviewing each column

Each column was explored to find common themes that would explain why we obtained missing data.

### Person/Title

> Missing: 2
>
> [3515, 61156]

The cells that were missing in these two columns were from the same rows. Although this section is about person/title, the content in these two rows were also missing and therefore will be explored.


| row #'s  | title reason | person reason | content reason | url |
| -------- | ------------ | ------------- | -------------- | ------ |
| 3515     | Title is located under the `fields-docs-content` class; `h2` ref | 6 people were listed at the end in the `fields-docs-content` class | Content exists within subtags and not within the paragraph base element.| https://www.presidency.ucsb.edu/documents/appeal-the-independent-democrats-congress-the-people-the-united-states |
| 61156    | Title is located under the `fields-docs-content` class; bolded in the `paragraph` element| No author found however, the citation at the bottom lists two people. We may ignore this and say no author.| Content lives in subtags.| https://www.presidency.ucsb.edu/documents/the-republican-contract-with-america |
 
### Date

> Missing: 34
>
> [27836, 27837,27841, 27843, 27845, 27846, 27847, 27848, 27849, 27850, 27851, 27852, 27853, 27854, 27855, 27856, 27857, 27858, 27859, 27860, 27861, 27862, 27863, 27864, 27865, 27866, 27867, 27868, 27869, 27870, 27871, 27872, 27873, 27874]

All 34 with missing dates had __"Event Timeline"__ in them.

The timeline exists in the `<tbody>` block within a `<table>` in the `field-docs-content`. See the below example.

The words exists within a `<span style>` element. See below for an example.

``` html
<div class="field-docs-content">
    <table class="Table" style="width:5.9in; border-collapse:
collapse; border: none" width="566",
        <body>
            <tr>
                <td colspan="2" style="border:none; border-bottom:solid #43b4e0 1.Opt; width:1.6in; padding:Oin 5.4pt Oin 5.4pt" width="154">
                    <p align="center" style="margin-top:3.0pt; margin-right: Oin; margin-bottom:3.Opt; margin-left:in; text-align: center">
                        <span style="line-height: normal"> = $0
                            <b>J</b>
                        </span>
                        <span style="line-height: normal">
                            <b>immy Carter (39) Event Timeline</b> 
                            </span>
                    </p>
```

### Content

> Missing: 2,528
>
> Too many to list out the numbers. Please run the notebook for the list.

After searching through the titles where the content is missing, I found common themes. The below accounts for about 95% of the different types of speeches.

| speech type     | # missing   | %    | reason |
| --------------- | ----------- | ---- | ------ |
| tweets          | 2,033       | 80.4 | content exists inside a table with multiple subtags |
| press release   | 333         | 13.2 | looks like content exists in subtags, there were also videos and pages with no text |
| executive order | 36          | 1.4  | content may say "...not published" and exists in a subtag. |
| fact sheets     | 35          | 1.4  | content exists inside subtags |

## Suggestions

- Use the provided link to obtain all the text in the subtags: https://stackoverflow.com/questions/40985060/scrapy-css-selector-get-text-of-all-inner-tags
  - If this goes through all the different types of subtags, then this should solve most of the problems.
  - Will probably still have to clean up the doc after.

